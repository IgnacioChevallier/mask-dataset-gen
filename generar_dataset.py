"""Genera datasets Sentinel-2 de áreas quemadas por evento y run."""

from __future__ import annotations

import argparse
import csv
import multiprocessing as mp
import os
import platform
import shutil
import tempfile
from functools import reduce
from pathlib import Path
from typing import Any

from dataset_runs import (
    DEFAULT_EVENT,
    DEFAULT_RUN,
    ConfigError,
    build_tiles,
    config_hash,
    dependency_versions,
    effective_config,
    end_exclusive,
    get_run_paths,
    git_commit,
    list_events,
    read_json,
    utc_now,
    write_json_atomic,
)


METADATA_FIELDS = [
    "event_id", "run_id", "roi_id", "row", "col", "tile",
    "lon_min", "lat_min", "lon_max", "lat_max",
    "pct_quemado_valido", "hectareas_quemadas", "pct_observacion_valida",
    "fecha_pre", "fecha_post", "escala_m", "status", "error",
]

_GEE: dict[str, Any] = {}


def _mask_clouds(image):
    scl = image.select("SCL")
    return image.updateMask(
        scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
    )


def _build_gee_assets(config: dict[str, Any]):
    import ee

    geometries = [ee.Geometry.Rectangle(roi["bbox"]) for roi in config["rois"]]
    region = reduce(lambda left, right: left.union(right), geometries)
    collection = (
        ee.ImageCollection(config["source"]["collection"])
        .filterBounds(region)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", config["cloud_percentage_max"]))
    )
    pre_window = config["windows"]["pre"]
    post_window = config["windows"]["post"]
    pre_collection = collection.filterDate(
        pre_window["start"], end_exclusive(pre_window["end_inclusive"])
    )
    post_collection = collection.filterDate(
        post_window["start"], end_exclusive(post_window["end_inclusive"])
    )

    pre_masked = pre_collection.map(_mask_clouds).median()
    post_masked = post_collection.map(_mask_clouds).median()
    pre_full = pre_collection.median()
    post_full = post_collection.median()

    pre_nbr = pre_masked.normalizedDifference(["B8", "B12"]).rename("NBR_pre")
    post_nbr = post_masked.normalizedDifference(["B8", "B12"]).rename("NBR_post")
    dnbr = pre_nbr.subtract(post_nbr).rename("dNBR")

    post_visible = post_full.select(["B2", "B3", "B4"])
    post_brightness = post_visible.reduce(ee.Reducer.mean())
    post_chroma = post_visible.reduce(ee.Reducer.max()).subtract(
        post_visible.reduce(ee.Reducer.min())
    )
    post_ndsi = post_full.normalizedDifference(["B3", "B11"]).rename("NDSI_post")
    pre_ndwi = pre_full.normalizedDifference(["B3", "B8"]).rename("NDWI_pre")

    mask_config = config["mask"]
    snow_or_gray = post_ndsi.gt(mask_config["ndsi_snow_max"]).Or(
        post_brightness.gt(mask_config["brightness_max"]).And(
            post_chroma.lt(mask_config["chroma_min"])
        )
    )
    pre_water = pre_ndwi.gt(mask_config["pre_ndwi_water_max"])
    burned_raw = (
        dnbr.gt(mask_config["dnbr_threshold"])
        .And(pre_nbr.gt(mask_config["pre_nbr_min"]))
        .And(post_nbr.lt(mask_config["post_nbr_max"]))
        .And(snow_or_gray.Not())
        .And(pre_water.Not())
    )
    burned_candidates = burned_raw.updateMask(burned_raw)
    min_pixels = int(mask_config["min_connected_pixels"])
    burned_clean = (
        burned_candidates.connectedPixelCount(min_pixels + 1, True)
        .gte(min_pixels)
        .unmask(0)
    )
    burned = (
        burned_clean.focal_max(
            radius=int(mask_config["dilation_pixels"]), units="pixels"
        )
        .rename("quemado")
        .toUint8()
    )

    bands = config["bands"]
    pre_valid = pre_masked.select(bands).mask().reduce(ee.Reducer.min()).gt(0)
    post_valid = post_masked.select(bands).mask().reduce(ee.Reducer.min()).gt(0)
    valid = pre_valid.And(post_valid).rename("observacion_valida").unmask(0).toUint8()

    return {
        "region": region,
        "geometries": geometries,
        "pre_collection": pre_collection,
        "post_collection": post_collection,
        "pre": pre_full.select(bands),
        "post": post_full.select(bands),
        "burned": burned,
        "valid": valid,
    }


