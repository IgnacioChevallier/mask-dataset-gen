# Resumen: Incendio Población Rosales, Los Alerces 2023 / event-filter-002

- Estado: `completed`
- Algoritmo: `event-filter-v1-1`
- Run padre: `baseline-001`
- Candidatos del baseline: 1358.74 ha
- Incendio objetivo: 1067.01 ha
- Otro incendio probable: 0.00 ha
- Cambio no confirmado: 291.74 ha
- Candidatos conservados: 78.53%
- Componentes: 9 (1 objetivo, 0 otro fuego, 8 no confirmados)
- Detecciones térmicas: 37
- Clústeres térmicos: 1

- Superficie oficial de referencia: 1160.00 ha
- Diferencia exploratoria: -92.99 ha

## Componentes

| ID | Clase | Área | Dist. hotspot objetivo | Motivo |
| --- | --- | ---: | ---: | --- |
| `component-003` | `incendio_objetivo` | 1053.70 ha | 12 m | próximo a la semilla del evento |
| `component-004` | `cambio_no_confirmado` | 111.39 ha | 4354 m | sin continuidad ni evidencia térmica suficiente |
| `component-007` | `cambio_no_confirmado` | 101.16 ha | 7390 m | sin continuidad ni evidencia térmica suficiente |
| `component-005` | `cambio_no_confirmado` | 31.65 ha | 6253 m | sin continuidad ni evidencia térmica suficiente |
| `component-002` | `cambio_no_confirmado` | 11.18 ha | 5414 m | sin continuidad ni evidencia térmica suficiente |
| `component-001` | `cambio_no_confirmado` | 10.89 ha | 9443 m | sin continuidad ni evidencia térmica suficiente |
| `component-006` | `cambio_no_confirmado` | 8.99 ha | 7696 m | sin continuidad ni evidencia térmica suficiente |
| `component-009` | `cambio_no_confirmado` | 7.68 ha | 7782 m | sin continuidad ni evidencia térmica suficiente |
| `component-008` | `cambio_no_confirmado` | 7.42 ha | 7622 m | sin continuidad ni evidencia térmica suficiente |

## Interpretación

El filtro atribuye objetos mediante reglas explícitas de proximidad a la semilla, detecciones térmicas y continuidad espacial. La ausencia de un hotspot no demuestra ausencia de fuego; las clases rechazadas se conservan para auditoría.
