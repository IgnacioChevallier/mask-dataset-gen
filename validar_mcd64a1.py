"""Cruce de la máscara objetivo de un run con MODIS MCD64A1 (celdas de ~463 m).

Sólo lectura: no escribe nada en dataset/. Imprime un CSV con, por evento:

- modis_roi_ha: celdas MCD64A1 quemadas en los ROIs entre el fin del PRE y el
  inicio del POST (incluye incendios vecinos).
- modis_incendio_ha: de esas, las celdas que contienen algún píxel de la máscara.
- mascara_ha: área de la máscara objetivo.
- mascara_confirmada_pct: % de píxeles de la máscara que caen en celdas MODIS quemadas.

Uso: .venv/bin/python validar_mcd64a1.py epuyen-2019 los-alerces-2023:event-filter-002
(el run por defecto es event-filter-001).
"""

import datetime as dt
import glob
import math
import sys

import ee
import numpy as np
import rasterio

from dataset_runs import effective_config

# Grilla sinusoidal MODIS.
RADIO, CELDA = 6371007.181, 463.312716525
X0, Y0 = -20015109.354, 10007554.677
CELDA_HA = CELDA * CELDA / 1e4


def _celda(lon, lat):
    lat_r = np.radians(lat)
    x = RADIO * np.radians(lon) * np.cos(lat_r)
    y = RADIO * lat_r
    return np.floor((Y0 - y) / CELDA).astype(np.int64), np.floor((x - X0) / CELDA).astype(np.int64)


def _celdas_modis(coleccion, proyeccion, rois, inicio: str, fin: str) -> set[tuple[int, int]]:
    desde, hasta = dt.date.fromisoformat(inicio), dt.date.fromisoformat(fin)
    epoca = dt.date(1970, 1, 1)
    dia_desde, dia_hasta = (desde - epoca).days, (hasta - epoca).days

    def quemado(img):
        # BurnDate es el día del año; se lleva a días desde 1970 para cruzar años.
        anio = ee.Date.fromYMD(img.date().get("year"), 1, 1).millis().divide(864e5)
        burn = img.select("BurnDate")
        dia = burn.add(ee.Image.constant(anio)).subtract(1).updateMask(burn.gt(0)).toFloat()
        return dia.gte(dia_desde).And(dia.lte(dia_hasta)).selfMask().rename("b").toByte()

    quemada = (
        coleccion.filterDate(dt.date(desde.year, desde.month, 1).isoformat(), (hasta + dt.timedelta(days=1)).isoformat())
        .map(quemado)
        .max()
    )
    celdas = set()
    for roi in rois:
        muestras = quemada.sample(
            region=ee.Geometry.Rectangle(roi["bbox"]), projection=proyeccion, scale=CELDA, geometries=True
        )
        cantidad = muestras.size().getInfo()
        if cantidad >= 5000:
            raise RuntimeError(f"{cantidad} celdas en {roi['id']}: supera el límite de getInfo().")
        for feature in muestras.getInfo()["features"]:
            lon, lat = feature["geometry"]["coordinates"]
            fila, col = _celda(np.array(lon), np.array(lat))
            celdas.add((int(fila), int(col)))
    return celdas


def _pixeles_mascara(run_dir: str) -> tuple[np.ndarray, np.ndarray]:
    pixeles = {}  # clave por índice global: los tiles se solapan un píxel
    for ruta in sorted(glob.glob(f"{run_dir}/mascaras/*.tif")):
        with rasterio.open(ruta) as fuente:
            filas, cols = np.nonzero(fuente.read(1))
            if not len(filas):
                continue
            xs, ys = rasterio.transform.xy(fuente.transform, filas, cols)
            res = fuente.res[0]
            for lon, lat in zip(np.asarray(xs), np.asarray(ys)):
                pixeles[(math.floor(lon / res), math.floor(lat / res))] = (lon, lat)
    valores = np.array(list(pixeles.values()))
    return valores[:, 0], valores[:, 1]


def main(argumentos: list[str]) -> int:
    if not argumentos:
        print(__doc__)
        return 1
    ee.Initialize(project="ee-nachochevallier")
    coleccion = ee.ImageCollection("MODIS/061/MCD64A1")
    proyeccion = coleccion.first().projection()
    print("evento,run,ventana,modis_roi_ha,modis_incendio_ha,mascara_ha,mascara_confirmada_pct")
    for argumento in argumentos:
        evento, _, run = argumento.partition(":")
        run = run or "event-filter-001"
        config = effective_config(evento, run)
        ventanas = config["windows"]
        inicio = (dt.date.fromisoformat(ventanas["pre"]["end_inclusive"]) + dt.timedelta(days=1)).isoformat()
        fin = (dt.date.fromisoformat(ventanas["post"]["start"]) - dt.timedelta(days=1)).isoformat()
        quemadas = _celdas_modis(coleccion, proyeccion, config["rois"], inicio, fin)
        lon, lat = _pixeles_mascara(f"dataset/{evento}/runs/{run}")
        filas, cols = _celda(lon, lat)
        claves = list(zip(filas.tolist(), cols.tolist()))
        confirmados = np.fromiter((clave in quemadas for clave in claves), bool, len(claves))
        hectareas = (config["grid"]["scale_m"] ** 2 * np.cos(np.radians(lat)) / 1e4).sum()
        print(
            f"{evento},{run},{inicio}/{fin},{len(quemadas) * CELDA_HA:.0f},"
            f"{len(set(claves) & quemadas) * CELDA_HA:.0f},{hectareas:.0f},{100 * confirmados.mean():.1f}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