def _init_worker(worker_config: dict[str, Any]) -> None:
    import ee

    project = worker_config["config"]["source"].get("project")
    ee.Initialize(project=project) if project else ee.Initialize()
    _GEE.update(_build_gee_assets(worker_config["config"]))
    _GEE["worker_config"] = worker_config


def _atomic_download(image, destination: Path, geometry, scale: int) -> None:
    import geemap

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.stem}.part.tif")
    temporary.unlink(missing_ok=True)
    try:
        geemap.download_ee_image(
            image=image.clip(geometry),
            filename=str(temporary),
            region=geometry,
            scale=scale,
            crs="EPSG:4326",
        )
        os.replace(temporary, destination)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _tile_statistics(tile_geometry) -> tuple[float, float, float]:
    import ee

    burned = _GEE["burned"]
    valid = _GEE["valid"]
    scale = _GEE["worker_config"]["config"]["grid"]["scale_m"]
    means = ee.Image.cat(
        [
            valid.toFloat().rename("valid_fraction"),
            burned.updateMask(valid).toFloat().rename("burned_fraction"),
        ]
    ).reduceRegion(
        reducer=ee.Reducer.mean(), geometry=tile_geometry, scale=scale, maxPixels=1e8
    )
    area = (
        ee.Image.pixelArea()
        .rename("burned_area_m2")
        .updateMask(burned.eq(1).And(valid.eq(1)))
        .reduceRegion(
            reducer=ee.Reducer.sum(), geometry=tile_geometry, scale=scale, maxPixels=1e8
        )
    )
    stats = ee.Dictionary(
        {
            "valid_fraction": means.get("valid_fraction"),
            "burned_fraction": means.get("burned_fraction"),
            "burned_area_m2": area.get("burned_area_m2"),
        }
    ).getInfo()
    valid_pct = float(stats.get("valid_fraction") or 0) * 100
    burned_pct = float(stats.get("burned_fraction") or 0) * 100
    burned_hectares = float(stats.get("burned_area_m2") or 0) / 10_000
    return burned_pct, burned_hectares, valid_pct


def _download_one(tile: dict[str, Any]) -> dict[str, Any]:
    import ee

    worker_config = _GEE["worker_config"]
    config = worker_config["config"]
    paths = worker_config["paths"]
    tile_id = tile["tile_id"]
    bbox = tile["bbox"]
    geometry = ee.Geometry.Rectangle(bbox)
    destinations = {
        "pre": Path(paths["pre"]) / f"{tile_id}.tif",
        "post": Path(paths["post"]) / f"{tile_id}.tif",
        "burned": Path(paths["masks"]) / f"{tile_id}.tif",
        "valid": Path(paths["valid"]) / f"{tile_id}.tif",
    }
    ordinal = int(worker_config["tile_ordinals"][tile_id])
    total = int(worker_config["total"])
    complete_files = all(path.is_file() for path in destinations.values())
    action = "Verificando" if complete_files else "Descargando"
    print(f"[{ordinal:03d}/{total}] {action} {tile_id}...", flush=True)

    try:
        if not complete_files:
            for path in destinations.values():
                path.unlink(missing_ok=True)
            scale = int(config["grid"]["scale_m"])
            _atomic_download(_GEE["pre"], destinations["pre"], geometry, scale)
            _atomic_download(_GEE["post"], destinations["post"], geometry, scale)
            _atomic_download(_GEE["burned"], destinations["burned"], geometry, scale)
            _atomic_download(_GEE["valid"], destinations["valid"], geometry, scale)

        burned_pct, burned_hectares, valid_pct = _tile_statistics(geometry)
        warning_threshold = float(config["quality"]["valid_coverage_warning_pct"])
        if valid_pct == 0:
            status = "error"
            error = "El tile no tiene observaciones válidas simultáneas en PRE y POST."
        elif valid_pct < warning_threshold:
            status = "warning"
            error = f"Cobertura válida menor a {warning_threshold:g}%."
        else:
            status = "ok"
            error = ""
        print(
            f"    ✓ {tile_id}: {burned_pct:.2f}% quemado sobre "
            f"{valid_pct:.2f}% válido ({burned_hectares:.2f} ha)",
            flush=True,
        )
    except Exception as exc:
        status = "error"
        error = str(exc)
        burned_pct = burned_hectares = valid_pct = 0.0
        print(f"    ✗ {tile_id}: {exc}", flush=True)

    pre_window = config["windows"]["pre"]
    post_window = config["windows"]["post"]
    return {
        "event_id": config["event_id"],
        "run_id": config["run_id"],
        "roi_id": tile["roi_id"],
        "row": tile["row"],
        "col": tile["col"],
        "tile": tile_id,
        "lon_min": bbox[0],
        "lat_min": bbox[1],
        "lon_max": bbox[2],
        "lat_max": bbox[3],
        "pct_quemado_valido": round(burned_pct, 4),
        "hectareas_quemadas": round(burned_hectares, 4),
        "pct_observacion_valida": round(valid_pct, 4),
        "fecha_pre": f"{pre_window['start']}/{pre_window['end_inclusive']}",
        "fecha_post": f"{post_window['start']}/{post_window['end_inclusive']}",
        "escala_m": config["grid"]["scale_m"],
        "status": status,
        "error": error,
    }


