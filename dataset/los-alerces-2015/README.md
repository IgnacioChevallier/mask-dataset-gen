# Los Alerces, cordón Situación 2015

**Clasificación:** combatido cerca de poblados/rutas. La villa está a ~5 km y hubo operación aérea; la zona intangible queda **sin confirmar**.

Términos y método comunes a todos los incendios: [README principal](../../README.md#uso-como-referencia-de-propagación).
Verificado contra las fuentes el 29-sep-2026.

## Resumen

- **Nombre:** incendio del Parque Nacional Los Alerces, margen del Lago Futalaufquen (cordón Situación).
- **Inicio:** lunes 23-mar-2015. La config usa 2015-03-22.
- **Control:** 27/28-mar-2015, "no hay propagación" (Diario de Cuyo, 28-mar-2015).
- **Superficie oficial:**
  - ~1.500 ha (prensa, valor aproximado de la config).
  - Más de 2.000 ha el 28-mar (Diario de Cuyo, citando al Plan Nacional de Manejo del Fuego).
- **Máscara del run vigente:** 1.202 ha.
- **Run vigente:** `event-filter-001`.

## Ignición

- **Fecha:** el 23-mar-2015 "se desató hoy" (Perfil). Infobae lo ubica "en la noche del lunes".
- **Hora:** no publicada; queda **sin confirmar**.
- **Lugar:** margen del Lago Futalaufquen, a 52 km de Esquel (Infobae). Estaba a unos 5 km del caserío de Villa Futalaufquen.
- **Causa:** intencional según el intendente del parque, Daniel Crosta: "No nos cabe duda de que alguien lo prendió" (Perfil, Infobae).
- **Coordenada del run:** -42,908 / -71,6272, primera detección VNP14A1. Cae 300 m dentro de la cicatriz y a 261 m de las primeras detecciones VIIRS; es coherente con el lugar documentado.

## Combate y supresión

- **Recursos:** tres aviones y dos helicópteros del SNMF (Infobae, Perfil).
- **Navegación:** hubo restricción de navegación en el Futalaufquen entre la cabecera sur y Punta Mattos, para que los medios aéreos cargaran agua (Perfil, según la búsqueda; igniteinsights la cita igual).
- **Entorno:** a ~5 km de Villa Futalaufquen. Infobae informa el fuego "controlado en las zonas residenciales de Villa Futalaufquen" y el foco principal extendiéndose por la margen del lago.
- **Zona intangible:** **sin confirmar**. No encontré una fuente que lo diga de este incendio.
- **Evacuaciones y viviendas:** no encontré cifras para este incendio. Las evacuaciones del 28-mar en El Desemboque son de Currumahuida.
- **Desde cuándo limita el combate:** el área FIRMS deja de crecer el 25/26-mar. El 27/28-mar se informa "sin propagación".

## Particularidades

- **Causa:** intencional según la intendencia.
- **Temporada:** fue la cola de la temporada 2015, con Cholila todavía activo.
- **Viento:** viento sur que empujaba las llamas hacia zonas habitadas (Perfil).
- **Evento vecino:** Perfil menciona un segundo foco cerca de la Laguna La Zeta, junto a Esquel, fuera de la ROI.
- **Quema posterior:** el incendio de enero de 2016 empezó en el mismo sector; según Crosta, con "similitudes" (La Nueva, 23-ene-2016).

## Uso como referencia

- **Horizonte de crecimiento libre:** ~48–72 h, hasta el 25/26-mar.
  - Área FIRMS: 125 ha el 23-mar, 1.626 el 24, 2.062 el 25 y 2.106 el 26; después, casi nada.
  - igniteinsights usa 72 h (91 %).
- **Cicatriz dentro del horizonte:** 1.147 de 1.202 ha (95 %).
- **Advertencias:**
  - Sin hora de inicio publicada: igniteinsights supone 13 h ART, antes de la primera pasada VIIRS, que ya ve 8 píxeles.
  - La máscara (1.202 ha) es menor que las cifras de prensa (1.500 a más de 2.000 ha).
  - Es Landsat 8 a 30 m.

## Fuentes

- Perfil, 23-mar-2015: [Se incendió el Parque Nacional Los Alerces y denuncian que fue "intencional"](https://www.perfil.com/noticias/sociedad/Se-incendio-el-Parque-Nacional-Los-Alerces-y-denuncian-que-fue-intencional-20150323-0038.phtml)
- Infobae, 23-mar-2015: [Hay un nuevo "incendio intencional", esta vez en el Parque Nacional Los Alerces](https://www.infobae.com/2015/03/23/1717784-chubut-hay-un-nuevo-incendio-intencional-esta-vez-el-parque-nacional-los-alerces/)
- La Nación, 23-mar-2015: [Se incendió el Parque Nacional Los Alerces y denuncian que fue "intencional"](https://www.lanacion.com.ar/sociedad/chubut-se-incendio-el-parque-nacional-los-alerces-y-denuncian-que-fue-intencional-nid1778733/)
- Diario de Cuyo, 28-mar-2015: [Está controlado el incendio en el Parque Los Alerces](https://diariodecuyo.com.ar/argentina/Esta-controlado-el-incendio-en-el-Parque-Los-Alerces-20150328-0022.html)
- Revista Cultura de Montaña, citada en la config: [Otra vez se incendió el Parque Nacional Los Alerces](https://revistadigital.culturademontania.org.ar/articulo/646cc8cffc0d3efac6f6e68e)
- igniteinsights: `benchmarks/casos/los-alerces-2015/calibracion-era5-v2.json`, `benchmarks/diagnosticos/los-alerces-2015.json` y `RESULTADOS-CSS-BAP.md` §3.2.
