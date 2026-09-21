# Resumen: Puerto Patriada, El Hoyo y Epuyén 2026 / legacy-v1

- Estado: `completed`
- Origen: dataset existente importado sin modificar los rasters ni el CSV
- Tiles: 196 tripletas PRE/POST/máscara
- PRE: `2023-11-01` a `2023-12-31`
- POST: `2026-02-01` a `2026-03-08`
- Estrategia de nombres: `tile_NNN`

Este resultado representa cambio acumulado entre 2023 y 2026. No aísla de
forma estricta el incendio iniciado en enero de 2026 y no contiene una capa de
observación válida. Los IDs exactos de las escenas Sentinel-2 usadas por la
ejecución original tampoco quedaron registrados.

Se conserva como resultado histórico e interfaz de compatibilidad. El run
`baseline-002` está definido para una comparación temporal mejor aislada, pero
su ejecución queda diferida.

Las siete visualizaciones guardadas y los catorce diagnósticos de remasking
existentes fueron clasificados bajo `visualizaciones/tiles/` y
`visualizaciones/diagnosticos/`, respectivamente. Las rutas históricas
`saved/` y `remask_comparisons/` se conservan como enlaces simbólicos.
