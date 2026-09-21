# Plan de soporte multi-incendio y runs reproducibles

## 1. Objetivo

Generalizar el pipeline actual para investigar múltiples incendios con imágenes
Sentinel-2, sin perder acceso al dataset existente de 2026 y sin mezclar los
artefactos de distintos incendios o experimentos.

El primer caso nuevo será el incendio de Epuyén iniciado el 15 de enero de
2025. El primer resultado tendrá carácter exploratorio: permitirá inspeccionar
la cicatriz inferida mediante dNBR, pero no se presentará como una máscara
validada científicamente sin un perímetro de referencia o etiquetado manual.

## Estado de implementación

El plan quedó implementado el 20 de septiembre de 2026. La arquitectura
multi-incendio, la migración compatible de `legacy-v1`, los runs inmutables,
la capa de observación válida, las validaciones operativas y las
visualizaciones están disponibles en el repositorio.

`epuyen-2025/baseline-001` se ejecutó por completo con el proyecto Earth Engine
`ee-nachochevallier`. `los-alerces-2023/baseline-001` quedó configurado como el
siguiente caso de estudio, pero no fue ejecutado.

## 2. Estado actual y problemas a resolver

El pipeline vigente tiene estas propiedades:

- usa `COPERNICUS/S2_SR_HARMONIZED` mediante Google Earth Engine;
- define tres rectángulos ROI directamente en `generar_dataset.py`;
- compara medianas PRE y POST y calcula `dNBR = NBR_pre - NBR_post`;
- guarda todos los resultados en un único `dataset/` plano;
- asigna nombres `tile_NNN` en función de la cantidad de máscaras existentes;
- permite un `--clear` global que elimina el dataset;
- los scripts de visualización y remasking dependen de rutas fijas;
- el README no coincide con varias fechas y parámetros del código activo.

El dataset existente contiene 196 tripletas PRE/POST/máscara y 196 filas de
metadatos. Sus ventanas son:

- PRE: `2023-11-01` a `2023-12-31`;
- POST: `2026-02-01` a `2026-03-08`.

Por lo tanto, ese resultado representa cambio acumulado entre 2023 y 2026 y no
debe describirse como una aislación estricta del incendio de enero de 2026. Se
preservará como resultado histórico.

## 3. Decisiones de diseño acordadas

### 3.1 Alcance

- El sistema será multi-incendio y admitirá múltiples runs por incendio.
- En esta etapa sólo se soportará Sentinel-2 SR Harmonized.
- La configuración identificará la fuente de datos para permitir una extensión
  futura, pero no se implementarán Landsat ni otros sensores.
- Las configuraciones se escribirán en JSON para evitar dependencias nuevas.

### 3.2 Identificadores

Incendios iniciales:

- `epuyen-2025`;
- `los-alerces-2023`;
- `puerto-patriada-2026`.

Runs iniciales:

- `epuyen-2025/baseline-001`: primer run exploratorio de Epuyén 2025;
- `los-alerces-2023/baseline-001`: siguiente caso de estudio, preparado pero
  todavía no ejecutado;
- `puerto-patriada-2026/legacy-v1`: importación inmutable del dataset actual;
- `puerto-patriada-2026/baseline-002`: futura corrección temporal de 2026.

### 3.3 Configuración por incendio

Las definiciones se separarán del código:

```text
config/
└── incendios/
    ├── epuyen-2025.json
    ├── los-alerces-2023.json
    └── puerto-patriada-2026.json
```

Cada definición contendrá, como mínimo:

- ID y nombre legible;
- descripción y fecha conocida de inicio;
- colección Sentinel-2;
- uno o más ROIs rectangulares, cada uno con ID propio;
- ventanas PRE y POST;
- bandas exportadas;
- resolución y tamaño de tile;
- umbrales espectrales y morfológicos;
- reglas de calidad;
- versión del algoritmo.

La configuración efectiva de cada run quedará copiada y sellada en su
`run.json`. Una edición futura del archivo de evento no cambiará el significado
de runs ya creados.

## 4. Estructura de resultados

La estructura canónica será:

