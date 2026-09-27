# Resumen: Incendio Los Alerces, Futalaufquen 2016 / event-filter-001

- Estado: `completed`
- Algoritmo: `event-filter-v1-1`
- Run padre: `baseline-001`
- Candidatos del baseline: 1957.36 ha
- Incendio objetivo: 1849.69 ha
- Otro incendio probable: 13.80 ha
- Cambio no confirmado: 93.88 ha
- Candidatos conservados: 94.50%
- Componentes: 11 (3 objetivo, 1 otro fuego, 7 no confirmados)
- Detecciones térmicas: 27
- Clústeres térmicos: 2

- Superficie oficial de referencia: 1700.00 ha
- Diferencia exploratoria: +149.69 ha

## Componentes

| ID | Clase | Área | Dist. hotspot objetivo | Motivo |
| --- | --- | ---: | ---: | --- |
| `component-003` | `incendio_objetivo` | 1800.12 ha | 6 m | próximo a la semilla del evento |
| `component-011` | `cambio_no_confirmado` | 29.55 ha | 9266 m | sin continuidad ni evidencia térmica suficiente |
| `component-005` | `cambio_no_confirmado` | 28.78 ha | 5012 m | sin continuidad ni evidencia térmica suficiente |
| `component-004` | `incendio_objetivo` | 16.37 ha | 1165 m | próximo a la semilla del evento |
| `component-006` | `otro_incendio_probable` | 15.18 ha | 4317 m | próximo a un clúster térmico distinto |
| `component-008` | `incendio_objetivo` | 13.40 ha | 4361 m | fragmento próximo a un componente objetivo |
| `component-007` | `cambio_no_confirmado` | 13.01 ha | 6030 m | sin continuidad ni evidencia térmica suficiente |
| `component-009` | `cambio_no_confirmado` | 11.63 ha | 6594 m | sin continuidad ni evidencia térmica suficiente |
| `component-010` | `cambio_no_confirmado` | 9.26 ha | 9059 m | sin continuidad ni evidencia térmica suficiente |
| `component-001` | `cambio_no_confirmado` | 3.82 ha | 5218 m | sin continuidad ni evidencia térmica suficiente |
| `component-002` | `cambio_no_confirmado` | 0.07 ha | 5231 m | sin continuidad ni evidencia térmica suficiente |

## Interpretación

El filtro atribuye objetos mediante reglas explícitas de proximidad a la semilla, detecciones térmicas y continuidad espacial. La ausencia de un hotspot no demuestra ausencia de fuego; las clases rechazadas se conservan para auditoría.
