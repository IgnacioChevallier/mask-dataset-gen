# Las Horquetas, Cholila 2015

**Clasificación:**

- acceso difícil / poco combatido;
- latente por rayo (**sin confirmar**);
- varios eventos en la ROI.

Términos y método comunes a todos los incendios: [README principal](../../README.md#uso-como-referencia-de-propagación).
Verificado contra las fuentes el 29-sep-2026.

## Resumen

- **Nombre:** incendio "Las Horquetas", Cholila (Chubut). Es el mayor de los incendios de Chubut de 2015.
- **Inicio:** 15-feb-2015 (Wikipedia); detección oficial el 16-feb (programa provincial de restauración).
- **Fin:** 6-abr-2015, con las lluvias de otoño desde el 4-abr, "decisivas" para apagar lo que quedaba (Wikipedia).
- **Superficie oficial:**
  - 28.960,3 ha, con islas sin quemar (programa provincial); INTA calcula 27.101 ha.
  - Más de 41.000 ha para el conjunto de la temporada (Wikipedia; "el mayor incendio registrado en el país" hasta Corrientes 2022).
- **Máscara del run vigente:** 26.763 ha.
- **Run vigente:** `event-filter-001`.

## Ignición

- **Lugar:** cerca del nacimiento del Río Tigre, a unos 40 km de Cholila, en una zona inaccesible (Página/12, 20-feb-2015).
- **Causa:** "por caída de rayos durante tormenta eléctrica" (Página/12, 20-feb-2015). La versión es discutida.
  - Wikipedia: "en ciertos sectores ... sus focos parecen haber sido provocados por la acción humana".
  - El gobernador Buzzi habló de especulación inmobiliaria en otros focos de la temporada.
- **Latencia:** un informe con "7 rayos" a comienzos de febrero y un inicio latente antes del 15-feb quedan **sin confirmar**. No encontré la fuente primaria.
- **Hora:** no publicada. La primera detección VIIRS SP es del 16-feb, 18:09 UTC, en ~-42,481 / -71,919, a 1.234 m de altura.
- **La coordenada del run no es la documentada.**
  - El run usa -42,45 / -71,7333, las coordenadas del valle del Lago Cholila.
  - Cae sobre el lago, 342 m fuera de la cicatriz y a 15,3 km de las primeras detecciones.

## Combate y supresión

- **Recursos:**
  - 200 brigadistas, 6 aeronaves, 14 autobombas y 3 helicópteros de Chile (Wikipedia).
  - 5-mar: 300 combatientes, cinco aviones hidrantes y tres helicópteros chilenos (La Nueva).
- **Acceso:** difícil. "La complejidad de este incendio es la logística, por la inaccesibilidad" (Página/12, 21-feb-2015).
- **Poblados:** lejos del foco. Luego afectó el valle del Lago Cholila; INTA registra pobladores rurales afectados.
- **Evacuaciones y viviendas:** no encontré cifras; quedan **sin confirmar**.
- **Desde cuándo limita el combate:** poco.
  - El 21-feb el perímetro estaba "contenido" con 4.500 ha, pero volvió a crecer hasta 24.900 ha al 5-mar (La Nueva).
  - Ardió hasta las lluvias de abril.

## Particularidades

- **Sequía:** en febrero de 2015 llovieron 6 mm, contra un promedio histórico de 105,5 mm (INTA).
- **Complejo con El Turbio / Cerro Plataforma:** según el programa provincial, en El Turbio "fue quemada una amplia superficie ... desde la base del cerro Plataforma llegando hasta las Horquetas".
  - Las ROIs de los dos eventos se superponen.
  - El filtro clasificó 9.040 ha como `otro_incendio_probable`.
- **Crecimiento en saltos:** 8.000 ha FIRMS el 18-feb, en un día.
- **Detección satelital:** buena; el 97 % de las detecciones cercanas cae en la cicatriz.

## Uso como referencia

- **Horizonte de crecimiento libre:** el área FIRMS crece hasta el 6-mar, ~19 días, y después suma poco hasta el 30-mar.
  - Área FIRMS: 44 ha el 16-feb, 415 el 17, 8.439 el 18, 12.693 el 21, 22.901 el 25-feb y 31.238 el 6-mar.
  - La caja incluye parte del complejo El Turbio.
  - igniteinsights usa el tope de 120 h (39 % del área FIRMS).
- **Cicatriz dentro del horizonte:** 6.959 de 26.763 ha (26 %).
- **Advertencias:**
  - Es el caso más cercano a una propagación libre, pero de semanas y con un clima que cambia.
  - Usar la primera detección VIIRS como ignición, no la coordenada del valle.
  - Revisar el límite con Cerro Plataforma: las dos cicatrices se tocan.
  - Es Landsat 8 a 30 m.

## Fuentes

- Página/12, 20-feb-2015: [Fuego sin control en Chubut](https://www.pagina12.com.ar/diario/sociedad/3-266521-2015-02-20.html)
- Página/12, 21-feb-2015: [Danza por la lluvia en Chubut](https://www.pagina12.com.ar/diario/sociedad/3-266602-2015-02-21.html)
- La Nueva, 5-mar-2015: [Se detuvo el avance del incendio en Cholila, pero se reavivó un foco en Lago Puelo](https://www.lanueva.com/nota/2015-3-5-16-25-0-se-detuvo-el-avance-del-incendio-en-cholila-pero-se-reavivo-un-foco-en-lago-puelo)
- CONAE, citada en la config: [Incendios Cholila, Chubut – Landsat 8 OLI, 3 de marzo de 2015](https://www.argentina.gob.ar/ciencia/conae/educacion-y-formacion-masiva/materiales-educativos/incendios-cholila-chubut-landsat-8-oli-3-de-marzo-de-2015)
- Gobierno del Chubut, sep-2015: [Programa de restauración de las áreas afectadas por grandes incendios forestales en Chubut 2014-2015](https://bosques.chubut.gov.ar/wp-content/uploads/2023/08/Programa-de-restauracion-de-las-areas-afectadas-por-grandes-incendios-forestales-en-Chubut-en-2014-2015.pdf)
- INTA, 2015: [Severidad del daño causado por el fuego en los incendios de "La Horqueta", "El Turbio" y "Desemboque"](https://sipas.inta.gob.ar/sites/default/files/archivos/INTA_da%C3%B1o_fuego_cholila_2015.pdf)
- Wikipedia, consultada el 29-sep-2026: [Incendios forestales en Chubut de 2015](https://es.wikipedia.org/wiki/Incendios_forestales_en_Chubut_de_2015)
- igniteinsights: `benchmarks/casos/cholila-2015/calibracion-era5-v2.json`, `benchmarks/diagnosticos/cholila-2015.json` y `RESULTADOS-CSS-BAP.md` §3.2 y §7.1.