```text
dataset/
├── epuyen-2025/
│   └── runs/
│       └── baseline-001/
│           ├── imagenes_pre/
│           ├── imagenes_post/
│           ├── mascaras/
│           ├── calidad/
│           │   └── observacion_valida/
│           ├── visualizaciones/
│           │   ├── resumen_roi/
│           │   ├── tiles/
│           │   └── diagnosticos/
│           ├── metadata.csv
│           ├── resumen.md
│           └── run.json
└── puerto-patriada-2026/
    └── runs/
        ├── legacy-v1/
        └── baseline-002/
```

Los GeoTIFFs de todos los runs, incluido `legacy-v1`, serán artefactos locales
ignorados por Git. Se versionarán el código, las configuraciones, la
documentación, los metadatos y los manifiestos livianos. Las visualizaciones
generadas también permanecerán locales. Si luego fuera necesario distribuir
datasets completos mediante Git, se evaluará Git LFS o almacenamiento de
objetos.

## 5. Compatibilidad con el dataset existente

Los archivos actuales se moverán, sin duplicarlos, a:

```text
dataset/puerto-patriada-2026/runs/legacy-v1/
```

Se conservarán enlaces simbólicos compatibles:

```text
dataset/imagenes_pre  -> puerto-patriada-2026/runs/legacy-v1/imagenes_pre
dataset/imagenes      -> puerto-patriada-2026/runs/legacy-v1/imagenes_post
dataset/mascaras      -> puerto-patriada-2026/runs/legacy-v1/mascaras
dataset/metadata.csv  -> puerto-patriada-2026/runs/legacy-v1/metadata.csv
```

`legacy-v1/run.json` tendrá estado `completed` y origen `imported`. Se
registrará que la configuración fue reconstruida a partir del código y del CSV
existentes.

Los nombres `tile_000` a `tile_195` se conservarán. Mantener esta estrategia de
nombres como una variante declarada en `run.json` tiene un costo bajo y evita
romper referencias.

Los scripts ejecutados sin selectores mantendrán como destino por defecto
`puerto-patriada-2026/legacy-v1`. No deberán volver a anexar o duplicar tiles si
el run ya está completo.

## 6. Nombres y orden de tiles nuevos

Los runs nuevos usarán identificadores deterministas derivados de su posición
en la grilla:

```text
roi_01_r000_c000.tif
roi_01_r000_c001.tif
roi_01_r001_c000.tif
```

El nombre no dependerá del orden de finalización de los workers ni de la
cantidad de archivos presentes. `metadata.csv` se escribirá ordenado por ROI,
fila y columna.

## 7. Interfaz de comandos

Uso explícito para runs nuevos:

```bash
python generar_dataset.py --event epuyen-2025 --run baseline-001
python visualizar.py --event epuyen-2025 --run baseline-001
python visualizar_roi.py --event epuyen-2025 --run baseline-001
```

Descubrimiento y preflight:

```bash
python generar_dataset.py --list-events
python generar_dataset.py --event epuyen-2025 --run baseline-001 --dry-run
```

Compatibilidad:

```bash
python generar_dataset.py
python visualizar.py tile_000
python visualizar_roi.py
```

Para eventos nuevos se exigirán `--event` y `--run`; no se crearán destinos
implícitos.

## 8. Ciclo de vida e inmutabilidad

Un run tendrá estados explícitos, al menos `running`, `incomplete`, `failed` y
`completed`.

Reglas:

1. Al crearlo, se fija la configuración efectiva y su hash.
2. Una interrupción permite reanudar únicamente archivos faltantes o fallidos.
3. Si la configuración solicitada no coincide con el hash guardado, se aborta
   antes de escribir.
4. El run se marca `completed` sólo después de pasar todas las validaciones.
5. Un run completado no se modifica ni se sobrescribe.
6. Todo cambio de parámetros requiere un ID de run nuevo.

Los runs derivados declararán `parent_run`, `change_reason` y un resumen
estructurado de `parameter_changes`.

El `--clear` global se retirará. Sólo se permitirá limpiar un run incompleto y
seleccionado explícitamente:

```bash
python generar_dataset.py \
  --event epuyen-2025 \
  --run baseline-001 \
  --clear-incomplete
```

