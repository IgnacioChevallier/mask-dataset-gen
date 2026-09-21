"""Configuración y rutas compartidas para datasets multi-incendio."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import subprocess
import tempfile
from copy import deepcopy
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from importlib import metadata as importlib_metadata
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config" / "incendios"
DATASET_DIR = BASE_DIR / "dataset"
DEFAULT_EVENT = "puerto-patriada-2026"
DEFAULT_RUN = "legacy-v1"
SAFE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SUPPORTED_COLLECTION = "COPERNICUS/S2_SR_HARMONIZED"


class ConfigError(ValueError):
    """Configuración inválida o inconsistente."""


@dataclass(frozen=True)
class RunPaths:
    event_id: str
    run_id: str
    root: Path
    pre: Path
    post: Path
    masks: Path
    valid: Path
    visualizations: Path
    roi_summaries: Path
    tile_visualizations: Path
    diagnostics: Path
    metadata: Path
    manifest: Path
    summary: Path

    def create(self) -> None:
        for directory in (
            self.pre,
            self.post,
            self.masks,
            self.valid,
            self.roi_summaries,
            self.tile_visualizations,
            self.diagnostics,
        ):
            directory.mkdir(parents=True, exist_ok=True)


def validate_id(value: str, label: str) -> str:
    if not SAFE_ID_RE.fullmatch(value):
        raise ConfigError(
            f"{label} inválido: {value!r}. Usá minúsculas, números y guiones."
        )
    return value


def list_events() -> list[dict[str, str]]:
    events = []
    for path in sorted(CONFIG_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            events.append(
                {
                    "event_id": data.get("event_id", path.stem),
                    "name": data.get("name", ""),
                    "path": str(path),
                }
            )
        except (OSError, json.JSONDecodeError):
            events.append({"event_id": path.stem, "name": "CONFIGURACIÓN INVÁLIDA", "path": str(path)})
    return events


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def load_event(event_id: str) -> dict[str, Any]:
    validate_id(event_id, "event_id")
    path = CONFIG_DIR / f"{event_id}.json"
    if not path.is_file():
        available = ", ".join(event["event_id"] for event in list_events()) or "ninguno"
        raise ConfigError(f"No existe {path}. Eventos disponibles: {available}.")
    try:
        event = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"JSON inválido en {path}: {exc}") from exc
    if event.get("event_id") != event_id:
        raise ConfigError(f"event_id de {path} no coincide con su nombre de archivo.")
    return event


def effective_config(event_id: str, run_id: str) -> dict[str, Any]:
    validate_id(run_id, "run_id")
    event = load_event(event_id)
    runs = event.get("runs")
    if not isinstance(runs, dict) or run_id not in runs:
        available = ", ".join(sorted(runs or {})) or "ninguno"
        raise ConfigError(
            f"El run {run_id!r} no está definido para {event_id}. Disponibles: {available}."
        )

    defaults = event.get("defaults", {})
    run = runs[run_id]
    config = _deep_merge(defaults, run)
    config.update(
        {
            "event_id": event_id,
            "event_name": event.get("name", event_id),
            "event_description": event.get("description", ""),
            "fire_start_date": event.get("fire_start_date"),
            "run_id": run_id,
            "source": deepcopy(event.get("source", {})),
            "rois": deepcopy(run.get("rois", event.get("rois", []))),
        }
    )
    if "reference" in event:
        config["reference"] = deepcopy(event["reference"])
    validate_config(config)
    return config


def validate_config(config: dict[str, Any]) -> None:
    required = {
        "event_id",
        "run_id",
        "source",
        "rois",
        "windows",
        "bands",
        "cloud_percentage_max",
        "mask",
        "grid",
        "quality",
        "algorithm_version",
    }
    missing = sorted(required - config.keys())
    if missing:
        raise ConfigError(f"Faltan campos requeridos: {', '.join(missing)}.")

    validate_id(config["event_id"], "event_id")
    validate_id(config["run_id"], "run_id")
    if config["source"].get("collection") != SUPPORTED_COLLECTION:
        raise ConfigError(
            f"Sólo se soporta {SUPPORTED_COLLECTION}; se recibió "
            f"{config['source'].get('collection')!r}."
        )

    rois = config["rois"]
    if not isinstance(rois, list) or not rois:
        raise ConfigError("rois debe ser una lista no vacía.")
    seen_roi_ids: set[str] = set()
    for roi in rois:
        roi_id = roi.get("id")
        validate_id(roi_id, "roi.id")
        if roi_id in seen_roi_ids:
            raise ConfigError(f"ROI duplicado: {roi_id}.")
        seen_roi_ids.add(roi_id)
        bbox = roi.get("bbox")
        if not isinstance(bbox, list) or len(bbox) != 4:
            raise ConfigError(f"El ROI {roi_id} debe tener bbox [oeste, sur, este, norte].")
        west, south, east, north = bbox
        if not all(isinstance(value, (int, float)) for value in bbox) or west >= east or south >= north:
            raise ConfigError(f"bbox inválido para {roi_id}: {bbox}.")

    for period in ("pre", "post"):
        window = config["windows"].get(period, {})
        try:
            start = date.fromisoformat(window["start"])
            end = date.fromisoformat(window["end_inclusive"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ConfigError(f"Ventana {period} inválida: {window!r}.") from exc
        if start > end:
            raise ConfigError(f"La ventana {period} comienza después de terminar.")

    bands = config["bands"]
    required_bands = {"B2", "B3", "B4", "B8", "B11", "B12"}
    if not isinstance(bands, list) or not required_bands.issubset(bands):
        raise ConfigError(f"bands debe incluir {sorted(required_bands)}.")

    grid = config["grid"]
    if grid.get("scale_m", 0) <= 0 or grid.get("tile_pixels", 0) <= 0:
        raise ConfigError("grid.scale_m y grid.tile_pixels deben ser positivos.")
    warning = config["quality"].get("valid_coverage_warning_pct")
    if not isinstance(warning, (int, float)) or not 0 <= warning <= 100:
        raise ConfigError("quality.valid_coverage_warning_pct debe estar entre 0 y 100.")


def get_run_paths(event_id: str, run_id: str) -> RunPaths:
    validate_id(event_id, "event_id")
    validate_id(run_id, "run_id")
    root = DATASET_DIR / event_id / "runs" / run_id
    visualizations = root / "visualizaciones"
    return RunPaths(
        event_id=event_id,
        run_id=run_id,
        root=root,
        pre=root / "imagenes_pre",
        post=root / "imagenes_post",
        masks=root / "mascaras",
        valid=root / "calidad" / "observacion_valida",
        visualizations=visualizations,
        roi_summaries=visualizations / "resumen_roi",
        tile_visualizations=visualizations / "tiles",
        diagnostics=visualizations / "diagnosticos",
        metadata=root / "metadata.csv",
        manifest=root / "run.json",
        summary=root / "resumen.md",
    )


def config_hash(config: dict[str, Any]) -> str:
    canonical = json.dumps(config, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def end_exclusive(end_inclusive: str) -> str:
    return (date.fromisoformat(end_inclusive) + timedelta(days=1)).isoformat()


def build_tiles(config: dict[str, Any]) -> list[dict[str, Any]]:
    scale = float(config["grid"]["scale_m"])
    tile_pixels = int(config["grid"]["tile_pixels"])
    tile_degrees = (scale * tile_pixels) / 111_320
    tiles: list[dict[str, Any]] = []
    for roi_index, roi in enumerate(config["rois"], start=1):
        west, south, east, north = roi["bbox"]
        cols = math.ceil((east - west) / tile_degrees)
        rows = math.ceil((north - south) / tile_degrees)
        for row in range(rows):
            lat_min = south + row * tile_degrees
            lat_max = min(lat_min + tile_degrees, north)
            for col in range(cols):
                lon_min = west + col * tile_degrees
                lon_max = min(lon_min + tile_degrees, east)
                tile_id = f"roi_{roi_index:02d}_r{row:03d}_c{col:03d}"
                tiles.append(
                    {
                        "tile_id": tile_id,
                        "roi_id": roi["id"],
                        "roi_index": roi_index,
                        "row": row,
                        "col": col,
                        "bbox": [lon_min, lat_min, lon_max, lat_max],
                    }
                )
    return tiles


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def git_commit() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=BASE_DIR,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def dependency_versions() -> dict[str, str]:
    versions = {}
    for package in ("earthengine-api", "geemap", "geedim", "numpy", "rasterio", "matplotlib"):
        try:
            versions[package] = importlib_metadata.version(package)
        except importlib_metadata.PackageNotFoundError:
            versions[package] = "not-installed"
    return versions
