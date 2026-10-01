# Currumahuida – Lago Puelo 2015

**Clasificación:**

- combatido cerca de poblados/rutas;
- varios eventos en la ROI.

**No usar como referencia de propagación:** incendio de varias fases sin ignición definida.

Términos y método comunes a todos los incendios: [README principal](../../README.md#uso-como-referencia-de-propagación).
Verificado contra las fuentes el 29-sep-2026.

## Resumen

- **Nombre:** incendio "Currumahuida – Lago Puelo" (Chubut).
- **Inicio:** fecha de detección oficial 23-mar-2015 (programa provincial). Hubo fases previas desde el 28-feb.
- **Control o extinción:** no encontré la fecha; queda **sin confirmar**. Probablemente fueron las lluvias de comienzos de abril, como en el resto de la temporada.
- **Superficie oficial:** 3.150,8 ha, con islas sin quemar (programa provincial); INTA calcula 3.162 ha.
- **Máscara del run vigente:** 4.236 ha, más que la superficie oficial.
- **Run vigente:** `event-filter-001`.

## Ignición

- **Fases documentadas:**
  - **28-feb:** incendio en un camping del Parque Nacional Lago Puelo, junto al espigón; se trabajó para que no cruzara al cerro Currumahuida (La Nueva, 28-feb-2015).
  - **5-mar:** "se reactivó un foco en el cerro Currumahuida", con 40 brigadistas y apoyo aéreo (La Nueva, 5-mar-2015).
  - **23-mar:** fecha de detección oficial del incendio con este nombre.
  - **28-mar:** el fuego avanza "por la ladera del cerro Currumahuida" y se evacúan unas 30 familias de El Desemboque (La Nueva, 28-mar-2015).
- **Origen el 28-feb "desde El Desemboque": sin confirmar.** La Nueva ubica el foco del 28-feb en un camping del PN Lago Puelo.
- **Causa:** el gobernador Buzzi atribuyó a intereses inmobiliarios tres de los cinco focos del cerro Currumahuida y Lago Puelo (Wikipedia). No es una pericia.
- **La coordenada del run no es la documentada.**
  - El run usa -42,185 / -71,553, el centroide de la cicatriz MODIS, a 6,9 km de las primeras detecciones.
  - No hay coordenada oficial.

## Combate y supresión

- **Evacuaciones:**
  - 28-feb: Villa del Lago, unas 500 familias a menos de 1 km del foco.
  - 28-mar: unas 30 familias de El Desemboque.
  - También el cordón Currumahuida.
- **Recursos:** 40 brigadistas y apoyo aéreo el 5-mar. El 28-mar La Nueva menciona "más de 300 brigadistas" con aviones y helicópteros, en una nota que mezcla este incendio con el de Los Alerces.
- **Entorno:** interfaz de Lago Puelo, El Hoyo y El Desemboque.
- **Desde cuándo limita el combate:** no se puede separar; el incendio tuvo varias fases, todas combatidas.

## Particularidades

- **Varias fases y focos:** 28-feb, 5-mar, 23-mar y 28-mar.
- **Ventana PRE (15-feb a 22-mar):** contiene las fases de febrero y comienzos de marzo. La máscara ve sólo lo que ardió desde el 23-mar.
- **Eventos vecinos:** la cicatriz de Desemboque (enero de 2015) está en la misma ladera.
- **Crecimiento en dos pulsos:** área FIRMS de 1.680 ha el 24-mar a 2.134 el 27-mar, y un salto a 4.657 ha el 28-mar.
- **Máscara más grande que lo oficial:** 4.236 contra 3.150,8 ha. La diferencia **no está explicada**.

## Uso como referencia

- **Horizonte de crecimiento libre:** no definible, por las fases múltiples.
  - Área FIRMS: 1.680 ha el 24-mar, 2.134 el 27, 4.657 el 28, 6.313 el 30 y 6.356 el 31-mar.
  - igniteinsights lo excluye.
- **Cicatriz dentro del horizonte:** no calculada.
- **Advertencias:**
  - Sin ignición única ni horizonte definido.
  - La máscara no se corresponde con la superficie oficial.
  - No usar para validar propagación.

## Fuentes

- La Nueva, 28-feb-2015: [Incendios: ordenan evacuar una villa cercana a Lago Puelo](https://www.lanueva.com/nota/2015-2-28-21-21-0-incendios-ordenan-evacuar-una-villa-cercana-a-lago-puelo)
- La Nueva, 5-mar-2015: [Se detuvo el avance del incendio en Cholila, pero se reavivó un foco en Lago Puelo](https://www.lanueva.com/nota/2015-3-5-16-25-0-se-detuvo-el-avance-del-incendio-en-cholila-pero-se-reavivo-un-foco-en-lago-puelo)
- La Nueva, 28-mar-2015: [Los Alerces y Lago Puelo: hay más evacuados por el avance del incendio](https://www.lanueva.com/nota/2015-3-28-1-3-0-los-alerces-y-lago-puelo-hay-mas-evacuados-por-el-avance-del-incendio)
- Gobierno del Chubut, sep-2015: [Programa de restauración de las áreas afectadas por grandes incendios forestales en Chubut 2014-2015](https://bosques.chubut.gov.ar/wp-content/uploads/2023/08/Programa-de-restauracion-de-las-areas-afectadas-por-grandes-incendios-forestales-en-Chubut-en-2014-2015.pdf)
- Wikipedia, consultada el 29-sep-2026: [Incendios forestales en Chubut de 2015](https://es.wikipedia.org/wiki/Incendios_forestales_en_Chubut_de_2015)
- igniteinsights: `benchmarks/diagnosticos/currumahuida-2015.json` y `RESULTADOS-CSS-BAP.md` §3.2.
