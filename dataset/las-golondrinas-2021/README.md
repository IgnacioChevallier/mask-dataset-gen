# Las Golondrinas – Cerro Radal 2021

**Clasificación:**

- combatido cerca de poblados/rutas: fue en la interfaz, aunque el combate no frenó la primera noche;
- varios eventos en la ROI.

Términos y método comunes a todos los incendios: [README principal](../../README.md#uso-como-referencia-de-propagación).
Verificado contra las fuentes el 29-sep-2026.

## Resumen

- **Nombre:** incendio "Cerro Radal y Las Golondrinas" (Lago Puelo y El Hoyo, Chubut).
- **Inicio:** martes 9-mar-2021, ~15 h ART.
- **Extinción:** declarada por el SPMF el 14-abr-2021 (Red43).
- **Superficie oficial:** 12.959 ha (SNMF, informe de áreas quemadas al 23-mar-2021). La config usa 12.901 ha, del balance oficial citado por Red43.
- **Máscara del run vigente:** 10.656 ha.
- **Run vigente:** `event-filter-001`.

## Ignición

- **Dos focos el 9-mar-2021**, según la pericia de la Policía Federal (elDiarioAR, mar-2022):
  - **Las Golondrinas, 15 h:** "incidencia térmica de líneas aéreas de media tensión" sobre coníferas vecinas.
  - **Cerro Radal (Lago Puelo), 30–40 min después:** "un elemento capaz de generar llama libre".
  - Los peritos descartaron el uso de acelerantes. No descartaron la intervención humana en Cerro Radal.
- **Hora según Radio Nacional:** "alrededor de las 16 h" en los dos lugares (según igniteinsights; no la verifiqué).
- **La coordenada del run no es la documentada.**
  - El run usa -42,084 / -71,371, el centroide de la cicatriz MODIS: está a 1.388 m de altura y a 7,9 km de las primeras detecciones.
  - Los focos documentados son Las Golondrinas (~-42,015 / -71,533) y Cerro Radal (~-42,033 / -71,566).
  - Los dos caen 600–800 m fuera de la cicatriz dNBR, en zona de viviendas.

## Combate y supresión

- **Entorno:** interfaz urbano-forestal (Las Golondrinas, Cerro Radal, Lago Puelo, El Hoyo) sobre la Ruta 40, a la que llegaron las llamas el mismo 9-mar (Red43).
- **Viviendas:** "el incendio alcanzó, en un par de horas, total o parcialmente 605 viviendas, 107 talleres y 135 galpones". Es el informe oficial leído por el intendente de Lago Puelo (Revista Cítrica, 9-mar-2022).
- **Evacuaciones:** hubo cientos de evacuados (Diario Río Negro); la cifra exacta queda **sin confirmar**.
- **Recursos:** no encontré cifras de brigadistas ni de medios aéreos; quedan **sin confirmar**. El incendio afectó la base del SNMF en Las Golondrinas (El Cordillerano).
- **Desde cuándo limita el combate:** el crecimiento principal ocurrió la primera noche, cuando el combate no podía frenarlo.

## Particularidades

- **Varios focos:** dos, con 30–40 minutos de diferencia.
- **Viento:**
  - Red43 informa ráfagas de hasta 90 km/h y un verano seco y caluroso.
  - La ráfaga del norte de 54 km/h de media horaria a las 00 UTC del 10-mar (estación El Bolsón) sale del análisis de igniteinsights con Meteostat; no la verifiqué contra una fuente publicada: **sin confirmar**.
- **Eventos vecinos:**
  - El incendio "El Boquete" (8.818 ha, Río Negro) empezó el 7-mar-2021 (SNMF).
  - La ventana PRE arranca en febrero para dejar fuera Cuesta del Ternero (enero de 2021).
  - El filtro clasificó 3.983 ha como `otro_incendio_probable`.
- **VIIRS casi no lo vio:** 6 píxeles la primera tarde (19:49 UTC) y 1 en la pasada nocturna, para ~10.000 ha.
  - Ardió entre dos pasadas.
  - Que haya ardido bajo el humo de El Boquete es una hipótesis **sin confirmar**. El informe del SNMF muestra una pluma de humo de este incendio el 13-mar.

## Uso como referencia

- **Horizonte de crecimiento libre:** la primera noche, del 9 al 10-mar. Con un satélite ciego, manda la cronología: 605 viviendas "en un par de horas" y casi sin detecciones posteriores.
  - El área FIRMS no sirve: 162 ha el 9-mar y 1.355 el 10-mar, contra ~10.600 ha de máscara.
  - igniteinsights usa 48 h (82 % en la primera noche) y puntúa contra la cicatriz completa.
- **Cicatriz dentro del horizonte:** 10.622 de 10.656 ha (~100 %), por cronología y no por detecciones.
- **Advertencias:**
  - No truncar la cicatriz con FIRMS: quedarían 853 ha.
  - Usar los dos focos documentados, no el centroide MODIS del run.
  - El viento del modelo global (GFS) no tiene la ráfaga nocturna: ninguna receta de igniteinsights pasa de sesgo 0,07.

## Fuentes

- Red43, 9-mar-2021: [Incendio en Cerro Radal: las llamas llegaron a la Ruta 40](https://www.red43.com.ar/nota/2021-3-9-20-52-28-incendio-en-cerro-radal-las-llamas-llegaron-a-la-ruta-40)
- El Cordillerano, 9-mar-2021: [El incendio de Las Golondrinas afectó la base del SNMF](https://www.elcordillerano.com.ar/noticias/2021/03/09/104918-el-incendio-de-las-golondrinas-afecto-la-base-del-servicio-nacional-de-manejo-del-fuego)
- Radio Nacional, 9-mar-2021: [Grave incendio en las Golondrinas y Cerro Radal](https://www.radionacional.com.ar/grave-incendio-en-las-golondrinas-y-cerro-radal/)
- Diario Río Negro, mar-2021: [Cinco incendios arrasan casas y chacras en la Comarca Andina](https://www.rionegro.com.ar/la-comarca-andina-sitiada-por-varios-incendios-1721003/)
- Red43, 14-abr-2021: [El incendio en Las Golondrinas se encuentra extinguido](https://www.red43.com.ar/nota/2021-4-14-9-7-37-el-incendio-en-las-golondrinas-se-encuentra-extinguido)
- MAyDS / SNMF, datos al 23-mar-2021: [Informe de áreas quemadas, incendios "Las Golondrinas" y "El Boquete"](https://www.argentina.gob.ar/sites/default/files/2020/12/informe_aq_rio_negro_chubut_07may2021.pdf)
- elDiarioAR, mar-2022: [Las pericias apuntan a una falla en el sistema eléctrico](https://www.eldiarioar.com/sociedad/incendios-patagonia-pericias-apuntan-falla-sistema-electrico_1_8192107.amp.html)
- Revista Cítrica, 9-mar-2022: [Comarca Andina: cenizas, dolores y promesas quedan](https://revistacitrica.com/comarca-andina-cenizas-incendio-un-ano.html)
- Wikipedia, citada en la config: [2021 Argentine Patagonia wildfires](https://en.wikipedia.org/wiki/2021_Argentine_Patagonia_wildfires)
- igniteinsights: `benchmarks/casos/las-golondrinas-2021/calibracion-v2.json`, `benchmarks/diagnosticos/las-golondrinas-2021.json` y `RESULTADOS-CSS-BAP.md` §2.10, §2.12 y §7.1.