def _read_metadata(path: Path) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["tile"]: row for row in csv.DictReader(handle) if row.get("tile")}


def _write_metadata(path: Path, rows: dict[str, dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".metadata.", suffix=".csv", dir=path.parent)
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=METADATA_FIELDS,
                lineterminator="\n",
            )
            writer.writeheader()
            ordered = sorted(
                rows.values(),
                key=lambda row: (str(row["roi_id"]), int(row["row"]), int(row["col"])),
            )
            writer.writerows({field: row.get(field, "") for field in METADATA_FIELDS} for row in ordered)
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def _scene_inventory(assets: dict[str, Any]) -> dict[str, list[str]]:
    return {
        "pre": assets["pre_collection"].aggregate_array("system:index").getInfo(),
        "post": assets["post_collection"].aggregate_array("system:index").getInfo(),
    }


def _region_metrics(config: dict[str, Any], assets: dict[str, Any]) -> dict[str, Any]:
    import ee

    burned = assets["burned"]
    valid = assets["valid"]
    scale = config["grid"]["scale_m"]

    def calculate(label: str, geometry) -> dict[str, Any]:
        means = ee.Image.cat(
            [
                valid.toFloat().rename("valid_fraction"),
                burned.updateMask(valid).toFloat().rename("burned_fraction"),
            ]
        ).reduceRegion(
            reducer=ee.Reducer.mean(), geometry=geometry, scale=scale, maxPixels=1e10
        )
        area = (
            ee.Image.pixelArea()
            .rename("burned_area_m2")
            .updateMask(burned.eq(1).And(valid.eq(1)))
            .reduceRegion(
                reducer=ee.Reducer.sum(), geometry=geometry, scale=scale, maxPixels=1e10
            )
        )
        values = ee.Dictionary(
            {
                "valid_fraction": means.get("valid_fraction"),
                "burned_fraction": means.get("burned_fraction"),
                "burned_area_m2": area.get("burned_area_m2"),
            }
        ).getInfo()
        return {
            "id": label,
            "valid_coverage_pct": round(float(values.get("valid_fraction") or 0) * 100, 4),
            "burned_valid_pct": round(float(values.get("burned_fraction") or 0) * 100, 4),
            "burned_hectares": round(float(values.get("burned_area_m2") or 0) / 10_000, 4),
        }

    per_roi = [
        calculate(roi["id"], geometry)
        for roi, geometry in zip(config["rois"], assets["geometries"], strict=True)
    ]
    total = calculate("total", assets["region"])
    return {"total": total, "by_roi": per_roi}


