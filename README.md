# mask-dataset-gen

Generador reproducible de datasets de áreas quemadas a partir de Sentinel-2 o Landsat 8 y Google Earth Engine. El sistema compara composiciones PRE y POST, calcula dNBR, aplica filtros espectrales y exporta imágenes, máscaras, calidad y metadatos por tile.

## Eventos configurados

```bash
python generar_dataset.py --list-events
```

Las configuraciones viven en `config/incendios/`. Los incendios 2015–2016 usan
Landsat 8 porque Sentinel-2 no cubre el período previo; el resto usa Sentinel-2.
La columna "Resultado" indica el run que conviene usar.

| Evento | Inicio | Sensor | Runs | Resultado |
| --- | --- | --- | --- | --- |
| `desemboque-2015` | 2015-01-30 | Landsat 8 | `baseline-002` | `event-filter-001` |
| `cerro-plataforma-2015` | 2015-02-03 | Landsat 8 | `baseline-001` | `event-filter-001` |
| `cholila-2015` | 2015-02-15 | Landsat 8 | `baseline-002` | `event-filter-001` |
| `los-alerces-2015` | 2015-03-22 | Landsat 8 | `baseline-001` | `event-filter-001` |
| `currumahuida-2015` | 2015-03-23 | Landsat 8 | `baseline-001` | `event-filter-001` |
| `los-alerces-2016` | 2016-01-21 | Landsat 8 | `baseline-001` | `event-filter-001` |
| `epuyen-2019` | 2019-01-28 | Sentinel-2 | `baseline-001` | `event-filter-001` |
| `las-golondrinas-2021` | 2021-03-09 | Sentinel-2 | `baseline-001` | `event-filter-001` |
| `los-alerces-2023` | 2023-02-04 | Sentinel-2 | `baseline-001` | `event-filter-002` |
| `los-alerces-2024` | 2024-01-25 | Sentinel-2 | `baseline-001` | `event-filter-001` |
| `epuyen-2025` | 2025-01-15 | Sentinel-2 | `baseline-001` | `event-filter-001` |
| `el-turbio-2025` | 2025-12-01 | Sentinel-2 | `baseline-001` | `event-filter-001` |
| `puerto-cafe-2025` | 2025-12-09 | Sentinel-2 | `baseline-001` | `event-filter-001` |
| `puerto-patriada-2026` | 2026-01-05 | Sentinel-2 | `baseline-002` | `event-filter-001` |

En los eventos que declaran `reference.modis_mcd64a1_ha`, el ROI se derivó de
la cicatriz MODIS MCD64A1 con margen y la semilla, de la primera detección
térmica (o del centroide MODIS cuando no había una confiable).

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

Todos los baselines están completos. Un preflight puede
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

Los runs descartados (Cholila `baseline-001`, Desemboque `baseline-001` y Los Alerces 2023 `event-filter-001`) se eliminaron; su historia queda en Git. Por eso algunos eventos empiezan en `baseline-002` o `event-filter-002`.

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

El dataset mezcla resoluciones a propósito: los eventos Landsat quedan a 30 m y los Sentinel-2 a 20 m, sin remuestreo. La escala efectiva de cada tile está en la columna `escala_m` de `metadata.csv` y en `grid.scale_m` de `run.json`; las hectáreas se calculan con el área real de cada píxel, así que son comparables entre eventos.

Los umbrales exactos no se duplican en esta documentación: la fuente de verdad es la configuración JSON y su copia sellada dentro de `run.json`. Además de la máscara binaria, los runs nuevos exportan una capa que distingue los píxeles con observación válida simultánea en PRE y POST.

## Trazabilidad y almacenamiento

`run.json` registra configuración, hash, escenas, entorno, estados, conteos y métricas. `metadata.csv` agrega posición de grilla, cobertura válida, área quemada y estado por tile.

Los GeoTIFFs de todos los runs se conservan localmente pero se ignoran en Git. Los runs `event-filter-*` enlazan (hardlink) las imágenes PRE, POST y la capa de validez de su run padre en lugar de copiarlas. Se versionan las configuraciones, los manifiestos, los metadatos y la documentación. Las visualizaciones generadas también son artefactos locales ignorados por Git.