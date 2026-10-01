# Los Alerces, Bahía Rosales 2024

**Clasificación:** combatido cerca de poblados/rutas.

Términos y método comunes a todos los incendios: [README principal](../../README.md#uso-como-referencia-de-propagación).
Verificado contra las fuentes el 29-sep-2026.

## Resumen

- **Nombre:** incendio del Parque Nacional Los Alerces, Bahía Rosales – Arroyo Centinela (Lago Futalaufquen).
- **Inicio:** jueves 25-ene-2024, ~22:30 h ART.
- **Control:** 21-feb-2024, "en todos sus sectores", tras 27 días de combate (Los Andes, citando al Comando Unificado).
- **Extinción:** 23-mar-2024 (Infobae).
- **Superficie oficial:**
  - 5.971 ha de bosque nativo (Ministerio de Seguridad, "persona buscada"; La Nación, 18-feb-2024).
  - 6.924 ha al control (Los Andes, 21-feb-2024).
- **Máscara del run vigente:** 6.007 ha.
- **Run vigente:** `event-filter-001`.

## Ignición

- **Fecha, hora y lugar:** 25-ene-2024 "aproximadamente a las 22:30", en la "población Lucas Rosales – Arroyo Centinela" (argentina.gob.ar).
- **Causa:** "incendio provocado". Lo investiga el Juzgado Federal de Esquel y hay recompensa (argentina.gob.ar). El gobernador Torres lo confirmó como intencional (France 24, 29-ene-2024).
- **Focos:** "dos focos que se unieron" queda **sin confirmar**. La prensa habla de "focos ígneos" en plural, sin describir la unión.
- **La coordenada del run no es la documentada.**
  - El run usa -42,8036 / -71,5939, la primera detección VIIRS 375 m: está a 1.015 m de altura, a media ladera, 1 km al sur del arroyo y a 1,3 km de las primeras detecciones.
  - El arroyo Centinela, junto a las primeras detecciones, está en ~-42,8035 / -71,6211.
  - igniteinsights usa la celda de la cicatriz más cercana: -42,80381 / -71,61425, a 721 m de altura.

## Combate y supresión

- **Recursos:**
  - 5-feb: 271 brigadistas, 114 personas de apoyo, tres helicópteros, dos aviones hidrantes y un avión de observación, con maquinaria vial (Infobae, 5-feb-2024).
  - Al control: 259 personas, 155 de ellas brigadistas (Los Andes).
- **Entorno:** población rural dentro del parque (Lucas Rosales, Bahía Rosales) y familias en Alto Río Percy. El fuego pasó a tierras provinciales.
- **Evacuaciones:** cuatro familias de Alto Río Percy, el 5-feb (Infobae).
- **Viviendas afectadas:** no hay cifra publicada; queda **sin confirmar**.
- **Desde cuándo limita el combate:**
  - Hubo combate intenso desde el inicio y durante 27 días.
  - El crecimiento nunca se detiene antes del 5-feb. Ese día, ráfagas de ~50 km/h dan "comportamiento extremo desde las 17 h" y un salto hacia la laguna Trafipán, las laderas del cerro El Sapo y el arroyo Centinela.

## Particularidades

- **Calor:** ola de calor previa confirmada. Bariloche marcó 36,4 °C el lunes 22-ene-2024, récord de enero desde 1961 (Perfil). Fue tres días antes de la ignición.
- **Crecimiento en dos fases:**
  - A los 5 días, ~50 % del área FIRMS final.
  - El 5-feb, salto grande: +3.245 ha FIRMS en un día.
- **Duración:** fue el incendio más largo de los combatidos cerca de población. La máscara coincide con la superficie oficial (6.007 contra 5.971 ha).

## Uso como referencia

- **Horizonte de crecimiento libre:** no hay un día en que el área FIRMS deje de crecer antes del salto del 5-feb.
  - Área FIRMS: 1.295 ha el 26-ene, 2.488 el 28, 4.174 el 30, 4.904 el 3-feb, 8.436 el 5-feb y 8.937 al final.
  - igniteinsights usa el tope de 120 h (~47 % del área FIRMS final).
- **Cicatriz dentro del horizonte:** 2.687 de 6.007 ha (45 %), al horizonte de 120 h.
- **Advertencias:**
  - Más de la mitad de la cicatriz ardió entre el día 6 y el 11, bajo combate y con el salto de viento del 5-feb.
  - Comparar la cicatriz completa con 5 días de simulación castiga al modelo por tiempo no simulado.
  - La semilla del run está 1 km al sur del foco documentado.

## Fuentes

- Ministerio de Seguridad (argentina.gob.ar), sin fecha: [Incendio provocado en Parque Nacional Los Alerces, persona buscada](https://www.argentina.gob.ar/persona-buscada/parque-nacional-los-alerces-provincia-del-chubut)
- Perfil, ene-2024: [Histórica ola de calor en la Patagonia: Bariloche alcanzó el récord mensual](https://www.perfil.com/noticias/actualidad/historica-ola-de-calor-en-la-patagonia-bariloche-estuvo-en-el-top-diez-de-las-temperaturas-mas-altas.phtml)
- France 24, 29-ene-2024: [Denuncian intencionalidad en incendio que sigue arrasando parque en Argentina](https://www.france24.com/es/minuto-a-minuto/20240129-denuncian-intencionalidad-en-incendio-que-sigue-arrasando-parque-en-argentina)
- Infobae, 5-feb-2024: [Ráfagas de viento aceleraron el avance del fuego y familias tuvieron que ser evacuadas](https://www.infobae.com/sociedad/2024/02/05/parque-nacional-los-alerces-rafagas-de-viento-provocaron-el-avance-del-fuego-y-familias-tuvieron-que-ser-evacuadas/)
- La Nación, 18-feb-2024: [Se conoció la cantidad de hectáreas arrasadas por el fuego en el parque](https://www.lanacion.com.ar/sociedad/incendios-controlados-se-conocio-la-cantidad-de-hectareas-arrasadas-por-el-fuego-en-el-parque-nid18022024/)
- Los Andes, 21-feb-2024: [Tras 27 días de lucha, lograron controlar el incendio "en todos los sectores"](https://www.losandes.com.ar/sociedad/tras-27-dias-de-lucha-lograron-controlar-el-incendio-en-todos-los-sectores-del-parque-nacional-los-alerces/)
- Infobae, 23-mar-2024: [Extinguieron el incendio en el Parque Nacional Los Alerces](https://www.infobae.com/sociedad/2024/03/23/extinguieron-el-incendio-en-el-parque-nacional-los-alerces/)
- igniteinsights: `benchmarks/casos/los-alerces-2024/cadena-horizonte.json` (ignición), `benchmarks/diagnosticos/los-alerces-2024.json` y `RESULTADOS-CSS-BAP.md` §3.2 y §7.1.
