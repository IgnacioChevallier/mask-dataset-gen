# Pendiente: distinguir la cicatriz objetivo de otros cambios

## Problema observado

`epuyen-2025/baseline-001` detecta correctamente la cicatriz principal del
incendio, pero también clasifica manchas laterales producidas por otros cambios
abruptos de la superficie. Entre las causas posibles están la cosecha o tala,
el secado estacional, los cambios agrícolas y otros incendios ocurridos dentro
de la misma ventana temporal.

El problema es conceptual: `dNBR` mide una perturbación de la vegetación, pero
no demuestra por sí solo que esa perturbación haya sido causada por fuego ni
que pertenezca al incendio específico bajo estudio.

Por este motivo se deben separar dos preguntas:

1. ¿El cambio observado es compatible con fuego?
2. ¿Ese cambio pertenece al incendio objetivo?

`baseline-001` responde parcialmente la primera pregunta, pero todavía no
resuelve la atribución al evento.

## Evidencia observada en Epuyén

La máscara generada contiene 17 componentes espaciales desconectados. El
análisis aproximado de esos componentes dio el siguiente resultado:

| Grupo | Área aproximada | Interpretación inicial |
| --- | ---: | --- |
| Cicatriz principal | 2.876 ha | Continua y con múltiples detecciones térmicas |
| Fragmentos próximos | 105 ha | A unos 44–780 m del núcleo y con evidencia térmica; probablemente pertenecen al mismo evento |
| Mancha al norte | 46 ha | Tiene detecciones térmicas, pero está separada unos 9 km; podría corresponder a otro incendio |
| Restantes manchas laterales | 204 ha | Alejadas y sin detecciones VIIRS próximas; posibles cambios no asociados a fuego |

Una selección inicial asociada espacialmente al incendio principal conservaría
aproximadamente 2.981 ha.

Esto indica que la proximidad entre las 3.228,79 ha clasificadas por el
baseline y las 3.530 ha oficiales puede ser parcialmente accidental: algunos
falsos positivos podrían estar compensando sectores reales omitidos. No se
deben ajustar parámetros con el único objetivo de igualar la superficie
oficial.

## Run propuesto

Crear un run derivado e inmutable:

```text
epuyen-2025/event-filter-001
```

El manifiesto debería declarar:

- `parent_run: baseline-001`;
- el motivo del cambio;
- los parámetros nuevos;
- las fuentes de evidencia térmica y espacial;
- las reglas utilizadas para atribuir componentes al incendio objetivo.

`baseline-001` debe permanecer intacto como resultado reproducible de la
clasificación puramente espectral actual.

## Estrategia recomendada

### 1. Componentes espaciales

Etiquetar cada mancha candidata como un objeto independiente mediante
componentes conectados.

Antes de separarlos se puede aplicar un cierre morfológico pequeño, del orden de
60–100 m, para evitar que caminos, nubes, sombras o huecos internos dividan una
cicatriz continua en varios objetos.

No se debe conservar automáticamente sólo el componente más grande: un
incendio real puede quedar fragmentado por caminos, ríos, píxeles inválidos o
focos secundarios.

### 2. Asociación con el incendio objetivo

Usar como semillas espaciales y temporales:

- el punto conocido de inicio del incendio;
- el clúster de detecciones térmicas VIIRS asociado a ese punto y fecha;
- un perímetro oficial, si estuviera disponible;
- opcionalmente, un polígono revisado o digitalizado manualmente.

Las detecciones VIIRS deben agruparse espacial y temporalmente. No alcanza con
aceptar cualquier hotspot dentro del ROI, porque puede haber otros incendios en
la misma región y ventana temporal.

Cada componente candidato debería clasificarse como:

- conectado o próximo al evento objetivo;
- compatible con otro incendio;
- cambio sin evidencia térmica;
- incierto.

VIIRS tiene una resolución nominal de 375 m. Sirve como evidencia de fuego y
como semilla aproximada, pero no como un perímetro preciso. La ausencia de una
detección VIIRS tampoco demuestra por sí sola que no haya existido fuego: el
satélite puede omitir eventos pequeños, breves, cubiertos por nubes o ocurridos
entre adquisiciones.

### 3. Firma espectral específica de fuego

Complementar `dNBR` con variables que ayuden a distinguir fuego de cosecha,
tala, suelo expuesto y sequedad:

