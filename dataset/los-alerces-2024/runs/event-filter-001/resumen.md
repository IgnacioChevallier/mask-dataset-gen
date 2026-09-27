# Resumen: Incendio Los Alerces, Bahía Rosales 2024 / event-filter-001

- Estado: `completed`
- Algoritmo: `event-filter-v1-1`
- Run padre: `baseline-001`
- Candidatos del baseline: 6095.41 ha
- Incendio objetivo: 6007.37 ha
- Otro incendio probable: 0.00 ha
- Cambio no confirmado: 88.05 ha
- Candidatos conservados: 98.56%
- Componentes: 11 (4 objetivo, 0 otro fuego, 7 no confirmados)
- Detecciones térmicas: 2551
- Clústeres térmicos: 1

- Superficie oficial de referencia: 5971.00 ha
- Diferencia exploratoria: +36.37 ha

## Componentes

| ID | Clase | Área | Dist. hotspot objetivo | Motivo |
| --- | --- | ---: | ---: | --- |
| `component-001` | `incendio_objetivo` | 5895.93 ha | 3 m | próximo a la semilla del evento |
| `component-004` | `incendio_objetivo` | 65.57 ha | 8 m | próximo al clúster térmico objetivo |
| `component-006` | `cambio_no_confirmado` | 65.24 ha | 6452 m | sin continuidad ni evidencia térmica suficiente |
| `component-007` | `cambio_no_confirmado` | 11.21 ha | 7442 m | sin continuidad ni evidencia térmica suficiente |
| `component-003` | `cambio_no_confirmado` | 8.99 ha | 2524 m | sin continuidad ni evidencia térmica suficiente |
| `component-005` | `incendio_objetivo` | 7.96 ha | 9 m | próximo al clúster térmico objetivo |
| `component-002` | `incendio_objetivo` | 6.80 ha | 36 m | próximo al clúster térmico objetivo |
| `component-009` | `cambio_no_confirmado` | 1.40 ha | 6946 m | sin continuidad ni evidencia térmica suficiente |
| `component-008` | `cambio_no_confirmado` | 0.67 ha | 7300 m | sin continuidad ni evidencia térmica suficiente |
| `component-010` | `cambio_no_confirmado` | 0.47 ha | 6797 m | sin continuidad ni evidencia térmica suficiente |
| `component-011` | `cambio_no_confirmado` | 0.06 ha | 7205 m | sin continuidad ni evidencia térmica suficiente |

## Interpretación

El filtro atribuye objetos mediante reglas explícitas de proximidad a la semilla, detecciones térmicas y continuidad espacial. La ausencia de un hotspot no demuestra ausencia de fuego; las clases rechazadas se conservan para auditoría.