def _validate_rasters(tiles: list[dict[str, Any]], paths) -> list[str]:
    import numpy as np
    import rasterio

    errors: list[str] = []
    for tile in tiles:
        tile_id = tile["tile_id"]
        files = {
            "pre": paths.pre / f"{tile_id}.tif",
            "post": paths.post / f"{tile_id}.tif",
            "mask": paths.masks / f"{tile_id}.tif",
            "valid": paths.valid / f"{tile_id}.tif",
        }
        missing = [name for name, path in files.items() if not path.is_file()]
        if missing:
            errors.append(f"{tile_id}: faltan {', '.join(missing)}")
            continue
        try:
            with rasterio.open(files["pre"]) as pre, rasterio.open(files["post"]) as post, rasterio.open(
                files["mask"]
            ) as mask, rasterio.open(files["valid"]) as valid:
                shape = (pre.height, pre.width)
                if any((src.height, src.width) != shape for src in (post, mask, valid)):
                    errors.append(f"{tile_id}: dimensiones incompatibles")
                if any(src.crs != pre.crs for src in (post, mask, valid)):
                    errors.append(f"{tile_id}: CRS incompatible")
                if any(not src.transform.almost_equals(pre.transform) for src in (post, mask, valid)):
                    errors.append(f"{tile_id}: transformación espacial incompatible")
                for label, source in (("máscara", mask), ("validez", valid)):
                    values = np.unique(source.read(1))
                    if not set(values.tolist()).issubset({0, 1}):
                        errors.append(f"{tile_id}: {label} no binaria: {values.tolist()}")
        except Exception as exc:
            errors.append(f"{tile_id}: no se pudo validar: {exc}")
    return errors


