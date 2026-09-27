"""Explorador interactivo de tiles para un evento y run."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import rasterio

from dataset_runs import get_run_paths


BANDA_R = 2
BANDA_G = 1
BANDA_B = 0
GAMMA = 0.8

if "s" in plt.rcParams["keymap.save"]:
    plt.rcParams["keymap.save"].remove("s")


def cargar_rgb(path_tif: Path) -> np.ndarray:
    with rasterio.open(path_tif) as source:
        red = source.read(BANDA_R + 1).astype(float)
        green = source.read(BANDA_G + 1).astype(float)
        blue = source.read(BANDA_B + 1).astype(float)
    rgb = np.stack([red, green, blue], axis=-1)
    valid = rgb[rgb > 0]
    if valid.size == 0:
        return np.zeros_like(rgb)
    low, high = np.percentile(valid, (2, 98))
    rgb = np.clip((rgb - low) / max(high - low, 1e-9), 0, 1)
    return np.power(rgb, GAMMA)


def cargar_banda(path_tif: Path) -> np.ndarray:
    with rasterio.open(path_tif) as source:
        return source.read(1)


def dibujar(fig, axes, tile_id: str, paths) -> None:
    pre_path = paths.pre / f"{tile_id}.tif"
    post_path = paths.post / f"{tile_id}.tif"
    mask_path = paths.masks / f"{tile_id}.tif"
    valid_path = paths.valid / f"{tile_id}.tif"
    if not all(path.exists() for path in (pre_path, post_path, mask_path)):
        print(f"Advertencia: faltan archivos para {tile_id}")
        return

    pre = cargar_rgb(pre_path)
    post = cargar_rgb(post_path)
    mask = cargar_banda(mask_path)
    valid = cargar_banda(valid_path) if valid_path.exists() else np.ones(mask.shape, dtype=np.uint8)
    overlay = post.copy()
    burned = (mask == 1) & (valid == 1)
    overlay[burned, 0] = 1.0
    overlay[burned, 1] *= 0.3
    overlay[burned, 2] *= 0.3
    overlay[valid == 0] = overlay[valid == 0] * 0.25 + 0.55 * 0.75
    pct = burned.sum() / max((valid == 1).sum(), 1) * 100
    valid_pct = (valid == 1).mean() * 100

    for axis in axes:
        axis.clear()
    fig.suptitle(
        f"Tile: {tile_id} | Quemado válido: {pct:.1f}% | Cobertura válida: {valid_pct:.1f}%",
        fontsize=13,
    )
    axes[0].imshow(pre)
    axes[0].set_title("Antes del incendio")
    axes[1].imshow(post)
    axes[1].set_title("Después del incendio")
    mask_display = np.where(valid == 1, mask, np.nan)
    axes[2].imshow(mask_display, cmap="gray_r", vmin=0, vmax=1)
    axes[2].set_facecolor("0.65")
    axes[2].set_title("Máscara binaria")
    axes[2].legend(
        handles=[
            mpatches.Patch(color="black", label="Quemado (1)"),
            mpatches.Patch(color="white", label="No quemado (0)"),
            mpatches.Patch(color="0.65", label="Sin datos válidos"),
        ],
        loc="lower right",
        fontsize=8,
    )
    axes[3].imshow(overlay)
    axes[3].set_title("Superposición")
    for axis in axes:
        axis.axis("off")
    fig.canvas.draw_idle()


def crear_ruta_guardado(directory: Path, tile_id: str, suffix: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    counter = 1
    while True:
        output = directory / f"{tile_id}_{suffix}_{counter:02d}.png"
        if not output.exists():
            return output
        counter += 1


def explorar(tiles: list[Path], initial_index: int, paths) -> None:
    state = {"index": initial_index}
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    fig.text(
        0.5,
        0.01,
        "← → navegar | s guardar | t transparente | q salir",
        ha="center",
        fontsize=9,
        color="gray",
    )
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    dibujar(fig, axes, tiles[state["index"]].stem, paths)

    def on_key(event) -> None:
        if event.key == "right":
            state["index"] = (state["index"] + 1) % len(tiles)
        elif event.key == "left":
            state["index"] = (state["index"] - 1) % len(tiles)
        elif event.key in {"s", "t"}:
            tile_id = tiles[state["index"]].stem
            suffix = "transparente" if event.key == "t" else "visualizacion"
            output = crear_ruta_guardado(paths.tile_visualizations, tile_id, suffix)
            fig.savefig(
                output, dpi=150, bbox_inches="tight", transparent=event.key == "t"
            )
            print(f"Guardado: {output}")
            return
        elif event.key == "q":
            plt.close(fig)
            return
        else:
            return
        dibujar(fig, axes, tiles[state["index"]].stem, paths)

    fig.canvas.mpl_connect("key_press_event", on_key)
    plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Explora los tiles de un evento y run.")
    parser.add_argument("tile", nargs="?", help="Tile inicial, con o sin .tif.")
    parser.add_argument("--event", required=True)
    parser.add_argument("--run", dest="run_id", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = get_run_paths(args.event, args.run_id)
    tiles = sorted(paths.post.glob("*.tif"))
    if not tiles:
        print(f"No se encontraron tiles POST en {paths.post}")
        return 1
    stems = [tile.stem for tile in tiles]
    requested = (args.tile or "").removesuffix(".tif")
    index = stems.index(requested) if requested in stems else 0
    if requested and requested not in stems:
        print(f"Advertencia: {requested} no existe; se abre {stems[0]}.")
    else:
        print(f"Navegando desde {stems[index]} ({len(tiles)} tiles).")
    explorar(tiles, index, paths)
    return 0


if __name__ == "__main__":
    sys.exit(main())
