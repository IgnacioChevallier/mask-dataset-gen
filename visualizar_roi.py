"""Genera mosaicos de un run completo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.merge import merge

from dataset_runs import effective_config, get_run_paths


BANDA_R = 2
BANDA_G = 1
BANDA_B = 0
GAMMA = 0.8


def _common_tile_names(paths) -> list[str]:
    sets = [
        {path.stem for path in paths.pre.glob("*.tif")},
        {path.stem for path in paths.post.glob("*.tif")},
        {path.stem for path in paths.masks.glob("*.tif")},
        {path.stem for path in paths.valid.glob("*.tif")},
    ]
    common = sorted(set.intersection(*sets)) if all(sets) else []
    if not common:
        raise FileNotFoundError(f"No hay tiles con PRE, POST, máscara y validez en {paths.root}.")
    return common


def _merge_rasters(files: list[Path]) -> np.ndarray:
    datasets = [rasterio.open(path) for path in files]
    try:
        mosaic, _ = merge(datasets)
        return mosaic
    finally:
        for dataset in datasets:
            dataset.close()


def _normalize_rgb(mosaic: np.ndarray) -> np.ndarray:
    rgb = np.stack(
        [mosaic[BANDA_R], mosaic[BANDA_G], mosaic[BANDA_B]], axis=-1
    ).astype(np.float32)
    nodata = np.all(rgb == 0, axis=-1)
    values = rgb[np.isfinite(rgb) & (rgb > 0)]
    if values.size == 0:
        raise ValueError("El mosaico no contiene valores RGB positivos.")
    low, high = np.percentile(values, (2, 98))
    if high <= low:
        raise ValueError("No se pudo normalizar RGB: percentiles inválidos.")
    rgb = np.clip((rgb - low) / (high - low), 0, 1)
    rgb = np.power(rgb, GAMMA)
    rgb[nodata] = 1.0
    return rgb


def _save_rgb(image: np.ndarray, output: Path, title: str) -> None:
    fig, axis = plt.subplots(figsize=(12, 10))
    axis.imshow(image)
    axis.set_title(title)
    axis.axis("off")
    fig.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _save_mask(mask: np.ndarray, valid: np.ndarray, output: Path, title: str) -> None:
    display = np.zeros((*mask.shape, 3), dtype=np.float32)
    display[mask == 0] = (1.0, 1.0, 1.0)
    display[mask == 1] = (0.0, 0.0, 0.0)
    display[valid == 0] = (0.65, 0.65, 0.65)
    fig, axis = plt.subplots(figsize=(12, 10))
    axis.imshow(display)
    axis.set_title(title + " — gris: sin observación válida")
    axis.axis("off")
    fig.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _overlay(rgb: np.ndarray, mask: np.ndarray, valid: np.ndarray) -> np.ndarray:
    result = rgb.copy()
    burned = (mask == 1) & (valid == 1)
    result[burned, 0] = 1.0
    result[burned, 1] *= 0.3
    result[burned, 2] *= 0.3
    result[valid == 0] = result[valid == 0] * 0.25 + np.array([0.55, 0.55, 0.55]) * 0.75
    return result


def generar_resumen_run(paths, config: dict) -> list[Path]:
    """Genera PRE, POST, máscara y overlay; se usa también desde el generador."""
    names = _common_tile_names(paths)
    pre_mosaic = _merge_rasters([paths.pre / f"{name}.tif" for name in names])
    post_mosaic = _merge_rasters([paths.post / f"{name}.tif" for name in names])
    mask = np.squeeze(_merge_rasters([paths.masks / f"{name}.tif" for name in names]))

    valid = np.squeeze(_merge_rasters([paths.valid / f"{name}.tif" for name in names]))

    if pre_mosaic.shape[1:] != mask.shape or post_mosaic.shape[1:] != mask.shape:
        raise ValueError("Los mosaicos PRE, POST y máscara no tienen las mismas dimensiones.")
    if valid.shape != mask.shape:
        raise ValueError("El mosaico de observación válida no coincide con la máscara.")

    pre_rgb = _normalize_rgb(pre_mosaic)
    post_rgb = _normalize_rgb(post_mosaic)
    overlay = _overlay(post_rgb, mask, valid)
    title = f"{config['event_name']} — {config['run_id']}"
    paths.roi_summaries.mkdir(parents=True, exist_ok=True)
    outputs = [
        paths.roi_summaries / "01_pre.png",
        paths.roi_summaries / "02_post.png",
        paths.roi_summaries / "03_mascara.png",
        paths.roi_summaries / "04_superposicion.png",
    ]
    _save_rgb(pre_rgb, outputs[0], f"{title} — PRE")
    _save_rgb(post_rgb, outputs[1], f"{title} — POST")
    _save_mask(mask, valid, outputs[2], f"{title} — máscara binaria")
    burned_valid = (mask == 1) & (valid == 1)
    pct = burned_valid.sum() / max((valid == 1).sum(), 1) * 100
    _save_rgb(overlay, outputs[3], f"{title} — superposición ({pct:.2f}% del área válida)")
    for output in outputs:
        print(f"Guardado: {output}")
    return outputs


def _save_compat_view(paths, config: dict, use_pre: bool, no_mask: bool) -> Path:
    names = _common_tile_names(paths)
    source_dir = paths.pre if use_pre else paths.post
    mosaic = _merge_rasters([source_dir / f"{name}.tif" for name in names])
    rgb = _normalize_rgb(mosaic)
    epoch = "pre" if use_pre else "post"
    if not no_mask:
        mask = np.squeeze(_merge_rasters([paths.masks / f"{name}.tif" for name in names]))
        valid = np.squeeze(_merge_rasters([paths.valid / f"{name}.tif" for name in names]))
        rgb = _overlay(rgb, mask, valid)
    paths.roi_summaries.mkdir(parents=True, exist_ok=True)
    suffix = "" if no_mask else "_mascara"
    output = paths.roi_summaries / f"roi_{epoch}{suffix}.png"
    _save_rgb(rgb, output, f"{config['event_name']} — {config['run_id']} — {epoch.upper()}")
    print(f"Guardado: {output}")
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualiza el ROI de un evento y run.")
    parser.add_argument("--event", required=True)
    parser.add_argument("--run", dest="run_id", required=True)
    parser.add_argument("--prev", action="store_true", help="Usar PRE en lugar de POST.")
    parser.add_argument("--nomask", action="store_true", help="No superponer la máscara.")
    parser.add_argument(
        "--all", action="store_true", help="Generar PRE, POST, máscara y superposición."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = get_run_paths(args.event, args.run_id)
    config = effective_config(args.event, args.run_id)
    try:
        if args.all:
            generar_resumen_run(paths, config)
        else:
            _save_compat_view(paths, config, args.prev, args.nomask)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
