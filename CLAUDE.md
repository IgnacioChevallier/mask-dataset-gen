# mask-dataset-gen

Genera datasets de áreas quemadas (PRE/POST/máscara por tile) con Sentinel-2 o
Landsat 8 vía Google Earth Engine. Uso y algoritmo: `README.md`.

## Comandos

- Python: siempre `.venv/bin/python` (3.14).
- Tests (rápidos, sin red): `.venv/bin/python -m unittest discover -s tests`
- Listar eventos: `.venv/bin/python generar_dataset.py --list-events`
- Preflight sin escribir: `.venv/bin/python generar_dataset.py --event <e> --run <r> --dry-run`
- Baseline: `generar_dataset.py --event <e> --run <r>`; derivados `event-filter-*`: `filtrar_evento.py --event <e> --run <r>`.

## Reglas

- **Runs inmutables.** Un run con `status: completed` en su `run.json` no se
modifica ni se regenera. Un experimento nuevo es un run ID nuevo en
`config/incendios/<evento>.json`; nunca se editan los parámetros de un run existente.
- Nunca borrar nada bajo `dataset/`. `--clear-incomplete` sólo con pedido explícito.
- Los runs reales consumen cuota de Earth Engine y tardan: correr `--dry-run`
primero y pedir confirmación antes de una ejecución real.
- Proyecto Earth Engine: `ee-nachochevallier`. Las credenciales no van al repo.
- Fuente de verdad de umbrales: el JSON de config y su copia sellada en `run.json`,
no la documentación.
- Tras cambiar código o configs, correr los tests; `tests/test_dataset_runs.py`
valida todas las configs.
- Código, comentarios y docs en español. Sin dependencias nuevas sin motivo.



## Earth Engine: invariantes a preservar

- `scale` explícito en todo `reduceRegion`/`sample`/descarga; nunca `bestEffort=True` (degrada la resolución en silencio). Ante timeouts, subir `tileScale`.
- Enmascarar nubes (`SCL` / `QA_PIXEL`) antes de `median()`, no después.
- Landsat C2 L2: aplicar `*0.0000275 - 0.2` y llevar a 0–10000 (`_landsat_as_s2`) antes de usar umbrales S2.
- NBR usa B8 y **B12** (SWIR2), no B11.
- `.getInfo()` sólo para escalares o listas chicas; nada de `if`/`for` de Python sobre objetos `ee.*`.
- FeatureCollections que pueden superar 5000 elementos se descargan paginando (`_fetch_features` en `filtrar_evento.py`); `getInfo()` aborta por encima de ese límite.
- Un cambio de colección, máscara, reductor o escala es un run nuevo con otra `algorithm_version`.



## Runs vigentes

- El run a usar de cada evento está en la columna "Resultado" de la tabla de `README.md` (hoy siempre un `event-filter-*`); no duplicar esa lista acá.
- El dataset alimenta un modelo físico, no uno de aprendizaje automático: no hay particiones train/test.
- Resoluciones mezcladas a propósito: Landsat 8 (2015–2016) a 30 m, Sentinel-2 a 20 m, sin remuestreo.



## Mapa

- `dataset_runs.py`: carga/merge/validación de config, rutas, grilla de tiles, hash. Puro, testeable.
- `generar_dataset.py`: pipeline Earth Engine de baselines (dNBR + filtros espectrales).
- `filtrar_evento.py`: atribución de componentes al incendio con VIIRS.
- `visualizar.py`, `visualizar_roi.py`: exploración y mosaicos resumen.
- GeoTIFFs y visualizaciones están ignorados por Git; se versionan configs, `run.json`, CSVs y `resumen.md`.
- Los `event-filter-*` enlazan (hardlink) PRE, POST y validez del run padre; no reemplazar por copias.

