# mask-dataset-gen

Generador reproducible de datasets de áreas quemadas a partir de Sentinel-2 y
Google Earth Engine. El sistema compara composiciones PRE y POST, calcula dNBR,
aplica filtros espectrales y exporta imágenes, máscaras, calidad y metadatos por
tile.

## Eventos configurados

```bash
python generar_dataset.py --list-events
```

Las configuraciones viven en `config/incendios/` y actualmente incluyen:

- `epuyen-2025`, con el run exploratorio `baseline-001`;
- `los-alerces-2023`, con el próximo caso de estudio `baseline-001`;
- `puerto-patriada-2026`, con `legacy-v1` y el futuro `baseline-002`.

## Estructura

```text
config/incendios/<evento>.json
dataset/<evento>/runs/<run>/
├── imagenes_pre/
├── imagenes_post/
├── mascaras/
├── calidad/observacion_valida/
├── visualizaciones/
├── metadata.csv
├── resumen.md
└── run.json
```

Cada run nuevo usa nombres deterministas como
`roi_01_r003_c004.tif`. Los resultados completos son inmutables y los runs
interrumpidos se pueden reanudar si su configuración no cambió.

## Instalación y autenticación

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
earthengine authenticate
```

Las credenciales de Earth Engine no se guardan en este repositorio.

## Preflight y generación

Consultar escenas, ROIs y tiles sin escribir archivos:

```bash
.venv/bin/python generar_dataset.py \
  --event epuyen-2025 \
  --run baseline-001 \
  --dry-run
```

Ejecutar o reanudar el run:

```bash
.venv/bin/python generar_dataset.py \
  --event epuyen-2025 \
  --run baseline-001
```

El run de Epuyén quedó completado. El siguiente caso preparado es Los Alerces
2023; antes de ejecutarlo se puede revisar su preflight sin escribir datos:

```bash
.venv/bin/python generar_dataset.py \
  --event los-alerces-2023 \
  --run baseline-001 \
  --dry-run
```

Las cuentas actuales de Earth Engine requieren un proyecto Google Cloud con la
API habilitada y registrado para uso de Earth Engine. Epuyén y Los Alerces usan
`ee-nachochevallier`; el proyecto efectivo se incluye en la configuración
sellada de `run.json`. `--project` permite reemplazarlo explícitamente al crear
otro run.

Un run incompleto se puede eliminar explícitamente:

```bash
.venv/bin/python generar_dataset.py \
  --event epuyen-2025 \
  --run baseline-001 \
  --clear-incomplete
```

El comando rechaza la limpieza de runs completados. El antiguo `--clear`
global ya no existe.

## Visualización

Generar los cuatro mosaicos resumen:

```bash
.venv/bin/python visualizar_roi.py \
  --event epuyen-2025 \
  --run baseline-001 \
  --all
```

Explorar tiles:

```bash
.venv/bin/python visualizar.py \
  --event epuyen-2025 \
  --run baseline-001
```

También se puede indicar un tile inicial como argumento posicional.

## Compatibilidad legacy

El dataset original está en:

```text
dataset/puerto-patriada-2026/runs/legacy-v1/
```

Las rutas antiguas bajo `dataset/` son enlaces simbólicos, por lo que siguen
funcionando:

```bash
python generar_dataset.py
python visualizar.py tile_000
python visualizar_roi.py
```

El generador sin argumentos detecta que `legacy-v1` ya está completo y no
duplica tiles.

## Algoritmo

La máscara base usa:

```text
NBR = (B8 - B12) / (B8 + B12)
dNBR = NBR_pre - NBR_post
```

Los umbrales exactos no se duplican en esta documentación: la fuente de verdad
es la configuración JSON y su copia sellada dentro de `run.json`. Además de la
máscara binaria, los runs nuevos exportan una capa que distingue los píxeles
con observación válida simultánea en PRE y POST.

## Trazabilidad y almacenamiento

`run.json` registra configuración, hash, escenas, entorno, estados, conteos y
métricas. `metadata.csv` agrega posición de grilla, cobertura válida, área
quemada y estado por tile.

Los GeoTIFFs de todos los runs, incluido `legacy-v1`, se conservan localmente
pero se ignoran en Git. Se versionan las configuraciones, los manifiestos, los
metadatos y la documentación. Las visualizaciones históricas livianas de
`legacy-v1` permanecen versionadas.

El plan y las decisiones de diseño están documentados en
[`PLAN_MULTI_INCENDIOS.md`](PLAN_MULTI_INCENDIOS.md).