def _write_summary(config: dict[str, Any], manifest: dict[str, Any], rows: dict[str, dict[str, Any]], path: Path) -> None:
    metrics = manifest.get("metrics", {})
    total = metrics.get("total", {})
    ranked = sorted(
        (row for row in rows.values() if row.get("status") in {"ok", "warning"}),
        key=lambda row: float(row.get("pct_quemado_valido") or 0),
        reverse=True,
    )[:10]
    lines = [
        f"# Resumen: {config['event_name']} / {config['run_id']}",
        "",
        f"- Estado: `{manifest['status']}`",
        f"- Algoritmo: `{config['algorithm_version']}`",
        f"- Escenas PRE: {len(manifest['scenes']['pre'])}",
        f"- Escenas POST: {len(manifest['scenes']['post'])}",
        f"- Tiles esperados: {manifest['counts']['expected']}",
        f"- Tiles correctos: {manifest['counts']['ok']}",
        f"- Tiles con advertencia: {manifest['counts']['warning']}",
        f"- Tiles fallidos: {manifest['counts']['error']}",
        f"- Cobertura válida total: {total.get('valid_coverage_pct', 0):.2f}%",
        f"- Área clasificada como quemada: {total.get('burned_hectares', 0):.2f} ha",
        f"- Porcentaje quemado sobre área válida: {total.get('burned_valid_pct', 0):.2f}%",
    ]
    reference_area = config.get("reference", {}).get("burned_area_ha")
    if reference_area:
        detected_area = float(total.get("burned_hectares", 0))
        difference = detected_area - float(reference_area)
        lines.extend(
            [
                f"- Superficie oficial de referencia: {float(reference_area):.2f} ha",
                f"- Diferencia exploratoria respecto de la referencia: {difference:+.2f} ha",
            ]
        )
    lines.extend(
        [
            "",
            "## Tiles con mayor porcentaje quemado",
            "",
            "| Tile | ROI | Quemado válido | Cobertura válida | Hectáreas |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in ranked:
        lines.append(
            f"| `{row['tile']}` | `{row['roi_id']}` | "
            f"{float(row['pct_quemado_valido']):.2f}% | "
            f"{float(row['pct_observacion_valida']):.2f}% | "
            f"{float(row['hectareas_quemadas']):.2f} |"
        )
    lines.extend(
        [
            "", "## Visualizaciones", "",
            "Los mosaicos PRE, POST, máscara y superposición están en "
            "`visualizaciones/resumen_roi/`.",
            "",
            "Este resultado es exploratorio y no constituye una validación científica de la cicatriz.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _counts(rows: dict[str, dict[str, Any]], expected: int) -> dict[str, int]:
    counts = {"expected": expected, "ok": 0, "warning": 0, "error": 0}
    for row in rows.values():
        status = row.get("status", "error")
        if status in counts:
            counts[status] += 1
    return counts


def _new_manifest(
    config: dict[str, Any], hash_value: str, tiles: list[dict[str, Any]], scenes: dict[str, list[str]]
) -> dict[str, Any]:
    now = utc_now()
    return {
        "schema_version": 1,
        "event_id": config["event_id"],
        "run_id": config["run_id"],
        "origin": config.get("origin", "generated"),
        "status": "running",
        "created_at": now,
        "last_started_at": now,
        "completed_at": None,
        "configuration_hash": hash_value,
        "configuration": config,
        "tile_naming": config.get("tile_naming", "grid-position-v1"),
        "scenes": scenes,
        "environment": {
            "git_commit": git_commit(),
            "python": platform.python_version(),
            "dependencies": dependency_versions(),
        },
        "counts": {"expected": len(tiles), "ok": 0, "warning": 0, "error": 0},
        "metrics": {},
        "validation_errors": [],
        "errors": [],
    }


def _print_preflight(config: dict[str, Any], tiles: list[dict[str, Any]], scenes: dict[str, list[str]], root: Path) -> None:
    print(f"Evento: {config['event_id']} — {config['event_name']}")
    print(f"Run: {config['run_id']}")
    print(f"Destino: {root}")
    print(f"ROIs: {len(config['rois'])}")
    print(f"Tiles: {len(tiles)}")
    print(f"Escenas Sentinel-2 PRE: {len(scenes['pre'])}")
    print(f"Escenas Sentinel-2 POST: {len(scenes['post'])}")
    print(f"PRE: {config['windows']['pre']['start']} a {config['windows']['pre']['end_inclusive']} (inclusive)")
    print(f"POST: {config['windows']['post']['start']} a {config['windows']['post']['end_inclusive']} (inclusive)")
    for roi in config["rois"]:
        roi_tiles = sum(tile["roi_id"] == roi["id"] for tile in tiles)
        print(f"  {roi['id']}: {roi_tiles} tiles — bbox={roi['bbox']}")


def _clear_incomplete(event_id: str, run_id: str) -> int:
    paths = get_run_paths(event_id, run_id)
    if not paths.root.exists():
        print(f"No existe el run: {paths.root}")
        return 0
    if not paths.manifest.is_file():
        raise RuntimeError(f"Se rechaza borrar {paths.root}: no contiene run.json.")
    manifest = read_json(paths.manifest)
    if manifest.get("status") == "completed":
        raise RuntimeError("Se rechaza limpiar un run completado e inmutable.")
    expected = (Path("dataset") / event_id / "runs" / run_id).as_posix()
    if expected not in paths.root.as_posix():
        raise RuntimeError(f"Ruta de limpieza inesperada: {paths.root}")
    shutil.rmtree(paths.root)
    print(f"Run incompleto eliminado: {paths.root}")
    return 0


def run_generation(
    event_id: str, run_id: str, dry_run: bool = False, project: str | None = None
) -> int:
    import ee

    config = effective_config(event_id, run_id)
    if project:
        config["source"]["project"] = project
    paths = get_run_paths(event_id, run_id)
    hash_value = config_hash(config)

    if paths.manifest.is_file():
        existing_manifest = read_json(paths.manifest)
        if existing_manifest.get("configuration_hash") != hash_value:
            raise RuntimeError(
                "La configuración actual no coincide con el run existente. "
                "Usá otro run_id o restaurá la configuración original."
            )
        if existing_manifest.get("status") == "completed" and not dry_run:
            print(f"El run ya está completo e inmutable: {paths.root}")
            return 0

    print("Inicializando Google Earth Engine...")
    try:
        configured_project = config["source"].get("project")
        ee.Initialize(project=configured_project) if configured_project else ee.Initialize()
        assets = _build_gee_assets(config)
        scenes = _scene_inventory(assets)
    except Exception as exc:
        message = str(exc)
        if "authorize access" in message.lower() or "authenticate" in message.lower():
            raise RuntimeError(
                "Earth Engine requiere autenticación. Ejecutá "
                "`.venv/bin/earthengine authenticate` y repetí el comando."
            ) from exc
        if "no project found" in message.lower():
            raise RuntimeError(
                "Earth Engine requiere un proyecto Google Cloud registrado. "
                "Indicá `--project ID_DEL_PROYECTO`; el valor quedará sellado en run.json."
            ) from exc
        raise RuntimeError(f"No se pudo consultar Google Earth Engine: {message}") from exc
    if not scenes["pre"] or not scenes["post"]:
        raise RuntimeError(
            "No hay imágenes Sentinel-2 para una de las ventanas. "
            "Ajustá las fechas o la nubosidad máxima."
        )
    tiles = build_tiles(config)
    _print_preflight(config, tiles, scenes, paths.root)
    if dry_run:
        print("Dry-run finalizado: no se creó ni modificó ningún run.")
        return 0

    paths.create()
    if paths.manifest.is_file():
        manifest = read_json(paths.manifest)
        manifest["status"] = "running"
        manifest["last_started_at"] = utc_now()
        manifest["scenes"] = scenes
        manifest["errors"] = []
    else:
        manifest = _new_manifest(config, hash_value, tiles, scenes)
    write_json_atomic(paths.manifest, manifest)

    rows = _read_metadata(paths.metadata)
    worker_config = {
        "config": config,
        "paths": {
            "pre": str(paths.pre), "post": str(paths.post),
            "masks": str(paths.masks), "valid": str(paths.valid),
        },
        "total": len(tiles),
        "tile_ordinals": {tile["tile_id"]: index for index, tile in enumerate(tiles, start=1)},
    }

    try:
        with mp.Pool(
            processes=int(config.get("max_workers", 4)),
            initializer=_init_worker,
            initargs=(worker_config,),
        ) as pool:
            for row in pool.imap_unordered(_download_one, tiles):
                rows[row["tile"]] = row
                _write_metadata(paths.metadata, rows)
                manifest["counts"] = _counts(rows, len(tiles))
                write_json_atomic(paths.manifest, manifest)

        manifest["counts"] = _counts(rows, len(tiles))
        validation_errors = _validate_rasters(tiles, paths)
        if len(rows) != len(tiles):
            validation_errors.append(f"metadata.csv tiene {len(rows)} filas y se esperaban {len(tiles)}.")
        manifest["validation_errors"] = validation_errors
        manifest["metrics"] = _region_metrics(config, assets)

        if validation_errors or manifest["counts"]["error"] > 0:
            manifest["status"] = "incomplete"
            _write_summary(config, manifest, rows, paths.summary)
            write_json_atomic(paths.manifest, manifest)
            print(
                f"Run incompleto: {manifest['counts']['error']} tiles fallidos, "
                f"{len(validation_errors)} errores de validación."
            )
            return 2

        from visualizar_roi import generar_resumen_run

        generar_resumen_run(paths, config)
        manifest["status"] = "completed"
        manifest["completed_at"] = utc_now()
        _write_summary(config, manifest, rows, paths.summary)
        write_json_atomic(paths.manifest, manifest)
        print(f"Run completado: {paths.root}")
        return 0
    except KeyboardInterrupt:
        manifest["status"] = "incomplete"
        manifest["errors"].append("Ejecución interrumpida por el usuario.")
        manifest["counts"] = _counts(rows, len(tiles))
        write_json_atomic(paths.manifest, manifest)
        print("Ejecución interrumpida; el run puede reanudarse.")
        return 130
    except BaseException as exc:
        manifest["status"] = "failed"
        manifest["errors"].append(str(exc))
        manifest["counts"] = _counts(rows, len(tiles))
        write_json_atomic(paths.manifest, manifest)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera un dataset Sentinel-2 reproducible para un incendio y run."
    )
    parser.add_argument("--event", help="ID del incendio definido en config/incendios/.")
    parser.add_argument("--run", dest="run_id", help="ID inmutable de la ejecución.")
    parser.add_argument(
        "--project",
        help="Proyecto Google Cloud registrado para usar Earth Engine.",
    )
    parser.add_argument("--list-events", action="store_true", help="Listar eventos configurados y salir.")
    parser.add_argument("--dry-run", action="store_true", help="Validar y consultar escenas sin escribir archivos.")
    parser.add_argument(
        "--clear-incomplete", action="store_true",
        help="Eliminar solamente el run seleccionado si no está completado.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.list_events:
        for event in list_events():
            print(f"{event['event_id']}: {event['name']}")
        return 0
    if bool(args.event) != bool(args.run_id):
        raise ConfigError("--event y --run deben proporcionarse juntos.")
    event_id = args.event or DEFAULT_EVENT
    run_id = args.run_id or DEFAULT_RUN
    if args.clear_incomplete:
        return _clear_incomplete(event_id, run_id)
    return run_generation(event_id, run_id, dry_run=args.dry_run, project=args.project)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ConfigError, RuntimeError) as exc:
        raise SystemExit(f"Error: {exc}") from exc