- MIRBI y diferencia temporal de MIRBI;
- NBR2;
- BAIS2;
- cambios en rojo, NIR, SWIR1 y SWIR2;
- bandas red-edge de Sentinel-2: `B5`, `B6`, `B7` y `B8A`.

Las bandas rojas y red-edge pueden aportar información para separar cosechas de
áreas quemadas. NIR y SWIR ayudan a identificar la pérdida de humedad y la
respuesta espectral de carbón, ceniza y vegetación dañada.

Estos indicadores no deberían convertirse inmediatamente en una nueva regla
binaria rígida. Conviene calcular primero sus distribuciones para:

- la cicatriz principal;
- los fragmentos próximos;
- las manchas laterales;
- zonas de control sin cambio.

### 4. Comportamiento temporal

Reemplazar la comparación exclusiva entre dos medianas por una serie temporal
de observaciones Sentinel-2 alrededor del evento.

Patrones esperables:

- incendio: cambio abrupto próximo a la fecha conocida y señal persistente en
  varias observaciones posteriores;
- sequedad estacional: cambio más gradual;
- cosecha o tala: cambio potencialmente abrupto y persistente, pero sin
  evidencia térmica y con distinta respuesta en rojo/red-edge;
- artefacto atmosférico: salto aislado que desaparece en la observación
  siguiente.

Como primera versión se puede exigir persistencia durante dos o tres
observaciones POST o durante una ventana aproximada de 15–45 días. El valor
final debe quedar parametrizado y documentado en el run.

### 5. Forma y contexto

La geometría puede utilizarse como evidencia secundaria:

- parcelas con bordes rectos o regulares pueden indicar cosecha;
- una cicatriz irregular y continua puede ser más compatible con fuego;
- cercanía espacial y temporal a hotspots aumenta la confianza.

La forma no debe ser un filtro definitivo. Los incendios también pueden seguir
límites de caminos o parcelas y las cosechas no siempre tienen geometrías
perfectamente regulares.

## Salidas propuestas

No reemplazar la máscara candidata por una única decisión opaca. Generar capas
separadas:

```text
candidatos_cambio.tif
incendio_objetivo.tif
otro_incendio_probable.tif
cambio_no_confirmado.tif
confianza_incendio.tif
```

Significado:

- `candidatos_cambio`: resultado espectral inicial, equivalente conceptualmente
  al baseline;
- `incendio_objetivo`: componentes atribuidos al evento estudiado;
- `otro_incendio_probable`: componentes con evidencia de fuego, pero no
  asociados al evento objetivo;
- `cambio_no_confirmado`: perturbaciones sin evidencia suficiente de fuego;
- `confianza_incendio`: puntuación continua para auditoría y ajuste posterior.

Los metadatos por componente deberían incluir:

- ID determinista;
- área y perímetro;
- centroide y límites;
- distancia al componente principal;
- distancia a la semilla del evento;
- cantidad y distancia de hotspots;
- fechas de hotspots;
- estadísticas de dNBR, MIRBI, NBR2, BAIS2 y red-edge;
- persistencia temporal;
- clase final y motivos de la decisión.

## Orden de implementación recomendado

1. Mantener sin cambios la generación de candidatos de `baseline-001`.
2. Incorporar componentes conectados y métricas por objeto.
3. Consultar VIIRS y formar clústeres espaciotemporales de fuego activo.
4. Identificar el clúster que contiene o está más próximo a la semilla del
   evento.
5. Clasificar los componentes como incendio objetivo, otro incendio o cambio
   no confirmado.
6. Incorporar persistencia temporal Sentinel-2.
7. Agregar MIRBI, NBR2, BAIS2 y bandas red-edge.
8. Generar visualizaciones comparativas entre candidato, resultado filtrado y
   clases rechazadas.
9. Recién después evaluar si hace falta un clasificador estadístico o de
   aprendizaje automático.

La primera iteración debería usar reglas explícitas y auditables. No se
recomienda comenzar con deep learning: todavía hay suficiente información
espacial, térmica y temporal sin explotar, y no existe un conjunto local de
etiquetas validado para entrenamiento.

## Criterios de aceptación

`event-filter-001` se considerará útil cuando:

- conserve la cicatriz central y sus fragmentos próximos razonables;
- separe incendios ajenos al evento objetivo;
- reduzca las manchas laterales sin evidencia térmica ni continuidad espacial;
- documente por qué se aceptó o rechazó cada componente;
- mantenga las capas intermedias para auditoría;
- no utilice las 3.530 ha oficiales como objetivo de calibración;
- permita aplicar la misma metodología a Los Alerces y otros incendios;
- pueda compararse reproduciblemente con `baseline-001`.

## Implementación y evaluación — 2026-09-21

Se implementó la primera iteración auditable en `filtrar_evento.py`. El proceso:

1. parte de un `baseline-001` completo e inmutable;
2. forma componentes sobre el mosaico global, no tile por tile;
3. aplica un cierre morfológico parametrizado de 80 m sólo para asociar objetos;
4. consulta detecciones térmicas y las agrupa espacialmente;
5. selecciona como objetivo el clúster más próximo a la semilla del evento;
6. clasifica cada componente por semilla, hotspot o continuidad con el objetivo;
7. conserva capas separadas y metadatos con el motivo de cada decisión.

Las salidas propuestas se materializan como directorios de tiles, para respetar
la estructura multi-incendio:

```text
candidatos_cambio/
mascaras/                       # incendio objetivo
otro_incendio_probable/
cambio_no_confirmado/
confianza_incendio/
componentes.csv
hotspots.csv
```

### Resultados

| Evento y run recomendado | Baseline informado | Incendio objetivo | Otro fuego | No confirmado | Evaluación visual |
| --- | ---: | ---: | ---: | ---: | --- |
| `epuyen-2025/event-filter-001` | 3.228,79 ha | 2.995,03 ha | 38,71 ha | 212,57 ha | Conserva la cicatriz central y elimina las manchas laterales observadas. |
| `los-alerces-2023/event-filter-002` | 1.346,40 ha | 1.067,01 ha | 0,00 ha | 291,74 ha | Conserva el componente con 37 observaciones térmicas y elimina los grupos aislados del norte y sur. |

La superficie candidata recalculada localmente difiere levemente del área del
manifiesto baseline porque se integra sobre los GeoTIFF exportados en EPSG:4326,
mientras que el baseline usa `pixelArea` de Earth Engine. La clasificación y
las comparaciones internas del filtro usan siempre el mismo cálculo local.

En Epuyén, la concordancia con las 3.530 ha oficiales empeora al retirar ruido,
lo cual respalda la advertencia original: la cercanía del baseline a la cifra
oficial estaba parcialmente compensada por falsos positivos. En Los Alerces,
la diferencia respecto de la referencia primaria de 1.160 ha baja de +186,40 ha
a -92,99 ha, aunque empeora respecto de la referencia alternativa de 1.390 ha.
La superficie oficial no se utilizó para decidir ningún componente.

La conclusión es que el filtro **mejora la pureza espacial y la atribución al
evento** en ambos casos, pero todavía no permite medir precisión o recall sin
un perímetro de verdad terreno. Las capas rechazadas se conservan justamente
para esa revisión.

`los-alerces-2023/event-filter-001` se conserva por la política de runs
inmutables, pero no debe usarse: una reducción temporal incorrecta de VNP14A1
produjo cero hotspots. `event-filter-002` usa una suma enmascarada, recupera 37
observaciones en 25 píxeles y es el resultado válido.

### Alcance pendiente

Esta iteración cubre los pasos 1–5 y 8 del orden recomendado. Siguen pendientes:

- persistencia temporal Sentinel-2 por observación;
- MIRBI, NBR2, BAIS2 y bandas red-edge por componente;
- evaluación contra perímetros revisados o polígonos de verdad terreno;
- eventual calibración de confianza con etiquetas, sin usar el área oficial
  como objetivo.

## Referencias técnicas

- Google Earth Engine, análisis de objetos y componentes conectados:
  <https://developers.google.com/earth-engine/guides/image_objects>
- Google Earth Engine, VIIRS Active Fire de 375 m:
  <https://developers.google.com/earth-engine/datasets/catalog/NASA_LANCE_SNPP_VIIRS_C2>
- Liu et al., detección de áreas quemadas mediante series temporales
  Sentinel-2 y productos de fuego activo:
  <https://www.sciencedirect.com/science/article/pii/S0034425723003048>
- van Dijk et al., separación espectral entre áreas quemadas y falsos positivos
  producidos por cosechas:
  <https://www.sciencedirect.com/science/article/pii/S0303243421000027>
