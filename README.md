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

## Uso como referencia de propagación

Los modelos de propagación se validan contra estas cicatrices, pero no modelan la
supresión. En igniteinsights, los incendios combatidos con éxito cerca de poblados y
rutas terminaron 4 a 14 veces más chicos que una propagación libre. Los de acceso
difícil, en cambio, se parecen a una propagación libre.

Cada `dataset/<evento>/README.md` documenta:

- la ignición;
- el combate y la supresión;
- las particularidades;
- el horizonte de crecimiento libre;
- las fuentes.

Lo que no se pudo verificar está marcado como **sin confirmar**.

### Clasificación

- **Combatido:** combatido cerca de poblados/rutas.
- **Acceso difícil:** acceso difícil / poco combatido.
- **Latente:** latente por rayo.
- **Varios:** varios eventos en la ROI.

Un incendio puede tener más de una.

### Horizonte y cicatriz

- **Horizonte de crecimiento libre:** momento en que el área FIRMS acumulada deja de crecer.
  - El área FIRMS acumulada es la suma diaria de píxeles VIIRS SP (375 m) sobre la caja de diagnóstico de igniteinsights (`benchmarks/diagnosticos/<evento>.json`).
  - Puede incluir incendios vecinos.
- **Cicatriz en el horizonte:** la máscara del run vigente ∩ un píxel VIIRS alrededor de cada detección hasta el horizonte. Es la referencia truncada de igniteinsights (`RESULTADOS-CSS-BAP.md` §2.1).

### Tabla resumen

| Evento | Clasificación | Horizonte libre | Cicatriz en el horizonte | Run vigente |
| --- | --- | --- | --- | --- |
| [`desemboque-2015`](dataset/desemboque-2015/README.md) | Combatido; varios | hasta el 3-feb; no usar (máscara = 24 % de lo oficial) | — | `event-filter-001` |
| [`cerro-plataforma-2015`](dataset/cerro-plataforma-2015/README.md) | Latente; varios | no definible (mezclado con Cholila) | — | `event-filter-001` |
| [`cholila-2015`](dataset/cholila-2015/README.md) | Acceso difícil; latente (sin confirmar); varios | crece ~19 días; se usa 120 h | 26 % | `event-filter-001` |
| [`los-alerces-2015`](dataset/los-alerces-2015/README.md) | Combatido | ~48–72 h | 95 % | `event-filter-001` |
| [`currumahuida-2015`](dataset/currumahuida-2015/README.md) | Combatido; varios | no definible (varias fases) | — | `event-filter-001` |
| [`los-alerces-2016`](dataset/los-alerces-2016/README.md) | Combatido | ~48 h (se usa 72 h) | 74 % | `event-filter-001` |
| [`epuyen-2019`](dataset/epuyen-2019/README.md) | Combatido | hasta el 3-feb (se usa 120 h) | 87 % | `event-filter-001` |
| [`las-golondrinas-2021`](dataset/las-golondrinas-2021/README.md) | Combatido; varios | primera noche (por cronología; VIIRS casi no lo vio) | ~100 % | `event-filter-001` |
| [`los-alerces-2023`](dataset/los-alerces-2023/README.md) | Combatido | ~54 h (se usa 72 h) | 99 % | `event-filter-002` |
| [`los-alerces-2024`](dataset/los-alerces-2024/README.md) | Combatido | no se detiene antes del 5-feb; se usa 120 h | 45 % | `event-filter-001` |
| [`epuyen-2025`](dataset/epuyen-2025/README.md) | Combatido | días 1–2 (se usa 96 h) | 77 % | `event-filter-001` |
| [`el-turbio-2025`](dataset/el-turbio-2025/README.md) | Latente; combatido (en parte) | crece bajo combate hasta el 11-dic; se usa 120 h | 56 % | `event-filter-001` |
| [`puerto-cafe-2025`](dataset/puerto-cafe-2025/README.md) | Acceso difícil; latente; varios | 96 h desde el 5-ene (fase explosiva) | 23 % | `event-filter-001` |
| [`puerto-patriada-2026`](dataset/puerto-patriada-2026/README.md) | Combatido; varios | 96 h, antes del salto del 10-ene | 23 % | `event-filter-001` |

## Validación externa: MODIS MCD64A1

