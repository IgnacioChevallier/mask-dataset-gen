# mask-dataset-gen

Generador reproducible de datasets de áreas quemadas a partir de Sentinel-2 o Landsat 8 y Google Earth Engine. El sistema compara composiciones PRE y POST, calcula dNBR, aplica filtros espectrales y exporta imágenes, máscaras, calidad y metadatos por tile.

## Eventos configurados

```bash
python generar_dataset.py --list-events
```

Las configuraciones viven en `config/incendios/` y actualmente incluyen:

- `cholila-2015`, con Landsat 8 (Sentinel-2 no existía antes del incendio):
`baseline-001`, `baseline-002` (ROI ampliado) y el derivado `event-filter-001`;
- `epuyen-2025`, con `baseline-001` y el derivado `event-filter-001`;
- `los-alerces-2023`, con `baseline-001`, el experimento `event-filter-001`
y el derivado recomendado `event-filter-002`;
- `puerto-cafe-2025`, incendio de Los Alerces–Rivadavia–Cholila iniciado en diciembre de 2025, con `baseline-001` y el derivado `event-filter-001`;
- `puerto-patriada-2026`, con `baseline-002` y el derivado `event-filter-001`.



## Estructura

```text
config/incendios/<evento>.json
dataset/<evento>/runs/<run>/
├── imagenes_pre/
├── imagenes_post/
├── mascaras/
├── candidatos_cambio/                 # runs event-filter
├── otro_incendio_probable/             # runs event-filter
├── cambio_no_confirmado/               # runs event-filter
├── confianza_incendio/                 # runs event-filter
├── calidad/observacion_valida/
├── visualizaciones/
├── componentes.csv                     # runs event-filter
├── hotspots.csv                        # runs event-filter
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

Los baselines de todos los eventos quedaron completados. Un preflight puede
revisar escenas y grilla sin escribir datos:

```bash
.venv/bin/python generar_dataset.py \
  --event los-alerces-2023 \
  --run baseline-001 \
  --dry-run
```



## Filtro de atribución al evento

Los runs `event-filter-*` se derivan de un baseline completo sin modificarlo:

```bash
.venv/bin/python filtrar_evento.py \
  --event epuyen-2025 \
  --run event-filter-001
```

El filtro etiqueta componentes sobre el mosaico global, selecciona el clúster térmico más próximo a la semilla declarada y conserva capas separadas para el incendio objetivo, otros incendios probables y cambios no confirmados. Epuyén, Puerto Patriada y Puerto Café usan VIIRS S-NPP NRT de 375 m. Los Alerces y Cholila usan el producto histórico VNP14A1 de 1 km porque la colección NRT de 375 m disponible en Earth Engine comienza en septiembre de 2023.

Las reglas y distancias efectivas quedan selladas en `run.json`; la decisión de cada objeto queda en `componentes.csv` y la evidencia en `hotspots.csv`.

En Los Alerces no debe usarse `event-filter-001`: esa ejecución conservada para trazabilidad reveló una reducción incorrecta de máscaras VNP14A1 y quedó sin evidencia térmica. `event-filter-002` corrige la reducción y es el resultado recomendado. En Cholila, `event-filter-001` deriva de `baseline-002`; `baseline-001` se conserva para trazabilidad porque su ROI cortaba la cicatriz.

Las cuentas actuales de Earth Engine requieren un proyecto Google Cloud con la API habilitada y registrado para uso de Earth Engine. Todos los eventos usan `ee-nachochevallier`; el proyecto efectivo se incluye en la configuración sellada de `run.json`. `--project` permite reemplazarlo explícitamente al crear otro run.

Un run incompleto se puede eliminar explícitamente:

```bash
.venv/bin/python generar_dataset.py \
  --event epuyen-2025 \
  --run baseline-001 \
  --clear-incomplete
```

El comando rechaza la limpieza de runs completados. El antiguo `--clear` global ya no existe.

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

## Algoritmo

La máscara base usa:

```text
NBR = (B8 - B12) / (B8 + B12)
dNBR = NBR_pre - NBR_post
```

Con Landsat 8 (`LANDSAT/LC08/C02/T1_L2`), las bandas SR se renombran a sus equivalentes S2 (`SR_B2..SR_B4` → `B2..B4`, `SR_B5` → `B8`, `SR_B6` → `B11`, `SR_B7` → `B12`), la reflectancia se lleva a escala 0–10000 y las nubes, sombras y nieve se enmascaran con `QA_PIXEL`. Así los mismos umbrales aplican a ambos sensores; la grilla Landsat usa 30 m en lugar de 20 m.

Los umbrales exactos no se duplican en esta documentación: la fuente de verdad es la configuración JSON y su copia sellada dentro de `run.json`. Además de la máscara binaria, los runs nuevos exportan una capa que distingue los píxeles con observación válida simultánea en PRE y POST.

## Trazabilidad y almacenamiento

`run.json` registra configuración, hash, escenas, entorno, estados, conteos y métricas. `metadata.csv` agrega posición de grilla, cobertura válida, área quemada y estado por tile.

Los GeoTIFFs de todos los runs se conservan localmente dalepero se ignoran en Git. Se versionan las configuraciones, los manifiestos, los metadatos y la documentación. Las visualizaciones generadas también son artefactos locales ignorados por Git.

El plan y las decisiones de diseño están documentados en
`[PLAN_MULTI_INCENDIOS.md](docs/PLAN_MULTI_INCENDIOS.md)`.