# Puerto Patriada 2026

**Clasificación:**

- combatido cerca de poblados/rutas;
- varios eventos en la ROI.

Términos y método comunes a todos los incendios: [README principal](../../README.md#uso-como-referencia-de-propagación).
Verificado contra las fuentes el 29-sep-2026.

## Resumen

- **Nombre:** incendio de Puerto Patriada (El Hoyo), con avance sobre Epuyén (Chubut).
- **Inicio:** tarde del lunes 5-ene-2026.
- **Contención:** 15/16-ene-2026, con 14.770 ha (Infobae, 16-ene-2026).
- **Reactivación y extinción:** se reactivó desde el 19-ene y se declaró extinguido a fines de marzo, con más de 30.000 ha (La Nación, 14-abr-2026).
- **Superficie oficial:** 14.770 ha al contenerse; más de 30.000 ha hasta la extinción.
- **Máscara del run vigente:** 24.513 ha.
- **Run vigente:** `event-filter-001`.

## Ignición

- **Fecha y hora:** "alrededor de la tarde del lunes 5 de enero". El foco inicial se detectó hacia las 14:30 (Wikipedia).
  - A las 15:42 Red43 ya informaba el cierre preventivo de Puerto Patriada "por principio de incendio".
- **Causa:** intencional. La fiscalía halló acelerante (combustible) en el lugar de inicio (Infobae, 10-ene-2026).
- **Coordenada del run:** -42,148083 / -71,534694, la localidad de Puerto Patriada. Cae 150 m fuera de la cicatriz.
  - La nota de la config dice que las primeras detecciones están "a ~2 km al norte", pero el diagnóstico las ubica a 267 m.
  - igniteinsights usa la celda interior más cercana: -42,14589 / -71,53471.

## Combate y supresión

- **Recursos:**
  - 10-ene: 479 personas (Diario Río Negro).
  - Al contenerse: 551 brigadistas y ocho medios aéreos, entre ellos un Boeing 737 Fireliner (Infobae, 16-ene).
- **Entorno:** interfaz urbano-forestal (Puerto Patriada, El Hoyo, Epuyén, El Coihue, La Angostura) y Ruta 40, cortada varias veces.
- **Evacuaciones:** más de 3.000 personas entre el 5 y el 6-ene. El 8/9-ene se evacuaron El Pedregoso, callejón Núñez y Aldea San Francisco, y el 10-ene La Angostura y El Coihue.
- **Viviendas:** 32 destruidas (C5N, 16-ene-2026).
- **Desde cuándo limita el combate:** hubo combate intenso desde el día 1. Se declaró contenido el 15/16-ene, con 22 de 32 sectores controlados el 12/13-ene y reactivaciones.

## Particularidades

- **Causa:** intencional, con acelerante.
- **10-ene, avance hacia El Coihue / Epuyén:** el fuego cruzó la Ruta 40 en Los Paredones.
  - "Otros focos": **sin confirmar**. La prensa atribuye El Coihue y La Angostura al "avance del incendio forestal iniciado en la zona de Puerto Patriada" (Mundo Empresarial / Gobierno del Chubut).
  - Lo que sí muestran los datos: el área FIRMS salta de 13.386 a 28.038 ha en un día, con grupos de detecciones al este (lon −71,25).
- **Por qué la máscara (24.513 ha) supera las 14.770 ha oficiales:**
  - la ventana POST empieza el 1-feb, así que incluye las reactivaciones del 19 al 26-ene en Epuyén (La Nación, 19-ene);
  - también incluye el crecimiento posterior a la contención.
  - La máscara mezcla fases, y probablemente focos distintos.
- **Varios eventos en la ROI:** la config tiene tres ROIs, una de ellas sobre Puerto Café. El filtro clasificó 40.744 ha como `otro_incendio_probable`.
- **Ventana POST sin margen:** empieza el mismo día en que dejan de aparecer detecciones (última: 1-feb).

## Uso como referencia

- **Horizonte de crecimiento libre:** 96 h, hasta el 9-ene, antes del salto del 10-ene.
  - Área FIRMS: 160 ha el 5-ene, 6.187 el 6, 10.157 el 7, 10.506 el 8, 13.386 el 9, 28.038 el 10 y 29.653 el 15.
  - Después, reactivaciones hasta 43.576 ha en la caja.
- **Cicatriz dentro del horizonte:** 5.726 de 24.513 ha (23 %).
- **Advertencias:**
  - No usar la cicatriz completa como resultado de una propagación desde Puerto Patriada.
  - Truncar antes del 10-ene.
  - La supresión fue intensa y temprana en la interfaz: incluso dentro del horizonte, el perímetro está recortado por el combate.

## Fuentes

- Red43, 5-ene-2026: [Cerraron Puerto Patriada por principio de incendio](https://www.red43.com.ar/nota/2026-1-5-15-42-7-cerraron-puerto-patriada-por-principio-de-incendio)
- Infobae, 10-ene-2026: [La investigación confirmó hallazgos de combustible donde se inició el fuego](https://www.infobae.com/sociedad/2026/01/10/incendios-en-chubut-la-investigacion-confirmo-hallazgos-de-combustible-donde-se-inicio-el-fuego/)
- Infobae, 10-ene-2026: [Evacuaron otra localidad cercana a El Hoyo y volvieron a cerrar un tramo de la Ruta 40](https://www.infobae.com/sociedad/2026/01/10/incendios-en-chubut-evacuaron-otra-localidad-cercana-a-el-hoyo-y-volvieron-a-cerrar-un-tramo-de-la-ruta-40/)
- Diario Río Negro, 10-ene-2026: [El mapa de los incendios en la Patagonia este sábado 10 de enero](https://www.rionegro.com.ar/sociedad/en-vivo-el-mapa-de-los-incendios-en-la-patagonia-este-sabado-10-de-enero-2026-4431004/)
- Mundo Empresarial, ene-2026: [Evacuaron El Coihue y La Angostura en Epuyén y cortaron la Ruta Nacional 40](https://mundoempresarial.ar/incendios-forestales-evacuaron-el-coihue-y-la-angostura-en-epuyen-y-cortaron-la-ruta-nacional-40/)
- Infobae, 16-ene-2026: [Los brigadistas contuvieron la totalidad del fuego en Puerto Patriada](https://www.infobae.com/sociedad/2026/01/16/incendios-en-chubut-los-brigadistas-contuvieron-la-totalidad-del-fuego-en-puerto-patriada-que-afecto-a-casi-15-mil-hectareas/)
- C5N, 16-ene-2026: [Brigadistas contuvieron el fuego, que afectó más de 15 mil hectáreas](https://www.c5n.com/sociedad/brigadistas-contuvieron-el-fuego-en-Puerto-Patriada-afecto-15-mil-hectareas-16-de-enero-2026)
- La Nación, 19-ene-2026: [Se reactivaron varios focos de incendio en Epuyén](https://www.lanacion.com.ar/sociedad/fuera-de-la-capacidad-de-combate-se-reactivaron-varios-focos-de-incendio-en-epuyen-y-el-hongo-de-nid19012026/)
- La Nación, 14-abr-2026: [Tras cuatro meses de fuego, extinguen el incendio en Los Alerces](https://www.lanacion.com.ar/sociedad/tras-cuatro-meses-de-fuego-extinguen-el-incendio-en-los-alerces-epicentro-de-las-peores-temporadas-nid14042026/)
- Wikipedia, consultada el 29-sep-2026: [Incendio forestal en Chubut de 2026](https://es.wikipedia.org/wiki/Incendio_forestal_en_Chubut_de_2026)
- igniteinsights: `benchmarks/casos/puerto-patriada-2026/cadena-horizonte.json`, `benchmarks/diagnosticos/puerto-patriada-2026.json` y `RESULTADOS-CSS-BAP.md` §2.2 y §3.2.