La opción rechazará runs completados. La eliminación deliberada de un run
completo quedará fuera del generador y se documentará por separado.

## 9. Configuración de `epuyen-2025/baseline-001`

### 9.1 Alcance espacial

Se utilizará únicamente el segundo ROI del código actual:

```json
[-71.578, -42.416, -71.201, -42.079]
```

Es un rectángulo de búsqueda, no un perímetro supuesto de la cicatriz. La
franja quemada se inferirá a partir de Sentinel-2 y dNBR. Mantener contexto no
quemado permitirá observar falsos positivos.

### 9.2 Ventanas temporales

- PRE: `2024-11-01` a `2025-01-14`, inclusive;
- POST: `2025-02-01` a `2025-03-08`, inclusive.

La implementación deberá convertir de forma explícita estas fechas inclusivas
a la semántica de fin exclusivo de `ee.ImageCollection.filterDate`.

### 9.3 Parámetros de máscara

El baseline reutilizará el algoritmo activo sin ajustar varios factores a la
vez:

| Parámetro | Valor |
| --- | ---: |
| `DNBR_UMBRAL` | `0.30` |
| `PRE_NBR_MIN` | `0.15` |
| `POST_NBR_MAX` | `0.40` |
| `NDSI_NIEVE_MAX` | `0.25` |
| `BRILLO_MAX` | `3500` |
| `CROMA_MIN` | `500` |
| `NDWI_AGUA_MAX` | `0.05` |
| `MIN_PIXELES` | `150` |
| `DILATACION_PX` | `1` |
| `ESCALA` | `20 m` |

Se mantendrán las bandas `B2`, `B3`, `B4`, `B8`, `B11` y `B12`, el filtro de
escenas con menos de 20% de nubosidad y la exclusión SCL vigente.

## 10. Capa de calidad

La máscara binaria seguirá usando `0` para no quemado y `1` para quemado, pero
se agregará una capa separada que indique dónde existen observaciones válidas
en PRE y POST. Esto evita interpretar ausencia de datos como evidencia de
ausencia de incendio.

Por tile:

- cobertura válida `>= 90%`: condición normal;
- cobertura válida `< 90%`: completar con advertencia;
- cobertura válida `0%`: marcar el tile como fallido y el run como incompleto;
- no excluir automáticamente tiles con cobertura parcial.

El porcentaje válido se guardará en `metadata.csv` y se mostrará en las
visualizaciones.

## 11. Metadatos y trazabilidad

`run.json` registrará:

- configuración completa y hash;
- colección e IDs exactos de escenas Sentinel-2 PRE y POST;
- versión del algoritmo;
- commit de Git;
- versiones de Python y dependencias relevantes;
- fechas de creación, inicio y finalización;
- estado del run y errores;
- conteos de tiles esperados, completos, omitidos y fallidos;
- estrategia de nombres de tiles;
- métricas resumidas y cobertura válida.

Los `metadata.csv` nuevos conservarán los campos conceptuales actuales y
agregarán, como mínimo:

- `event_id` y `run_id`;
- `roi_id`, fila y columna;
- ID determinista del tile;
- límites geográficos;
- porcentaje quemado sobre área válida;
- porcentaje de observación válida;
- ventanas PRE y POST;
- resolución;
- estado y mensaje de error.

El CSV original de `legacy-v1` no se modificará.

## 12. Validaciones operativas

### 12.1 Antes de descargar

- validar estructura, tipos y campos requeridos del JSON;
- validar IDs seguros de evento y run;
- autenticar e inicializar Earth Engine sin guardar credenciales en el repo;
- comprobar que existan escenas PRE y POST;
- calcular cantidad de ROIs y tiles;
- mostrar escenas, cobertura, tiles y destino mediante `--dry-run`;
- rechazar colisiones con runs completados o configuraciones incompatibles.

### 12.2 Después de descargar

- exigir una tripleta PRE/POST/máscara por tile;
- exigir su correspondiente raster de observación válida;
- comprobar dimensiones, grilla, CRS y transformación coincidentes;
- comprobar que las máscaras sólo contengan `0` y `1`;
- comprobar una única fila de metadatos por tile;
- ordenar y escribir metadatos de forma determinista;
- generar las visualizaciones resumen;
- completar `resumen.md` y `run.json` antes de marcar `completed`.

