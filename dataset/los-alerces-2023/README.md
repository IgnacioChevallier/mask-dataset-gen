# Población Rosales II, Los Alerces 2023

**Clasificación:** combatido cerca de poblados/rutas.

Términos y método comunes a todos los incendios: [README principal](../../README.md#uso-como-referencia-de-propagación).
Verificado contra las fuentes el 29-sep-2026.

## Resumen

- **Nombre:** incendio "Población Rosales II", Parque Nacional Los Alerces (Chubut).
- **Inicio:** sábado 4-feb-2023, 22 h ART.
- **Control:** 12-feb-2023 (Red43).
- **Superficie oficial:** 1.160 ha (informe mensual SNMF, feb-2023); un parte diario posterior y Red43 dan 1.390 ha.
- **Máscara del run vigente:** 1.067 ha.
- **Run vigente:** `event-filter-002`.

## Ignición

- **Fecha y hora:** sábado 4-feb-2023 a las 22 h ("El sábado a las 22 hs se declaró un incendio denominado Población Rosales II", parte citado por Red43, 5-feb-2023).
- **Lugar:** Población Rosales, junto a Laguna Larga, dentro del parque.
- **Causa:** "presuntamente intencional" (Red43, 12-feb-2023).
- **Coordenada del run:** -42,8825 / -71,576667, tomada de los partes del SNMF. Es la documentada: cae 124 m dentro de la cicatriz, a 801 m de altura y a 723 m de las primeras detecciones VIIRS.

## Combate y supresión

- **Recursos:**
  - Primer día: 40 brigadistas del parque y del SPMF, tres medios aéreos y un helicóptero.
  - 6-feb: unas 100 personas, un Chinook, dos aviones hidrantes y otro helicóptero con helibalde, más maquinaria vial para cortafuegos.
- **Entorno:** asentamiento de pobladores (Población Rosales) y prestadores turísticos dentro del parque.
- **Evacuaciones y daños:**
  - Se evacuó a pobladores y a quienes estaban en los prestadores turísticos.
  - Hubo "infraestructura afectada" y "viviendas afectadas" según los títulos de Red43, sin cifra: el número de viviendas queda **sin confirmar**.
- **Desde cuándo limita el combate:** el área FIRMS deja de crecer el 7-feb, a las ~54 h. Desde ahí hubo liquidación y combate hasta el control del 12-feb.

## Particularidades

- **Viento:** el 5-feb el incendio estaba "activo y en condiciones extremas" (Red43).
- **Duración:** el crecimiento duró unos 3 días. Es el caso más limpio del dataset: la cicatriz dentro del horizonte es prácticamente la cicatriz entera.
- **Evento vecino:** la misma nota del 12-feb informa otro incendio en el Lago Cholila, de ~500 ha. Queda fuera de la ROI (unos 40 km al norte).
- **Detección satelital:** la cicatriz no tiene problemas de observación: la cobertura válida es del 100 %.

## Uso como referencia

- **Horizonte de crecimiento libre:** ~54 h, hasta el 7-feb, cuando el área FIRMS deja de crecer.
  - Área FIRMS acumulada: 777 ha el 5-feb, 1.207 el 6-feb, 2.059 el 7-feb, 2.084 el 8-feb y 2.089 el 9-feb.
  - igniteinsights usa 72 h.
- **Cicatriz dentro del horizonte:** 1.056 de 1.067 ha (99 %).
- **Advertencias:**
  - La máscara da 1.067 ha, contra 1.160 ha del SNMF y 1.390 ha del parte posterior: puede faltar borde de baja severidad.
  - Después de las 54 h, el perímetro lo fija el combate, no la propagación.

## Fuentes

- Red43, 5-feb-2023: [El incendio del PNLA continúa activo y hay viviendas afectadas](https://www.red43.com.ar/nota/2023-2-5-23-49-1-el-incendio-del-pnla-continua-activo-y-hay-viviendas-afectadas)
- Red43, 5-feb-2023: [El incendio del PNLA está activo y en condiciones extremas](https://www.red43.com.ar/nota/2023-2-5-13-3-14-el-incendio-del-pnla-esta-activo-y-en-condiciones-extremas)
- Red43, 6-feb-2023: [Varios medios aéreos y alrededor de 100 personas combaten las llamas](https://www.red43.com.ar/nota/2023-2-6-10-20-16-varios-medios-aereos-y-alrededor-de-100-personas-combaten-las-llamas-en-el-p-n-los-alerces)
- Red43, 12-feb-2023: [Brigadistas controlaron el incendio en cercanías del Parque "Los Alerces"](https://www.red43.com.ar/nota/2023-2-12-20-36-6-brigadistas-controlaron-incendio-en-cercanias-del-parque-los-alerces)
- SNMF, feb-2023: [Informe de ocurrencia, febrero de 2023](https://www.argentina.gob.ar/sites/default/files/2022/08/informe_ocurrencia_mes_febrero_2023.pdf)
- SNMF, 1-mar-2023: [Reporte diario](https://www.argentina.gob.ar/sites/default/files/2022/08/reporte_diario_01-03-2023.pdf)
- igniteinsights: `benchmarks/diagnosticos/los-alerces-2023.json` (área FIRMS) y `RESULTADOS-CSS-BAP.md` §2.9 y §3.2.
