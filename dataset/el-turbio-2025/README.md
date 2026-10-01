# El Turbio 2025

**Clasificación:**

- latente por rayo;
- combatido cerca de poblados/rutas, en parte: hubo combate intenso, pero en un valle de pobladores dispersos y sin rutas.

Términos y método comunes a todos los incendios: [README principal](../../README.md#uso-como-referencia-de-propagación).
Verificado contra las fuentes el 29-sep-2026.

## Resumen

- **Nombre:** incendio de Loma de la Chancha, valle de El Turbio (Lago Puelo, Chubut), junto al Parque Nacional Lago Puelo.
- **Inicio:** detectado el lunes 1-dic-2025.
- **Control:** 90 % controlado el 18-dic-2025, según el SPMF (Red43).
- **Superficie oficial:** ~3.000 ha (ANB, 10-dic-2025). La superficie final seguía "en evaluación" el 18-dic.
- **Máscara del run vigente:** 1.969 ha.
- **Run vigente:** `event-filter-001`.

## Ignición

- **Fecha y lugar:** detectado el lunes 1-dic-2025 en Loma de la Chancha (Red43, 4-dic-2025).
- **Causa:** "la caída de un rayo" (Red43, 4-dic-2025). La fecha exacta de la tormenta queda **sin confirmar**.
- **Detección satelital:** la primera detección VIIRS SP es del 2-dic, 18:16 UTC. Es un día después de la detección oficial, así que al principio ardió latente.
- **Coordenada del run:** -42,2959 / -71,9356, primera detección VIIRS 375 m. Cae 60 m fuera de la cicatriz.
  - La nota de la config dice "3 de diciembre", pero la primera detección SP es del 2-dic.
  - No hay coordenada oficial. igniteinsights usa la celda interior más cercana: -42,29621 / -71,93738, a 554 m de altura.

## Combate y supresión

- **Recursos:**
  - Primeros días: brigadistas de El Turbio, Lago Puelo y Golondrinas, dos aviones hidrantes y un helicóptero; el jueves se sumaron 16 brigadistas nacionales y otro helicóptero (Red43, 4-dic).
  - 9-dic: más de 110 personas, 66 combatientes en línea y cinco medios aéreos "cuando el clima lo permite" (Red43, 9-dic).
- **Entorno y acceso:** valle sin rutas, con pobladores dispersos.
  - El combate fue indirecto por "combustible vegetal pesado encendido" y topografía difícil.
  - El humo impidió operar con aviones algunos días (ANB).
- **Evacuaciones y viviendas:** no se publicaron; quedan **sin confirmar**.
- **Desde cuándo limita el combate:** hubo combate desde el primer día, pero el crecimiento siguió diez días: el área FIRMS crece hasta el 11-dic.

## Particularidades

- **Rayo y latencia:** inicio latente por rayo, un día sin detección satelital.
- **Quemas previas:** re-quema la cicatriz del complejo de 2015 (Cerro Plataforma / Del Morro).
  - ANB describe "renovales de un incendio anterior de 2015".
  - Según igniteinsights, el 82 % de la máscara es "Remanente de disturbio reciente" en CCS-BAP 2017.
- **Crecimiento lento:** diez días hasta ~2.000 ha de máscara.
- **Máscara chica:** 1.969 ha contra 3.000 ha publicadas.
  - Hipótesis: sotobosque quemado bajo el umbral dNBR, **sin confirmar**.
  - El área FIRMS (6.346 ha) sobreestima por el píxel de 375 m.
- **Baja confirmación MODIS MCD64A1 (53 %):** es fragmentación, no error de máscara.
  - MCD64A1 marca como no quemado (QA válido) el lóbulo oeste: `component-001`, 302 ha, 206 detecciones VIIRS, 6 % confirmado.
  - También los 9 componentes chicos del este (7–62 ha, 0 % confirmado).
  - Su dNBR (mediana 0,42) es igual al del componente principal (0,43), que confirma un 71 %.
  - La cicatriz es irregular: sólo el 30 % del área cae en celdas de 500 m quemadas en más de un 75 %, contra 66–68 % en Epuyén 2025 y Los Alerces 2024.
  - A igual fracción de celda quemada, confirma algo menos que esos eventos: 88 % contra 96–98 % en celdas casi llenas. Ese resto queda **sin explicar**; podría deberse al humo o al rebrote de 2015.
- **Fuente dudosa en la config:** la nota de argentina.gob.ar citada en `reference.sources` ("Incendio en el valle de El Turbio") habla de 380 ha en el cerro Cubridor. Parece ser el incendio "Del Morro" de 2015 (387,3 ha, programa provincial de restauración), no este: **sin confirmar**.

## Uso como referencia

- **Horizonte de crecimiento libre:** no hay: el incendio crece bajo combate hasta el 11-dic.
  - Área FIRMS: 70 ha el 2-dic, 1.389 el 4, 2.732 el 6, 3.911 el 8, 5.578 el 10 y 6.346 el 11-dic; después se estanca.
  - igniteinsights usa el tope de 120 h (~50 %).
- **Cicatriz dentro del horizonte:** 1.100 de 1.969 ha (56 %), al horizonte de 120 h.
- **Advertencias:**
  - Un modelo sin supresión sobre-propaga aquí 4–7×.
  - El combustible real es rebrote de 10 años sobre la cicatriz de 2015: un mapa que lo trate como pastizal-arbustal acelera el fuego.
  - La máscara subestima el área publicada en ~1/3.

## Fuentes

- Red43, 4-dic-2025: [Brigadistas y aviones hidrantes en plena batalla contra las llamas](https://www.red43.com.ar/nota/2025-12-4-9-4-28-incendio-en-el-turbio-brigadistas-y-aviones-hidrantes-en-plena-batalla-contra-las-llamas)
- Red43, 9-dic-2025: [Más de 110 personas trabajan en un operativo complejo y en expansión](https://www.red43.com.ar/nota/2025-12-9-10-2-11-incendio-en-el-turbio-mas-de-110-personas-trabajan-en-un-operativo-complejo-y-en-expansion)
- ANB, 10-dic-2025: [Más de 3 mil hectáreas arrasadas por el fuego en El Turbio](https://www.anbariloche.com.ar/noticias/2025/12/10/101303-mas-de-3-mil-hectareas-arrasadas-por-el-fuego-en-el-turbio)
- Red43, 18-dic-2025: [El incendio en El Turbio fue controlado en un 90 %](https://www.red43.com.ar/nota/2025-12-18-10-39-49-alivio-el-incendio-en-el-turbio-fue-controlado-en-un-90)
- argentina.gob.ar, sin fecha, citada en la config: [Incendio en el valle de El Turbio](https://www.argentina.gob.ar/noticias/incendio-en-el-valle-de-el-turbio)
- igniteinsights: `benchmarks/casos/el-turbio-2025/cadena-horizonte.json`, `benchmarks/diagnosticos/el-turbio-2025.json` y `RESULTADOS-CSS-BAP.md` §3.2, §7.2 y §7.3.