Las escrituras deberán ser atómicas cuando sea práctico: descargar o producir
un archivo temporal y renombrarlo sólo al finalizar correctamente.

## 13. Visualizaciones y resumen

Cada run nuevo generará automáticamente:

- mosaico PRE del ROI;
- mosaico POST del ROI;
- máscara del ROI;
- máscara superpuesta sobre POST;
- capturas o diagnósticos adicionales por tile sin sobrescribir nombres
  existentes.

Las vistas deberán diferenciar las zonas sin observación válida.

Las métricas se calcularán con `ee.Image.pixelArea()` y no aproximando cada
píxel geográfico como un cuadrado fijo. Se informarán:

- hectáreas clasificadas como quemadas;
- porcentaje quemado sobre área válida;
- cobertura válida;
- métricas por ROI y para la unión total;
- ranking de tiles con mayor porcentaje quemado.

`resumen.md` reunirá configuración, escenas, métricas, advertencias, enlaces a
visualizaciones y estado final.

## 14. Run corregido de 2026

`puerto-patriada-2026/baseline-002` conservará los tres ROIs y parámetros
actuales, pero utilizará ventanas más cercanas al evento:

- PRE: `2025-11-01` a `2026-01-04`, inclusive;
- POST: `2026-02-01` a `2026-03-08`, inclusive.

El PRE ya incorpora la cicatriz de Epuyén 2025 como estado de base. El objetivo
es reducir la atribución al incendio de 2026 de cambios ocurridos desde 2023.

Este run no se ejecutará hasta revisar `epuyen-2025/baseline-001`.

## 15. Secuencia de implementación y ejecución

### Fase A: modelo y configuración

1. Introducir carga y validación de configuraciones JSON.
2. Separar constantes globales de la lógica de procesamiento.
3. Resolver rutas por evento y run.
4. Implementar manifiesto, hash y estados del run.
5. Incorporar nombres deterministas y metadatos ordenados.

### Fase B: migración y compatibilidad

1. Verificar nuevamente las 196 tripletas y filas existentes.
2. Moverlas a `puerto-patriada-2026/runs/legacy-v1` preservando contenido.
3. Crear el manifiesto importado.
4. Crear enlaces simbólicos de compatibilidad.
5. Adaptar generador, visualizadores y remasking a rutas seleccionables.
6. Actualizar `.gitignore` para conservar localmente, pero no versionar, los
   GeoTIFFs de `legacy-v1`.

### Fase C: calidad y visualización

1. Exportar observación válida.
2. Añadir preflight y `--dry-run`.
3. Añadir validaciones posteriores y reanudación.
4. Generar métricas con `pixelArea`.
5. Generar las cuatro vistas del ROI y `resumen.md`.

### Fase D: primer run de Epuyén

1. Ejecutar `--dry-run` para confirmar escenas y cantidad de tiles.
2. Si hay escenas suficientes, ejecutar `epuyen-2025/baseline-001` completo.
3. Revisar cobertura, área estimada, mosaicos y tiles destacados.
4. Comparar razonadamente con las 3.530 ha reportadas oficialmente.
5. Recomendar conservar el baseline o crear `tuning-001`.

### Fase E: trabajo posterior

1. Sólo después de revisar Epuyén, ejecutar
   `puerto-patriada-2026/baseline-002`.
2. Compararlo con `legacy-v1` sin modificar ninguno de los dos.

## 16. Criterio de aceptación de `epuyen-2025/baseline-001`

El primer run se considerará entregado cuando:

- esté completo y pueda reanudarse con seguridad si hubo interrupciones;
- registre configuración, escenas y estado reproducible;
- informe cobertura válida y área detectada;
- produzca vistas PRE, POST, máscara y superposición;
- identifique los tiles con más detección;
- incluya observaciones sobre falsos positivos o negativos visibles;
- compare el orden de magnitud con el dato oficial, sin calibrar los umbrales
  para forzar una coincidencia;
