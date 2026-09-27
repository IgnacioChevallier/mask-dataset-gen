"""Deriva una máscara atribuida a un incendio desde un run espectral completo.

La clasificación conserva la máscara candidata del run padre, forma objetos
espaciales sobre el mosaico completo y usa detecciones térmicas para separar el
incendio objetivo, otros incendios probables y cambios no confirmados.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import platform
import shutil
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.warp import Resampling, reproject
from scipy.ndimage import binary_closing, label
from scipy.spatial import cKDTree

from dataset_runs import (
    ConfigError,
    config_hash,
    dependency_versions,
    effective_config,
    end_exclusive,
    get_run_paths,
    git_commit,
    read_json,
    utc_now,
    write_json_atomic,
)


EARTH_RADIUS_M = 6_371_008.8
CLASS_TARGET = "incendio_objetivo"
CLASS_OTHER = "otro_incendio_probable"
CLASS_UNCONFIRMED = "cambio_no_confirmado"


@dataclass(frozen=True)
class DerivedPaths:
    candidates: Path
    other_fire: Path
    unconfirmed: Path
    confidence: Path
    components: Path
    hotspots: Path
    comparison: Path


def _derived_paths(root: Path) -> DerivedPaths:
    return DerivedPaths(
        candidates=root / "candidatos_cambio",
        other_fire=root / "otro_incendio_probable",
        unconfirmed=root / "cambio_no_confirmado",
        confidence=root / "confianza_incendio",
        components=root / "componentes.csv",
        hotspots=root / "hotspots.csv",
        comparison=root / "visualizaciones" / "resumen_roi" / "05_comparacion_filtro.png",
    )


def _xy_m(longitude: float, latitude: float, reference_latitude: float) -> tuple[float, float]:
    return (
        math.radians(longitude) * EARTH_RADIUS_M * math.cos(math.radians(reference_latitude)),
        math.radians(latitude) * EARTH_RADIUS_M,
    )


def distance_m(
    first: tuple[float, float], second: tuple[float, float]
) -> float:
    """Distancia equirectangular local, adecuada para ROIs regionales pequeños."""
    reference_latitude = (first[1] + second[1]) / 2
    first_xy = _xy_m(first[0], first[1], reference_latitude)
    second_xy = _xy_m(second[0], second[1], reference_latitude)
    return math.hypot(first_xy[0] - second_xy[0], first_xy[1] - second_xy[1])


def cluster_detections(
    detections: list[dict[str, Any]], radius_m: float
) -> list[dict[str, Any]]:
    """Agrupa hotspots por proximidad y devuelve clústeres deterministas."""
    if not detections:
        return []
    reference_latitude = float(np.mean([item["latitude"] for item in detections]))
    points = np.asarray(
        [_xy_m(item["longitude"], item["latitude"], reference_latitude) for item in detections]
    )
    tree = cKDTree(points)
    parents = list(range(len(detections)))

    def find(index: int) -> int:
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(left: int, right: int) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parents[max(left_root, right_root)] = min(left_root, right_root)

    for left, right in tree.query_pairs(radius_m):
        union(left, right)

    members: dict[int, list[int]] = defaultdict(list)
    for index in range(len(detections)):
        members[find(index)].append(index)

    unsorted = []
    for indices in members.values():
        items = [detections[index] for index in indices]
        unsorted.append(
            {
                "members": items,
                "longitude": float(np.mean([item["longitude"] for item in items])),
                "latitude": float(np.mean([item["latitude"] for item in items])),
                "dates": sorted(
                    {
                        str(value)
                        for item in items
                        for value in (item["date"], item.get("last_date"))
                        if value
                    }
                ),
            }
        )
    unsorted.sort(key=lambda item: (item["latitude"], item["longitude"], item["dates"][0]))
    for index, cluster in enumerate(unsorted, start=1):
        cluster["id"] = f"thermal-{index:03d}"
        for member in cluster["members"]:
            member["cluster_id"] = cluster["id"]
    return unsorted


def choose_target_cluster(
    clusters: list[dict[str, Any]], ignition_point: tuple[float, float]
) -> dict[str, Any] | None:
    if not clusters:
        return None
    return min(
        clusters,
        key=lambda cluster: min(
            distance_m(
                ignition_point,
                (member["longitude"], member["latitude"]),
            )
            for member in cluster["members"]
        ),
    )


def classify_component(
    *,
    seed_distance_m: float,
    target_hotspot_distance_m: float,
    other_hotspot_distance_m: float,
    target_component_distance_m: float,
    parameters: dict[str, Any],
) -> tuple[str, str]:
    """Regla explícita de atribución, separada para poder probarla."""
    if seed_distance_m <= parameters["seed_max_distance_m"]:
        return CLASS_TARGET, "próximo a la semilla del evento"
    if target_hotspot_distance_m <= parameters["component_hotspot_max_distance_m"]:
        return CLASS_TARGET, "próximo al clúster térmico objetivo"
    if target_component_distance_m <= parameters["component_link_max_distance_m"]:
        return CLASS_TARGET, "fragmento próximo a un componente objetivo"
    if other_hotspot_distance_m <= parameters["component_hotspot_max_distance_m"]:
        return CLASS_OTHER, "próximo a un clúster térmico distinto"
    return CLASS_UNCONFIRMED, "sin continuidad ni evidencia térmica suficiente"


def _active_image(image, band: str, threshold: float):
    return image.select(band).gte(threshold).rename("active").selfMask()


def _fetch_features(collection) -> list[dict[str, Any]]:
    """Descarga una FeatureCollection paginando; getInfo() aborta con más de 5000 elementos."""
    import ee

    features: list[dict[str, Any]] = []
    params: dict[str, Any] = {"expression": collection, "pageSize": 5000}
    while True:
        page = ee.data.computeFeatures(params)
        features.extend(page.get("features", []))
        if not page.get("nextPageToken"):
            return features
        params["pageToken"] = page["nextPageToken"]


def query_thermal_detections(config: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    """Consulta todos los píxeles térmicos activos del período en una sola petición."""
    import ee

    thermal = config["event_filter"]["thermal"]
    geometries = [ee.Geometry.Rectangle(roi["bbox"]) for roi in config["rois"]]
    region = geometries[0]
    for geometry in geometries[1:]:
        region = region.union(geometry)
    collection = (
        ee.ImageCollection(thermal["collection"])
        .filterBounds(region)
        .filterDate(thermal["start"], end_exclusive(thermal["end_inclusive"]))
    )
    band = str(thermal["band"])
    threshold = float(thermal["threshold"])
    scale = int(thermal["scale_m"])

    def append_samples(image, accumulated):
        image = ee.Image(image)
        active = _active_image(image, band, threshold)
        samples = (
            active.addBands(ee.Image.pixelLonLat())
            .sample(region=region, scale=scale, geometries=False, tileScale=2)
            .map(
                lambda feature: ee.Feature(feature).set(
                    {
                        "date": ee.Date(image.get("system:time_start")).format("YYYY-MM-dd"),
                        "image_id": image.get("system:index"),
                    }
                )
            )
        )
        return ee.FeatureCollection(accumulated).merge(samples)

    sampling_mode = thermal.get("sampling_mode", "per-observation")
    if sampling_mode == "aggregate":
        start_date = ee.Date(thermal["start"])

        def encode_observation(image):
            image = ee.Image(image)
            active = _active_image(image, band, threshold)
            day_number = ee.Date(image.get("system:time_start")).difference(start_date, "day").round().add(1)
            day_band = ee.Image.constant(day_number).toFloat().rename("day").updateMask(active)
            # No usar unmask(0): VNP14A1 tiene footprints diarios distintos y
            # el unmask previo a la reducción puede eliminar el área útil.
            return active.toFloat().rename("active").addBands(day_band)

        encoded = collection.map(encode_observation)
        aggregate = (
            encoded.select("active").sum().rename("observation_count").selfMask()
            .addBands(encoded.select("day").min().rename("first_day"))
            .addBands(encoded.select("day").max().rename("last_day"))
            .addBands(ee.Image.pixelLonLat())
        )
        feature_collection = aggregate.sample(
            region=region, scale=scale, geometries=False, tileScale=2
        )
    elif sampling_mode == "per-observation":
        feature_collection = ee.FeatureCollection(
            collection.iterate(append_samples, ee.FeatureCollection([]))
        )
    else:
        raise ConfigError(f"sampling_mode térmico no soportado: {sampling_mode!r}")
    detections = []
    for feature in _fetch_features(feature_collection):
        properties = feature.get("properties", {})
        if sampling_mode == "aggregate":
            first_offset = int(round(float(properties["first_day"]))) - 1
            last_offset = int(round(float(properties["last_day"]))) - 1
            first_date = (date.fromisoformat(thermal["start"]) + timedelta(days=first_offset)).isoformat()
            last_date = (date.fromisoformat(thermal["start"]) + timedelta(days=last_offset)).isoformat()
            observation_count = int(round(float(properties["observation_count"])))
            image_id = ""
        else:
            first_date = properties["date"]
            last_date = properties["date"]
            observation_count = 1
            image_id = properties.get("image_id", "")
        detections.append(
            {
                "longitude": float(properties["longitude"]),
                "latitude": float(properties["latitude"]),
                "date": first_date,
                "last_date": last_date,
                "observation_count": observation_count,
                "image_id": image_id,
            }
        )
    detections.sort(key=lambda item: (item["date"], item["latitude"], item["longitude"]))
    image_ids = collection.aggregate_array("system:index").getInfo()
    return detections, image_ids


def _read_mosaic(files: Iterable[Path]) -> tuple[np.ndarray, Any, Any]:
    datasets = [rasterio.open(path) for path in files]
    if not datasets:
        raise FileNotFoundError("No hay rásteres para formar el mosaico.")
    try:
        mosaic, transform = merge(datasets)
        return mosaic, transform, datasets[0].crs
    finally:
        for dataset in datasets:
            dataset.close()


def _pixel_dimensions_m(transform, latitude: float) -> tuple[float, float]:
    x_m = abs(math.radians(transform.a) * EARTH_RADIUS_M * math.cos(math.radians(latitude)))
    y_m = abs(math.radians(transform.e) * EARTH_RADIUS_M)
    return x_m, y_m


def _closing_structure(radius_m: float, x_m: float, y_m: float) -> np.ndarray:
    x_radius = max(1, math.ceil(radius_m / x_m))
    y_radius = max(1, math.ceil(radius_m / y_m))
    yy, xx = np.ogrid[-y_radius : y_radius + 1, -x_radius : x_radius + 1]
    return ((xx * x_m) ** 2 + (yy * y_m) ** 2 <= radius_m**2)


def _row_pixel_areas(shape: tuple[int, int], transform) -> np.ndarray:
    rows = np.arange(shape[0], dtype=np.float64)
    latitudes = transform.f + (rows + 0.5) * transform.e
    width = abs(math.radians(transform.a)) * EARTH_RADIUS_M * np.cos(np.radians(latitudes))
    height = abs(math.radians(transform.e)) * EARTH_RADIUS_M
    return width * height


def _coordinates_for_indices(rows: np.ndarray, cols: np.ndarray, transform) -> tuple[np.ndarray, np.ndarray]:
    longitudes = transform.c + (cols.astype(np.float64) + 0.5) * transform.a
    latitudes = transform.f + (rows.astype(np.float64) + 0.5) * transform.e
    return longitudes, latitudes


def _tree_for_pixels(rows: np.ndarray, cols: np.ndarray, transform, reference_latitude: float) -> cKDTree:
    longitudes, latitudes = _coordinates_for_indices(rows, cols, transform)
    points = np.column_stack(
        (
            np.radians(longitudes) * EARTH_RADIUS_M * math.cos(math.radians(reference_latitude)),
            np.radians(latitudes) * EARTH_RADIUS_M,
        )
    )
    return cKDTree(points)


def _minimum_tree_distance(tree: cKDTree, points: list[dict[str, Any]], reference_latitude: float) -> float:
    if not points:
        return math.inf
    coordinates = np.asarray(
        [_xy_m(item["longitude"], item["latitude"], reference_latitude) for item in points]
    )
    distances, _ = tree.query(coordinates, k=1)
    return float(np.min(distances))


def _nearby_hotspots(
    tree: cKDTree,
    points: list[dict[str, Any]],
    reference_latitude: float,
    threshold_m: float,
) -> list[dict[str, Any]]:
    if not points:
        return []
    coordinates = np.asarray(
        [_xy_m(item["longitude"], item["latitude"], reference_latitude) for item in points]
    )
    distances, _ = tree.query(coordinates, k=1)
    return [point for point, distance in zip(points, distances, strict=True) if distance <= threshold_m]


def classify_components(
    candidate: np.ndarray,
    transform,
    detections: list[dict[str, Any]],
    target_cluster_id: str | None,
    config: dict[str, Any],
) -> tuple[dict[str, np.ndarray], list[dict[str, Any]]]:
    """Clasifica objetos globalmente para evitar cortes artificiales entre tiles."""
    parameters = config["event_filter"]
    ignition = parameters["ignition_point"]
    seed = (float(ignition["longitude"]), float(ignition["latitude"]))
    reference_latitude = float(np.mean([roi["bbox"][1] + roi["bbox"][3] for roi in config["rois"]]) / 2)
    x_m, y_m = _pixel_dimensions_m(transform, reference_latitude)
    structure = _closing_structure(float(parameters["closing_radius_m"]), x_m, y_m)
    object_mask = binary_closing(candidate, structure=structure) | candidate
    labels, component_count = label(object_mask, structure=np.ones((3, 3), dtype=np.uint8))
    pixel_areas = _row_pixel_areas(candidate.shape, transform)

    target_hotspots = [item for item in detections if item.get("cluster_id") == target_cluster_id]
    other_hotspots = [item for item in detections if item.get("cluster_id") != target_cluster_id]
    records: list[dict[str, Any]] = []
    component_trees: dict[int, cKDTree] = {}

    for component_id in range(1, component_count + 1):
        rows, cols = np.where((labels == component_id) & candidate)
        if rows.size == 0:
            continue
        tree = _tree_for_pixels(rows, cols, transform, reference_latitude)
        component_trees[component_id] = tree
        longitudes, latitudes = _coordinates_for_indices(rows, cols, transform)
        seed_xy = np.asarray([_xy_m(seed[0], seed[1], reference_latitude)])
        seed_distance = float(tree.query(seed_xy, k=1)[0][0])
        target_distance = _minimum_tree_distance(tree, target_hotspots, reference_latitude)
        other_distance = _minimum_tree_distance(tree, other_hotspots, reference_latitude)
        near_target = _nearby_hotspots(
            tree,
            target_hotspots,
            reference_latitude,
            float(parameters["component_hotspot_max_distance_m"]),
        )
        near_other = _nearby_hotspots(
            tree,
            other_hotspots,
            reference_latitude,
            float(parameters["component_hotspot_max_distance_m"]),
        )
        area_m2 = float(np.sum(pixel_areas[rows]))
        records.append(
            {
                "numeric_id": component_id,
                "component_id": f"component-{component_id:03d}",
                "pixel_count": int(rows.size),
                "area_ha": area_m2 / 10_000,
                "centroid_longitude": float(np.mean(longitudes)),
                "centroid_latitude": float(np.mean(latitudes)),
                "west": float(np.min(longitudes)),
                "south": float(np.min(latitudes)),
                "east": float(np.max(longitudes)),
                "north": float(np.max(latitudes)),
                "seed_distance_m": seed_distance,
                "target_hotspot_distance_m": target_distance,
                "other_hotspot_distance_m": other_distance,
                "target_hotspot_count": len(near_target),
                "other_hotspot_count": len(near_other),
                "target_hotspot_dates": sorted(
                    {value for item in near_target for value in (item["date"], item.get("last_date")) if value}
                ),
                "other_hotspot_dates": sorted(
                    {value for item in near_other for value in (item["date"], item.get("last_date")) if value}
                ),
                "class": None,
                "reason": None,
                "confidence": 0,
                "target_component_distance_m": math.inf,
            }
        )

    # Primera pasada: evidencia directa de semilla o clúster térmico objetivo.
    direct_target_ids: set[int] = set()
    for record in records:
        classification, reason = classify_component(
            seed_distance_m=record["seed_distance_m"],
            target_hotspot_distance_m=record["target_hotspot_distance_m"],
            other_hotspot_distance_m=math.inf,
            target_component_distance_m=math.inf,
            parameters=parameters,
        )
        if classification == CLASS_TARGET:
            record["class"], record["reason"] = classification, reason
            direct_target_ids.add(record["numeric_id"])

    if not direct_target_ids and records:
        closest = min(records, key=lambda item: item["seed_distance_m"])
        closest["class"] = CLASS_TARGET
        closest["reason"] = "respaldo: componente más próximo a la semilla sin hotspots disponibles"
        direct_target_ids.add(closest["numeric_id"])

    target_rows, target_cols = np.where(np.isin(labels, list(direct_target_ids)) & candidate)
    target_tree = (
        _tree_for_pixels(target_rows, target_cols, transform, reference_latitude)
        if target_rows.size
        else None
    )

    # Segunda pasada: continuidad con el objetivo y luego evidencia de otro fuego.
    for record in records:
        if record["class"] == CLASS_TARGET:
            continue
        tree = component_trees[record["numeric_id"]]
        if target_tree is None:
            link_distance = math.inf
        else:
            component_points = tree.data
            distances, _ = target_tree.query(component_points, k=1)
            link_distance = float(np.min(distances))
        record["target_component_distance_m"] = link_distance
        classification, reason = classify_component(
            seed_distance_m=math.inf,
            target_hotspot_distance_m=record["target_hotspot_distance_m"],
            other_hotspot_distance_m=record["other_hotspot_distance_m"],
            target_component_distance_m=link_distance,
            parameters=parameters,
        )
        record["class"], record["reason"] = classification, reason

    layers = {
        CLASS_TARGET: np.zeros(candidate.shape, dtype=np.uint8),
        CLASS_OTHER: np.zeros(candidate.shape, dtype=np.uint8),
        CLASS_UNCONFIRMED: np.zeros(candidate.shape, dtype=np.uint8),
        "confidence": np.zeros(candidate.shape, dtype=np.uint8),
    }
    hotspot_limit = max(float(parameters["component_hotspot_max_distance_m"]), 1.0)
    seed_limit = max(float(parameters["seed_max_distance_m"]), 1.0)
    for record in records:
        pixels = (labels == record["numeric_id"]) & candidate
        layers[record["class"]][pixels] = 1
        target_score = max(0.0, 1.0 - record["target_hotspot_distance_m"] / (2 * hotspot_limit))
        seed_score = max(0.0, 1.0 - record["seed_distance_m"] / (2 * seed_limit))
        if record["class"] == CLASS_TARGET:
            confidence = round(70 + 20 * target_score + 10 * seed_score)
        elif record["class"] == CLASS_OTHER:
            confidence = 35
        else:
            confidence = 10
        record["confidence"] = int(min(100, max(0, confidence)))
        layers["confidence"][pixels] = record["confidence"]
    return layers, records


def _copy_parent_inputs(parent, destination) -> None:
    # Hardlinks: los runs completos son inmutables, así que compartir el archivo no ocupa disco extra.
    for source_dir, destination_dir in (
        (parent.pre, destination.pre),
        (parent.post, destination.post),
        (parent.valid, destination.valid),
    ):
        destination_dir.mkdir(parents=True, exist_ok=True)
        for source in sorted(source_dir.glob("*.tif")):
            os.link(source, destination_dir / source.name)


def _write_mosaic_as_tiles(
    array: np.ndarray,
    source_transform,
    source_crs,
    references: list[Path],
    destination: Path,
) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for reference in references:
        with rasterio.open(reference) as source:
            profile = source.profile.copy()
            output = np.zeros((source.height, source.width), dtype=np.uint8)
            reproject(
                source=array,
                destination=output,
                src_transform=source_transform,
                src_crs=source_crs,
                dst_transform=source.transform,
                dst_crs=source.crs,
                resampling=Resampling.nearest,
            )
            profile.update(count=1, dtype="uint8", nodata=0, compress="deflate")
        target = destination / reference.name
        temporary = target.with_name(f".{target.stem}.part.tif")
        with rasterio.open(temporary, "w", **profile) as sink:
            sink.write(output, 1)
        os.replace(temporary, target)


def _area_hectares(mask: np.ndarray, transform) -> float:
    rows, _ = np.where(mask)
    if not rows.size:
        return 0.0
    return float(np.sum(_row_pixel_areas(mask.shape, transform)[rows]) / 10_000)


def _tile_metrics(mask_path: Path, valid_path: Path, extra_paths: dict[str, Path]) -> dict[str, float]:
    with rasterio.open(mask_path) as mask_source, rasterio.open(valid_path) as valid_source:
        mask = mask_source.read(1) == 1
        valid = valid_source.read(1) == 1
        transform = mask_source.transform
    valid_count = int(valid.sum())
    result = {
        "pct_quemado_valido": (float((mask & valid).sum()) / max(valid_count, 1)) * 100,
        "pct_observacion_valida": float(valid.mean()) * 100,
        "hectareas_quemadas": _area_hectares(mask & valid, transform),
        "valid_pixels": valid_count,
        "target_pixels": int((mask & valid).sum()),
    }
    for label_name, path in extra_paths.items():
        with rasterio.open(path) as source:
            layer = source.read(1) == 1
        result[f"hectareas_{label_name}"] = _area_hectares(layer & valid, transform)
        result[f"pixels_{label_name}"] = int((layer & valid).sum())
    return result


def _write_metadata(parent_metadata: Path, paths, derived: DerivedPaths) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    with parent_metadata.open(newline="", encoding="utf-8") as handle:
        parent_rows = list(csv.DictReader(handle))
    rows = []
    totals: dict[str, float] = defaultdict(float)
    for parent_row in parent_rows:
        name = f"{parent_row['tile']}.tif"
        metrics = _tile_metrics(
            paths.masks / name,
            paths.valid / name,
            {
                "candidatas": derived.candidates / name,
                "otro_incendio": derived.other_fire / name,
                "no_confirmadas": derived.unconfirmed / name,
            },
        )
        row = dict(parent_row)
        row["run_id"] = paths.run_id
        for field in (
            "pct_quemado_valido",
            "pct_observacion_valida",
            "hectareas_quemadas",
            "hectareas_candidatas",
            "hectareas_otro_incendio",
            "hectareas_no_confirmadas",
        ):
            row[field] = round(float(metrics[field]), 4)
        rows.append(row)
        for key, value in metrics.items():
            totals[key] += value
    fields = list(parent_rows[0].keys()) + [
        "hectareas_candidatas",
        "hectareas_otro_incendio",
        "hectareas_no_confirmadas",
    ]
    fd, temporary_name = tempfile.mkstemp(prefix=".metadata.", suffix=".csv", dir=paths.root)
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        os.replace(temporary_name, paths.metadata)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise
    total_valid = max(totals["valid_pixels"], 1)
    summary = {
        "burned_hectares": round(totals["hectareas_quemadas"], 4),
        "candidate_hectares": round(totals["hectareas_candidatas"], 4),
        "other_fire_hectares": round(totals["hectareas_otro_incendio"], 4),
        "unconfirmed_hectares": round(totals["hectareas_no_confirmadas"], 4),
        "burned_valid_pct": round(totals["target_pixels"] / total_valid * 100, 4),
    }
    return rows, summary


def _write_components(path: Path, records: list[dict[str, Any]]) -> None:
    fields = [
        "component_id", "class", "reason", "confidence", "pixel_count", "area_ha",
        "centroid_longitude", "centroid_latitude", "west", "south", "east", "north",
        "seed_distance_m", "target_hotspot_distance_m", "other_hotspot_distance_m",
        "target_component_distance_m", "target_hotspot_count", "other_hotspot_count",
        "target_hotspot_dates", "other_hotspot_dates",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for record in records:
            row = {field: record.get(field, "") for field in fields}
            for field in ("area_ha", "seed_distance_m", "target_hotspot_distance_m", "other_hotspot_distance_m", "target_component_distance_m"):
                value = row[field]
                row[field] = "" if not math.isfinite(float(value)) else round(float(value), 2)
            row["target_hotspot_dates"] = "|".join(record["target_hotspot_dates"])
            row["other_hotspot_dates"] = "|".join(record["other_hotspot_dates"])
            writer.writerow(row)


def _write_hotspots(path: Path, detections: list[dict[str, Any]], target_cluster_id: str | None) -> None:
    fields = [
        "date", "last_date", "observation_count", "longitude", "latitude",
        "image_id", "cluster_id", "is_target_cluster",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for item in detections:
            writer.writerow(
                {
                    **{field: item.get(field, "") for field in fields[:-1]},
                    "is_target_cluster": item.get("cluster_id") == target_cluster_id,
                }
            )


def _save_comparison(paths, derived: DerivedPaths, config: dict[str, Any], detections: list[dict[str, Any]], target_cluster_id: str | None) -> None:
    import matplotlib.pyplot as plt

    from visualizar_roi import _merge_rasters, _normalize_rgb, _overlay

    names = sorted(path.stem for path in paths.masks.glob("*.tif"))
    post = _normalize_rgb(_merge_rasters([paths.post / f"{name}.tif" for name in names]))
    valid = np.squeeze(_merge_rasters([paths.valid / f"{name}.tif" for name in names]))
    target = np.squeeze(_merge_rasters([paths.masks / f"{name}.tif" for name in names]))
    candidates = np.squeeze(_merge_rasters([derived.candidates / f"{name}.tif" for name in names]))
    other = np.squeeze(_merge_rasters([derived.other_fire / f"{name}.tif" for name in names]))
    unconfirmed = np.squeeze(_merge_rasters([derived.unconfirmed / f"{name}.tif" for name in names]))
    _, transform, _ = _read_mosaic([paths.masks / f"{name}.tif" for name in names])

    rejected = post.copy()
    rejected[other == 1] = (1.0, 0.55, 0.0)
    rejected[unconfirmed == 1] = (0.0, 0.85, 1.0)
    classified = post.copy()
    classified[target == 1] = (1.0, 0.05, 0.05)
    classified[other == 1] = (1.0, 0.55, 0.0)
    classified[unconfirmed == 1] = (0.0, 0.85, 1.0)
    classified[valid == 0] *= 0.4

    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    axes[0, 0].imshow(_overlay(post, candidates, valid))
    axes[0, 0].set_title("Candidatos del baseline")
    axes[0, 1].imshow(_overlay(post, target, valid))
    axes[0, 1].set_title("Incendio objetivo")
    axes[1, 0].imshow(rejected)
    axes[1, 0].set_title("Rechazados: naranja=otro fuego, celeste=no confirmado")
    axes[1, 1].imshow(classified)
    axes[1, 1].set_title("Clasificación y evidencia térmica")
    for item in detections:
        col = (item["longitude"] - transform.c) / transform.a
        row = (item["latitude"] - transform.f) / transform.e
        if item.get("cluster_id") == target_cluster_id:
            axes[1, 1].scatter(col, row, s=8, c="yellow", marker="o", alpha=0.55)
        else:
            axes[1, 1].scatter(col, row, s=10, c="magenta", marker="x", alpha=0.7)
    ignition = config["event_filter"]["ignition_point"]
    seed_col = (ignition["longitude"] - transform.c) / transform.a
    seed_row = (ignition["latitude"] - transform.f) / transform.e
    axes[1, 1].scatter(seed_col, seed_row, s=90, c="white", marker="*", edgecolors="black")
    for axis in axes.ravel():
        axis.axis("off")
    fig.suptitle(f"{config['event_name']} — {config['run_id']} — auditoría del filtro")
    fig.tight_layout()
    derived.comparison.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(derived.comparison, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _write_summary(config: dict[str, Any], manifest: dict[str, Any], records: list[dict[str, Any]], path: Path) -> None:
    metrics = manifest["metrics"]
    comparison = manifest["comparison_to_parent"]
    class_counts = defaultdict(int)
    for record in records:
        class_counts[record["class"]] += 1
    lines = [
        f"# Resumen: {config['event_name']} / {config['run_id']}",
        "",
        f"- Estado: `{manifest['status']}`",
        f"- Algoritmo: `{config['algorithm_version']}`",
        f"- Run padre: `{config['parent_run']}`",
        f"- Candidatos del baseline: {metrics['candidate_hectares']:.2f} ha",
        f"- Incendio objetivo: {metrics['burned_hectares']:.2f} ha",
        f"- Otro incendio probable: {metrics['other_fire_hectares']:.2f} ha",
        f"- Cambio no confirmado: {metrics['unconfirmed_hectares']:.2f} ha",
        f"- Candidatos conservados: {comparison['retained_candidate_pct']:.2f}%",
        f"- Componentes: {len(records)} ({class_counts[CLASS_TARGET]} objetivo, "
        f"{class_counts[CLASS_OTHER]} otro fuego, {class_counts[CLASS_UNCONFIRMED]} no confirmados)",
        f"- Detecciones térmicas: {manifest['thermal_evidence']['detection_count']}",
        f"- Clústeres térmicos: {manifest['thermal_evidence']['cluster_count']}",
        "",
    ]
    reference_area = config.get("reference", {}).get("burned_area_ha")
    if reference_area:
        difference = metrics["burned_hectares"] - float(reference_area)
        lines.extend(
            [
                f"- Superficie oficial de referencia: {float(reference_area):.2f} ha",
                f"- Diferencia exploratoria: {difference:+.2f} ha",
                "",
            ]
        )
    lines.extend(
        [
            "## Componentes",
            "",
            "| ID | Clase | Área | Dist. hotspot objetivo | Motivo |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for record in sorted(records, key=lambda item: item["area_ha"], reverse=True):
        hotspot_distance = record["target_hotspot_distance_m"]
        formatted_distance = "sin detecciones" if not math.isfinite(hotspot_distance) else f"{hotspot_distance:.0f} m"
        lines.append(
            f"| `{record['component_id']}` | `{record['class']}` | {record['area_ha']:.2f} ha | "
            f"{formatted_distance} | {record['reason']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretación",
            "",
            "El filtro atribuye objetos mediante reglas explícitas de proximidad a la semilla, "
            "detecciones térmicas y continuidad espacial. La ausencia de un hotspot no demuestra "
            "ausencia de fuego; las clases rechazadas se conservan para auditoría.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _validate_outputs(paths, derived: DerivedPaths, references: list[Path]) -> list[str]:
    errors = []
    directories = [paths.masks, derived.candidates, derived.other_fire, derived.unconfirmed, derived.confidence]
    for reference in references:
        expected_shape = None
        expected_transform = None
        for directory in directories:
            path = directory / reference.name
            if not path.is_file():
                errors.append(f"Falta {path}")
                continue
            with rasterio.open(path) as source:
                if expected_shape is None:
                    expected_shape = source.shape
                    expected_transform = source.transform
                elif source.shape != expected_shape or not source.transform.almost_equals(expected_transform):
                    errors.append(f"Geometría incompatible en {path}")
                values = np.unique(source.read(1))
                if directory != derived.confidence and not set(values.tolist()).issubset({0, 1}):
                    errors.append(f"Capa no binaria en {path}: {values.tolist()}")
        layer_arrays = []
        for directory in (derived.candidates, paths.masks, derived.other_fire, derived.unconfirmed):
            with rasterio.open(directory / reference.name) as source:
                layer_arrays.append(source.read(1))
        candidates, target, other, unconfirmed = layer_arrays
        class_sum = target + other + unconfirmed
        if np.any(class_sum > 1):
            errors.append(f"Clases superpuestas en {reference.name}")
        if not np.array_equal(class_sum, candidates):
            errors.append(f"Las clases no particionan los candidatos en {reference.name}")
        with rasterio.open(derived.confidence / reference.name) as source:
            confidence = source.read(1)
        if confidence.max(initial=0) > 100:
            errors.append(f"Confianza fuera de rango en {reference.name}")
    return errors


def run_event_filter(event_id: str, run_id: str) -> int:
    import ee

    config = effective_config(event_id, run_id)
    if not config["algorithm_version"].startswith("event-filter-"):
        raise RuntimeError("El run seleccionado no usa un algoritmo event-filter.")
    parent_run = config["parent_run"]
    parent_paths = get_run_paths(event_id, parent_run)
    paths = get_run_paths(event_id, run_id)
    derived = _derived_paths(paths.root)
    hash_value = config_hash(config)

    if not parent_paths.manifest.is_file():
        raise RuntimeError(f"No existe el manifiesto del run padre: {parent_paths.manifest}")
    parent_manifest = read_json(parent_paths.manifest)
    if parent_manifest.get("status") != "completed":
        raise RuntimeError("El run padre debe estar completo antes de derivar una máscara.")
    if paths.manifest.is_file():
        existing = read_json(paths.manifest)
        if existing.get("configuration_hash") != hash_value:
            raise RuntimeError("La configuración no coincide con el run derivado existente.")
        if existing.get("status") == "completed":
            print(f"El run ya está completo e inmutable: {paths.root}")
            return 0
        raise RuntimeError("El run derivado existe pero está incompleto; usá --clear-incomplete.")
    if paths.root.exists() and any(paths.root.iterdir()):
        raise RuntimeError("El destino existe sin manifiesto; no se sobrescribirá.")

    paths.create()
    for directory in (derived.candidates, derived.other_fire, derived.unconfirmed, derived.confidence):
        directory.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "event_id": event_id,
        "run_id": run_id,
        "origin": "derived",
        "parent_run": parent_run,
        "parent_configuration_hash": parent_manifest.get("configuration_hash"),
        "status": "running",
        "created_at": utc_now(),
        "completed_at": None,
        "configuration_hash": hash_value,
        "configuration": config,
        "environment": {
            "git_commit": git_commit(),
            "python": platform.python_version(),
            "dependencies": dependency_versions(),
        },
        "errors": [],
        "validation_errors": [],
    }
    write_json_atomic(paths.manifest, manifest)

    try:
        project = config["source"].get("project")
        ee.Initialize(project=project) if project else ee.Initialize()
        print("Consultando evidencia térmica...", flush=True)
        detections, thermal_images = query_thermal_detections(config)
        if not detections and not config["event_filter"].get("allow_empty_thermal", False):
            raise RuntimeError(
                "La fuente térmica no devolvió detecciones. Para usar el respaldo basado sólo "
                "en la semilla se debe declarar allow_empty_thermal=true explícitamente."
            )
        clusters = cluster_detections(
            detections, float(config["event_filter"]["thermal_cluster_radius_m"])
        )
        ignition = config["event_filter"]["ignition_point"]
        target_cluster = choose_target_cluster(
            clusters, (float(ignition["longitude"]), float(ignition["latitude"]))
        )
        target_cluster_id = target_cluster["id"] if target_cluster else None
        detection_count = sum(int(item.get("observation_count", 1)) for item in detections)
        print(
            f"Evidencia térmica: {detection_count} observaciones en {len(detections)} píxeles, "
            f"{len(clusters)} clústeres; "
            f"objetivo={target_cluster_id or 'sin detecciones'}",
            flush=True,
        )

        references = sorted(parent_paths.masks.glob("*.tif"))
        if not references:
            raise FileNotFoundError("El run padre no contiene máscaras candidatas.")
        candidate_mosaic, transform, crs = _read_mosaic(references)
        candidate = candidate_mosaic[0] == 1
        layers, components = classify_components(
            candidate, transform, detections, target_cluster_id, config
        )
        print(f"Clasificados {len(components)} componentes espaciales.", flush=True)

        _copy_parent_inputs(parent_paths, paths)
        _write_mosaic_as_tiles(candidate.astype(np.uint8), transform, crs, references, derived.candidates)
        _write_mosaic_as_tiles(layers[CLASS_TARGET], transform, crs, references, paths.masks)
        _write_mosaic_as_tiles(layers[CLASS_OTHER], transform, crs, references, derived.other_fire)
        _write_mosaic_as_tiles(layers[CLASS_UNCONFIRMED], transform, crs, references, derived.unconfirmed)
        _write_mosaic_as_tiles(layers["confidence"], transform, crs, references, derived.confidence)
        rows, metrics = _write_metadata(parent_paths.metadata, paths, derived)
        _write_components(derived.components, components)
        _write_hotspots(derived.hotspots, detections, target_cluster_id)

        manifest["counts"] = {
            "expected": len(references),
            "ok": sum(row["status"] == "ok" for row in rows),
            "warning": sum(row["status"] == "warning" for row in rows),
            "error": sum(row["status"] == "error" for row in rows),
        }
        manifest["metrics"] = metrics
        parent_area = float(parent_manifest.get("metrics", {}).get("total", {}).get("burned_hectares", 0))
        candidate_area = metrics["candidate_hectares"]
        manifest["comparison_to_parent"] = {
            "parent_reported_hectares": parent_area,
            "candidate_local_hectares": candidate_area,
            "target_hectares": metrics["burned_hectares"],
            "removed_hectares": round(candidate_area - metrics["burned_hectares"], 4),
            "retained_candidate_pct": round(
                metrics["burned_hectares"] / max(candidate_area, 1e-9) * 100, 4
            ),
        }
        manifest["thermal_evidence"] = {
            "collection": config["event_filter"]["thermal"]["collection"],
            "image_count": len(thermal_images),
            "images": thermal_images,
            "detection_count": detection_count,
            "unique_pixel_count": len(detections),
            "cluster_count": len(clusters),
            "target_cluster_id": target_cluster_id,
            "clusters": [
                {
                    "id": cluster["id"],
                    "longitude": round(cluster["longitude"], 6),
                    "latitude": round(cluster["latitude"], 6),
                    "detection_count": len(cluster["members"]),
                    "dates": cluster["dates"],
                }
                for cluster in clusters
            ],
        }
        validation_errors = _validate_outputs(paths, derived, references)
        manifest["validation_errors"] = validation_errors
        if validation_errors or manifest["counts"]["error"]:
            manifest["status"] = "incomplete"
            write_json_atomic(paths.manifest, manifest)
            raise RuntimeError(f"Run derivado incompleto: {len(validation_errors)} errores.")

        from visualizar_roi import generar_resumen_run

        generar_resumen_run(paths, config)
        _save_comparison(paths, derived, config, detections, target_cluster_id)
        manifest["status"] = "completed"
        manifest["completed_at"] = utc_now()
        _write_summary(config, manifest, components, paths.summary)
        write_json_atomic(paths.manifest, manifest)
        print(f"Run completado: {paths.root}")
        return 0
    except BaseException as exc:
        manifest["status"] = "failed"
        manifest["errors"].append(str(exc))
        write_json_atomic(paths.manifest, manifest)
        raise


def _clear_incomplete(event_id: str, run_id: str) -> int:
    paths = get_run_paths(event_id, run_id)
    if not paths.root.exists():
        print(f"No existe el run: {paths.root}")
        return 0
    if not paths.manifest.is_file():
        raise RuntimeError("Se rechaza limpiar un directorio sin run.json.")
    manifest = read_json(paths.manifest)
    if manifest.get("status") == "completed":
        raise RuntimeError("Se rechaza limpiar un run completado e inmutable.")
    shutil.rmtree(paths.root)
    print(f"Run derivado incompleto eliminado: {paths.root}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Atribuye componentes de cambio a un incendio.")
    parser.add_argument("--event", required=True)
    parser.add_argument("--run", dest="run_id", required=True)
    parser.add_argument("--clear-incomplete", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.clear_incomplete:
        return _clear_incomplete(args.event, args.run_id)
    return run_event_filter(args.event, args.run_id)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ConfigError, RuntimeError, FileNotFoundError) as exc:
        raise SystemExit(f"Error: {exc}") from exc
