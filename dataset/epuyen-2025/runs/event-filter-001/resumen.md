# Resumen: Incendio de Epuyén 2025 / event-filter-001

- Estado: `completed`
- Algoritmo: `event-filter-v1`
- Run padre: `baseline-001`
- Candidatos del baseline: 3246.31 ha
- Incendio objetivo: 2995.03 ha
- Otro incendio probable: 38.71 ha
- Cambio no confirmado: 212.57 ha
- Candidatos conservados: 92.26%
- Componentes: 15 (2 objetivo, 1 otro fuego, 12 no confirmados)
- Detecciones térmicas: 745
- Clústeres térmicos: 2

- Superficie oficial de referencia: 3530.00 ha
- Diferencia exploratoria: -534.97 ha

## Componentes

| ID | Clase | Área | Dist. hotspot objetivo | Motivo |
| --- | --- | ---: | ---: | --- |
| `component-005` | `incendio_objetivo` | 2966.32 ha | 1 m | próximo a la semilla del evento |
| `component-013` | `cambio_no_confirmado` | 51.94 ha | 15243 m | sin continuidad ni evidencia térmica suficiente |
| `component-004` | `otro_incendio_probable` | 38.24 ha | 7763 m | próximo a un clúster térmico distinto |
| `component-006` | `cambio_no_confirmado` | 37.55 ha | 7561 m | sin continuidad ni evidencia térmica suficiente |
| `component-012` | `cambio_no_confirmado` | 36.18 ha | 15393 m | sin continuidad ni evidencia térmica suficiente |
| `component-015` | `cambio_no_confirmado` | 13.35 ha | 12369 m | sin continuidad ni evidencia térmica suficiente |
| `component-014` | `cambio_no_confirmado` | 12.26 ha | 15303 m | sin continuidad ni evidencia térmica suficiente |
| `component-010` | `cambio_no_confirmado` | 11.65 ha | 16145 m | sin continuidad ni evidencia térmica suficiente |
| `component-007` | `cambio_no_confirmado` | 9.04 ha | 8294 m | sin continuidad ni evidencia térmica suficiente |
| `component-001` | `cambio_no_confirmado` | 8.65 ha | 14818 m | sin continuidad ni evidencia térmica suficiente |
| `component-011` | `cambio_no_confirmado` | 8.46 ha | 6974 m | sin continuidad ni evidencia térmica suficiente |
| `component-009` | `incendio_objetivo` | 8.36 ha | 68 m | próximo a la semilla del evento |
| `component-008` | `cambio_no_confirmado` | 7.91 ha | 7391 m | sin continuidad ni evidencia térmica suficiente |
| `component-003` | `cambio_no_confirmado` | 7.49 ha | 8445 m | sin continuidad ni evidencia térmica suficiente |
| `component-002` | `cambio_no_confirmado` | 6.66 ha | 12687 m | sin continuidad ni evidencia térmica suficiente |

## Interpretación

El filtro atribuye objetos mediante reglas explícitas de proximidad a la semilla, detecciones térmicas y continuidad espacial. La ausencia de un hotspot no demuestra ausencia de fuego; las clases rechazadas se conservan para auditoría.
