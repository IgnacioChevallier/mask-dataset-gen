# Cerro Plataforma, El Turbio 2015

**Clasificación:**

- latente por rayo;
- varios eventos en la ROI;
- acceso difícil / poco combatido (**sin confirmar**).

**No usar como referencia de propagación:** la fecha de inicio es incierta en semanas y la referencia se mezcla con Cholila.

Términos y método comunes a todos los incendios: [README principal](../../README.md#uso-como-referencia-de-propagación).
Verificado contra las fuentes el 29-sep-2026.

## Resumen

- **Nombre:** incendio "Cerro Plataforma", zona El Turbio (Chubut).
- **Inicio:** detectado el 3-feb-2015 (programa provincial).
- **Control:** contradictorio.
  - Página/12 lo da por "controlado", con guardia de cenizas, el 20-feb-2015.
  - Al día siguiente, la misma publicación dice que El Turbio "continúa descontrolado y avanza".
  - La Nueva informa 10.000 ha en El Turbio el 5-mar.
- **Superficie oficial:** 7.371,3 ha, con islas sin quemar (programa provincial); INTA calcula 7.407 ha.
- **Máscara del run vigente:** 6.292 ha.
- **Run vigente:** `event-filter-001`.

## Ignición

- **Lugar y causa:** "hay en realidad dos incendios, uno que se declaró en la zona de Tres Picos y otro más abajo, en un cerro que conocemos como Plataforma". Se atribuyen a un rayo en tormenta eléctrica, "hace dos semanas" (Página/12, 20-feb-2015), es decir, a comienzos de febrero.
- **Hora:** no publicada.
- **La coordenada del run no es la documentada.**
  - El run usa -42,294 / -71,869, el centroide de la cicatriz MODIS: cae sobre suelo no combustible, 297 m fuera de la cicatriz.
  - No hay coordenadas oficiales del foco.

## Combate y supresión

- **Recursos:**
  - Brigadas de Defensa Civil en El Turbio (La Nueva, 3-feb).
  - El 20/21-feb cayó una avioneta que combatía el fuego y el piloto resultó herido (Página/12; El Chubut).
- **Acceso:** el valle de El Turbio no tiene rutas y el acceso es difícil. No lo confirmé con una fuente de 2015: **sin confirmar**.
- **Poblados:** INTA registra 16 pobladores rurales afectados en la zona El Turbio.
- **Evacuaciones:** no encontré cifras.
- **Desde cuándo limita el combate:** no definible.

## Particularidades

- **Rayo y latencia:** inicio por rayo a comienzos de febrero. La primera detección VIIRS es del 17-feb, 14 días después del inicio oficial.
- **Complejo con Cholila:** según el programa provincial, en El Turbio "fue quemada una amplia superficie ... desde la base del cerro Plataforma llegando hasta las Horquetas".
  - Las ROIs se superponen y el área FIRMS de este evento crece al ritmo de Cholila (4.466 ha el 18-feb).
  - El filtro clasificó 237 ha como `otro_incendio_probable`.
- **Evento vecino:** el incendio "Del Morro" (detectado el 29-ene, 387,3 ha, mayormente en el PN Lago Puelo) es de la misma zona El Turbio (programa provincial).
- **Quemas posteriores:** esta cicatriz se re-quemó en el incendio El Turbio de 2025.

## Uso como referencia

- **Horizonte de crecimiento libre:** no definible.
  - Área FIRMS: 207 ha el 17-feb, 4.466 el 18, 6.476 el 21, 9.563 el 25-feb y 12.372 el 6-mar, junto con el complejo Cholila.
  - igniteinsights lo excluye.
- **Cicatriz dentro del horizonte:** no calculada.
- **Advertencias:**
  - La hora de inicio es incierta en semanas.
  - La referencia probablemente está mezclada con Cholila.
  - La semilla está fuera de la cicatriz.
  - No usar para validar propagación.

## Fuentes

- La Nueva, 3-feb-2015: [Los incendios en la zona de Lago Puelo siguen sin control](https://www.lanueva.com/nota/2015-2-3-1-7-0-los-incendios-en-la-zona-de-lago-puelo-siguen-sin-control)
- Página/12, 20-feb-2015: [Fuego sin control en Chubut](https://www.pagina12.com.ar/diario/sociedad/3-266521-2015-02-20.html)
- Página/12, 21-feb-2015: [Danza por la lluvia en Chubut](https://www.pagina12.com.ar/diario/sociedad/3-266602-2015-02-21.html)
- El Chubut, 21-feb-2015: [Cayó avioneta que combatía incendios en Chubut](https://www.elchubut.com.ar/policiales/2015-2-21-cayo-avioneta-que-combatia-incendios-en-chubut-y-el-piloto-sufrio-heridas-leves)
- La Nueva, 5-mar-2015: [Se detuvo el avance del incendio en Cholila, pero se reavivó un foco en Lago Puelo](https://www.lanueva.com/nota/2015-3-5-16-25-0-se-detuvo-el-avance-del-incendio-en-cholila-pero-se-reavivo-un-foco-en-lago-puelo)
- Gobierno del Chubut, sep-2015: [Programa de restauración de las áreas afectadas por grandes incendios forestales en Chubut 2014-2015](https://bosques.chubut.gov.ar/wp-content/uploads/2023/08/Programa-de-restauracion-de-las-areas-afectadas-por-grandes-incendios-forestales-en-Chubut-en-2014-2015.pdf)
- INTA, 2015: [Severidad del daño causado por el fuego en los incendios de "La Horqueta", "El Turbio" y "Desemboque"](https://sipas.inta.gob.ar/sites/default/files/archivos/INTA_da%C3%B1o_fuego_cholila_2015.pdf)
- igniteinsights: `benchmarks/diagnosticos/cerro-plataforma-2015.json` y `RESULTADOS-CSS-BAP.md` §3.2.
