# Puerto Café, Los Alerces 2025–2026

**Clasificación:**

- acceso difícil / poco combatido;
- latente por rayo;
- varios eventos en la ROI.

Términos y método comunes a todos los incendios: [README principal](../../README.md#uso-como-referencia-de-propagación).
Verificado contra las fuentes el 29-sep-2026.

## Resumen

- **Nombre:** incendio "Puerto Café", Brazo Sur del Lago Menéndez, Parque Nacional Los Alerces.
- **Inicio:** detectado el martes 9-dic-2025.
- **Contención, control y extinción:** contenido el 18-feb-2026, controlado el 26-mar-2026 (Comando Unificado) y extinguido el 14-abr-2026.
- **Superficie oficial:** ~31.000 ha, sumando más de 16.000 ha en el parque y más de 15.000 ha en jurisdicción provincial (La Nación, 14-abr-2026).
- **Máscara del run vigente:** 38.236 ha.
- **Run vigente:** `event-filter-001`.

## Ignición

- **Fecha y lugar:** 9-dic-2025, en la zona intangible del Brazo Sur del Lago Menéndez (Red43, 9-dic-2025).
- **Causa:** rayo, "casi con seguridad", vinculado a "tormentas eléctricas de gran intensidad" de los días previos (parte oficial, Red43).
  - La tormenta del 29-nov queda **sin confirmar**: el parte no da fecha.
- **Coordenada del run:** -42,724 / -71,912, centroide de las primeras detecciones VIIRS del 9-dic. Coincide con el lugar documentado; no hay coordenada oficial.

## Combate y supresión

- **Recursos:**
  - Primer día: 17 brigadistas, un avión anfibio, un helicóptero con helibalde y 32 personas en total.
  - Al control: 11 personas en el lugar (Red43, 27-mar-2026).
- **Acceso:** "sector sin presencia humana ni vías de acceso", al que se llega por agua (parte oficial). Es el sector "más valioso del Parque desde el punto de vista ecológico".
- **Poblados:** lejos al principio. Desde el 21-ene el fuego entra en jurisdicción provincial: Villa Lago Rivadavia y alrededores de Cholila.
- **Evacuaciones y viviendas:** no encontré cifras; quedan **sin confirmar**.
- **Desde cuándo limita el combate:** en la fase explosiva, el combate casi no limita el crecimiento, por el acceso. El crecimiento se estanca recién a principios de febrero.

## Particularidades

- **Fase latente:** ~500 ha del 9-dic al 5-ene.
  - Red43 informa 270 ha el 17-dic.
  - El área FIRMS es de 524 ha al 5-ene.
- **Fase explosiva:** "A partir del 5 de enero ... se propagó de forma explosiva hacia los lagos Verde y Rivadavia", con altas temperaturas, viento y sequía extrema (La Nación).
- **Salida del parque:** el 21-ene cruzó el límite norte del parque (La Nación).
- **Varios eventos en la ROI:** la ROI (Menéndez–Rivadavia–Cholila) incluye otros incendios activos en enero de 2026.
  - El área FIRMS de la caja llega a 61.198 ha, contra una máscara de 38.236 ha.
  - Una semilla FIRMS de toda la caja los mezcla: en igniteinsights produjo 21.718 ha de falso positivo a 44 km. igniteinsights sólo usa detecciones a menos de 1 km de la cicatriz.
  - El filtro de evento clasificó 994 ha como `otro_incendio_probable`.
- **Máscara más grande que lo oficial:** 38.236 contra ~31.000 ha. La cifra oficial es aproximada ("más de").

## Uso como referencia

- **Horizonte de crecimiento libre:** 96 h desde el 5-ene 20 UTC, sólo la fase explosiva, sembrada con lo latente observado.
  - Área FIRMS: 524 ha el 5-ene, 4.319 el 6, 12.809 el 7, 16.208 el 8, 18.224 el 9 y 19.419 el 10.
  - Después sigue creciendo en pulsos hasta el 2-feb (60.951 ha en la caja, con otros incendios).
- **Cicatriz dentro del horizonte:** 8.832 de 38.236 ha (23 %).
- **Advertencias:**
  - No simular desde el rayo del 9-dic: 27 días latentes no son propagación.
  - No sembrar con FIRMS de toda la ROI: hay otros incendios.
  - El 77 % de la cicatriz ardió después del horizonte, casi sin combate: sirve como propagación libre de largo plazo, pero con clima cambiante.

## Fuentes

- Red43, 9-dic-2025: [Alerta en Los Alerces: combaten un incendio en la zona intangible de Lago Menéndez](https://www.red43.com.ar/nota/2025-12-9-15-25-0-alerta-en-los-alerces-combaten-un-incendio-en-la-zona-intangible-de-lago-menendez)
- Red43, 9-dic-2025: [Incendio activo en el Menéndez: parte oficial](https://www.red43.com.ar/nota/2025-12-9-17-42-35-incendio-activo-en-el-menendez-parte-oficial)
- Red43, 17-dic-2025: [El fuego afecta 270 hectáreas en zona de reserva intangible](https://www.red43.com.ar/nota/2025-12-17-14-50-0-incendio-en-el-parque-nacional-los-alerces-el-fuego-afecta-270-hectareas-en-zona-de-reserva-intangible)
- Red43, 27-mar-2026: [Controlaron el incendio en el Parque Nacional Los Alerces](https://www.red43.com.ar/nota/2026-3-27-9-6-0-controlaron-el-incendio-en-el-parque-nacional-los-alerces)
- La Nación, 28-mar-2026: [Después de tres meses y medio, logran controlar el incendio en el Parque Los Alerces](https://www.lanacion.com.ar/sociedad/temporada-catastrofica-despues-de-tres-meses-y-medio-logran-controlar-el-incendio-en-el-parque-los-nid28032026/)
- La Nación, 14-abr-2026: [Tras cuatro meses de fuego, extinguen el incendio en Los Alerces](https://www.lanacion.com.ar/sociedad/tras-cuatro-meses-de-fuego-extinguen-el-incendio-en-los-alerces-epicentro-de-las-peores-temporadas-nid14042026/)
- igniteinsights: `benchmarks/casos/puerto-cafe-2025/calibracion-v2s.json` (semilla), `benchmarks/diagnosticos/puerto-cafe-2025.json` y `RESULTADOS-CSS-BAP.md` §2.3 y §3.2.
