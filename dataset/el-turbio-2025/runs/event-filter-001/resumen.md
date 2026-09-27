# Resumen: Incendio El Turbio 2025 / event-filter-001

- Estado: `completed`
- Algoritmo: `event-filter-v1-1`
- Run padre: `baseline-001`
- Candidatos del baseline: 1968.74 ha
- Incendio objetivo: 1968.74 ha
- Otro incendio probable: 0.00 ha
- Cambio no confirmado: 0.00 ha
- Candidatos conservados: 100.00%
- Componentes: 11 (11 objetivo, 0 otro fuego, 0 no confirmados)
- Detecciones térmicas: 1947
- Clústeres térmicos: 1

- Superficie oficial de referencia: 3000.00 ha
- Diferencia exploratoria: -1031.26 ha

## Componentes

| ID | Clase | Área | Dist. hotspot objetivo | Motivo |
| --- | --- | ---: | ---: | --- |
| `component-002` | `incendio_objetivo` | 1430.81 ha | 3 m | próximo a la semilla del evento |
| `component-001` | `incendio_objetivo` | 302.33 ha | 3 m | próximo a la semilla del evento |
| `component-009` | `incendio_objetivo` | 61.52 ha | 6 m | próximo al clúster térmico objetivo |
| `component-007` | `incendio_objetivo` | 57.01 ha | 3 m | próximo al clúster térmico objetivo |
| `component-011` | `incendio_objetivo` | 40.00 ha | 6 m | próximo al clúster térmico objetivo |
| `component-005` | `incendio_objetivo` | 14.40 ha | 8 m | próximo al clúster térmico objetivo |
| `component-008` | `incendio_objetivo` | 11.71 ha | 9 m | próximo al clúster térmico objetivo |
| `component-003` | `incendio_objetivo` | 11.34 ha | 8 m | próximo a la semilla del evento |
| `component-006` | `incendio_objetivo` | 9.41 ha | 3 m | próximo al clúster térmico objetivo |
| `component-010` | `incendio_objetivo` | 8.47 ha | 3 m | próximo al clúster térmico objetivo |
| `component-004` | `incendio_objetivo` | 7.59 ha | 3 m | próximo al clúster térmico objetivo |

## Interpretación

El filtro atribuye objetos mediante reglas explícitas de proximidad a la semilla, detecciones térmicas y continuidad espacial. La ausencia de un hotspot no demuestra ausencia de fuego; las clases rechazadas se conservan para auditoría.