- concluya con una recomendación concreta sobre un posible `tuning-001`.

No se afirmará exactitud, sensibilidad ni especificidad sin verdad de terreno o
un perímetro independiente.

## 17. Fuera de alcance actual

- soporte para sensores distintos de Sentinel-2;
- entrenamiento de modelos de aprendizaje automático;
- validación científica con verdad de terreno;
- ajuste automático de umbrales;
- ejecución inmediata de `puerto-patriada-2026/baseline-002`;
- almacenamiento remoto o publicación del dataset;
- suite de pruebas automatizadas y smoke test de un tile.

La ausencia temporal de pruebas automatizadas es un riesgo aceptado. Las
validaciones incorporadas al pipeline reducen errores operativos, pero no
reemplazan pruebas unitarias o de integración. Deberán añadirse antes de una
refactorización posterior importante.

## 18. Fuentes de contexto del incendio de Epuyén 2025

- Servicio Nacional de Manejo del Fuego, reporte que registra inicio el
  `15/01/2025` y superficie de `3.530 ha`:
  <https://www.argentina.gob.ar/sites/default/files/2024/09/reporte_diario_26_03_2025_0.pdf>
- Vialidad Nacional, ubicación del inicio en La Rinconada:
  <https://www.argentina.gob.ar/noticias/en-chubut-vialidad-nacional-colabora-en-la-lucha-contra-el-incendio-de-bosques-en-epuyen>

## 19. Siguiente caso: Los Alerces 2023

Se agrega `los-alerces-2023/baseline-001` para el incendio Gabriel Rodales /
Población Rosales II, iniciado el 4 de febrero de 2023.

Configuración preparada:

- ROI: `[-71.72, -43.0, -71.43, -42.76]`, alrededor de Población Rosales y
  Laguna Larga;
- PRE: `2022-11-01` a `2023-02-03`, inclusive;
- POST: `2023-02-20` a `2023-03-31`, inclusive;
- parámetros: el mismo baseline espectral que Epuyén 2025;
- grilla estimada: 42 tiles de 256 × 256 píxeles a 20 m/píxel.

El control externo principal será la estimación mensual oficial de 1.160 ha
(278 ha dentro del parque y 882 ha en jurisdicción provincial). El manifiesto
también conserva el parte posterior de 1.390 ha como referencia alternativa,
sin usar ninguna de las dos cifras para ajustar automáticamente los umbrales.

Fuentes:

- Informe de ocurrencia de febrero de 2023:
  <https://www.argentina.gob.ar/sites/default/files/2022/08/informe_ocurrencia_mes_febrero_2023.pdf>
- Reporte diario del 1 de marzo de 2023:
  <https://www.argentina.gob.ar/sites/default/files/2022/08/reporte_diario_01-03-2023.pdf>

Este caso se ejecutará después de completar y revisar Epuyén 2025.

## 20. Resultado de `epuyen-2025/baseline-001`

El run terminó en estado `completed` y dejó:

- 19 escenas Sentinel-2 PRE y 7 POST;
- 72 juegos completos de PRE, POST, máscara y observación válida;
- 71 tiles en estado normal y uno con advertencia por 89,73% de cobertura;
- 99,07% de cobertura válida total;
- 3.228,79 ha clasificadas como quemadas, frente a la referencia oficial de
  3.530 ha: una diferencia exploratoria de -301,21 ha (-8,53%);
- cuatro visualizaciones del mosaico y un manifiesto sin errores de validación.

La vista superpuesta muestra una cicatriz principal grande y espacialmente
continua al sur y sudeste del lago Epuyén. También aparecen parches aislados
fuera de ese núcleo, por lo que la cercanía entre la superficie detectada y la
oficial no debe interpretarse todavía como exactitud: falsos positivos y falsos
negativos pueden compensarse en el total.

Se conserva `baseline-001` sin modificar. La recomendación es contrastarlo con
un perímetro independiente antes de crear un eventual `tuning-001`; no se
ajustarán umbrales sólo para acercar el total a 3.530 ha. El siguiente run a
evaluar será `los-alerces-2023/baseline-001`.
