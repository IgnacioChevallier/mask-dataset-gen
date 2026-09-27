# Resumen: Incendio Currumahuida–Lago Puelo 2015 / event-filter-001

- Estado: `completed`
- Algoritmo: `event-filter-v1-1`
- Run padre: `baseline-001`
- Candidatos del baseline: 4244.93 ha
- Incendio objetivo: 4236.47 ha
- Otro incendio probable: 0.00 ha
- Cambio no confirmado: 8.46 ha
- Candidatos conservados: 99.80%
- Componentes: 7 (6 objetivo, 0 otro fuego, 1 no confirmados)
- Detecciones térmicas: 85
- Clústeres térmicos: 2

- Superficie oficial de referencia: 3150.80 ha
- Diferencia exploratoria: +1085.67 ha

## Componentes

| ID | Clase | Área | Dist. hotspot objetivo | Motivo |
| --- | --- | ---: | ---: | --- |
| `component-005` | `incendio_objetivo` | 2029.96 ha | 6 m | próximo a la semilla del evento |
| `component-001` | `incendio_objetivo` | 1450.25 ha | 6 m | próximo al clúster térmico objetivo |
| `component-006` | `incendio_objetivo` | 693.76 ha | 6 m | próximo a la semilla del evento |
| `component-003` | `incendio_objetivo` | 25.98 ha | 910 m | próximo al clúster térmico objetivo |
| `component-004` | `incendio_objetivo` | 17.25 ha | 1056 m | próximo al clúster térmico objetivo |
| `component-007` | `incendio_objetivo` | 10.57 ha | 1156 m | próximo al clúster térmico objetivo |
| `component-002` | `cambio_no_confirmado` | 8.26 ha | 4566 m | sin continuidad ni evidencia térmica suficiente |

## Interpretación

El filtro atribuye objetos mediante reglas explícitas de proximidad a la semilla, detecciones térmicas y continuidad espacial. La ausencia de un hotspot no demuestra ausencia de fuego; las clases rechazadas se conservan para auditoría.