Contraste de la máscara objetivo del run vigente con
[MCD64A1 v061](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD64A1)
(celdas de ~463 m, `BurnDate` entre el fin del PRE y el inicio del POST).
Es un chequeo de coherencia, no verdad de campo: MCD64A1 engorda los bordes y
omite fuegos chicos o de baja severidad.

```bash
.venv/bin/python validar_mcd64a1.py epuyen-2019 los-alerces-2023:event-filter-002
```

- **MCD64A1 en ROI:** todo lo quemado en los ROIs en esa ventana, incluidos incendios vecinos.
- **MCD64A1 del incendio:** celdas quemadas que contienen algún píxel de la máscara. Depende de la máscara, así que sirve para comparar áreas, no como prueba independiente.
- **Máscara confirmada:** % de píxeles de la máscara que caen en una celda MODIS quemada. Es la medida independiente.

| Evento | Oficial (ha) | Máscara (ha) | MCD64A1 del incendio (ha) | MCD64A1 en ROI (ha) | Máscara confirmada |
| --- | ---: | ---: | ---: | ---: | ---: |
| `desemboque-2015` | 2307 | 558 | 322 | 322 | 49 % |
| `cerro-plataforma-2015` | 7371 | 6292 | 7492 | 7899 | 81 % |
| `cholila-2015` | 28960 | 26763 | 30202 | 41880 | 90 % |
| `los-alerces-2015` | 1500 | 1202 | 1395 | 1417 | 88 % |
| `currumahuida-2015` | 3151 | 4236 | 4680 | 4937 | 84 % |
| `los-alerces-2016` | 1700 | 1850 | 2147 | 2147 | 90 % |
| `epuyen-2019` | 1553 | 1545 | 1975 | 1996 | 83 % |
| `las-golondrinas-2021` | 12901 | 10656 | 11377 | 17838 | 89 % |
| `los-alerces-2023` | 1160 | 1067 | 1395 | 1481 | 90 % |
| `los-alerces-2024` | 5971 | 6007 | 6719 | 6740 | 88 % |
| `epuyen-2025` | 3530 | 2995 | 3198 | 3198 | 85 % |
| `el-turbio-2025` | 3000 | 1969 | 1696 | 1739 | 53 % |
| `puerto-cafe-2025` | 31000 | 38236 | 40850 | 41300 | 84 % |
| `puerto-patriada-2026` | 14770 | 24513 | 27777 | 64269 | 84 % |

Lectura:

- En 12 de 14 eventos, entre el 81 % y el 90 % de la máscara cae en celdas que MCD64A1 también marca quemadas. El resto se concentra en los bordes, donde una celda de 500 m queda parcialmente quemada.
- Salvo en Desemboque y El Turbio, MCD64A1 del incendio supera a la máscara entre un 7 % y un 31 %. Es lo esperable: cada celda que toca la cicatriz cuenta entera, con islas sin quemar incluidas.
- Donde la máscara supera la cifra oficial (Currumahuida, Puerto Café, Puerto Patriada), MCD64A1 también la supera: respalda el área de la máscara frente a la oficial.
- La diferencia entre MCD64A1 en ROI y MCD64A1 del incendio coincide con los incendios vecinos que el filtro separa. En Puerto Patriada son ~36.500 ha contra las 40.700 ha de "otro incendio probable"; en Cholila, ~11.700 ha, con un total en ROI cercano a las 41.000 ha que citan otras fuentes.
- Desemboque (49 %) y El Turbio (53 %) tienen baja confirmación. Desemboque ya está marcado como no usable.
- El Turbio es una omisión de MCD64A1 por fragmentación, no un error de la máscara:
  - Los 11 componentes tienen detecciones VIIRS a menos de 10 m.
  - El dNBR de lo no confirmado es igual al del resto (mediana 0,42–0,43).
  - Sólo el 30 % del área cae en celdas MODIS quemadas en más de un 75 %; en Epuyén 2025 y Los Alerces 2024 es el 66–68 %.
  - En las celdas casi llenas confirma un 88 %, y por debajo de la mitad, un 9–27 %. Ver [su README](dataset/el-turbio-2025/README.md).

Los valores `reference.modis_mcd64a1_ha` de las configs se usaron para derivar
los ROIs y no siguen este método. No se actualizan porque `reference` forma parte
del hash de configuración de los runs.

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