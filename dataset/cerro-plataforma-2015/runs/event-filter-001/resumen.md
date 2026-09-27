# Resumen: Incendio Cerro Plataforma, El Turbio 2015 / event-filter-001

- Estado: `completed`
- Algoritmo: `event-filter-v1-1`
- Run padre: `baseline-001`
- Candidatos del baseline: 6615.93 ha
- Incendio objetivo: 6291.86 ha
- Otro incendio probable: 237.09 ha
- Cambio no confirmado: 86.98 ha
- Candidatos conservados: 95.10%
- Componentes: 26 (18 objetivo, 4 otro fuego, 4 no confirmados)
- Detecciones térmicas: 349
- Clústeres térmicos: 3

- Superficie oficial de referencia: 7371.30 ha
- Diferencia exploratoria: -1079.44 ha

## Componentes

| ID | Clase | Área | Dist. hotspot objetivo | Motivo |
| --- | --- | ---: | ---: | --- |
| `component-004` | `incendio_objetivo` | 4583.06 ha | 6 m | próximo a la semilla del evento |
| `component-007` | `incendio_objetivo` | 1353.08 ha | 6 m | próximo a la semilla del evento |
| `component-025` | `otro_incendio_probable` | 131.01 ha | 2804 m | próximo a un clúster térmico distinto |
| `component-024` | `otro_incendio_probable` | 78.88 ha | 4958 m | próximo a un clúster térmico distinto |
| `component-016` | `incendio_objetivo` | 73.61 ha | 12 m | próximo al clúster térmico objetivo |
| `component-005` | `cambio_no_confirmado` | 60.67 ha | 4676 m | sin continuidad ni evidencia térmica suficiente |
| `component-011` | `incendio_objetivo` | 54.24 ha | 1467 m | próximo al clúster térmico objetivo |
| `component-015` | `incendio_objetivo` | 36.24 ha | 854 m | próximo al clúster térmico objetivo |
| `component-023` | `otro_incendio_probable` | 20.77 ha | 4451 m | próximo a un clúster térmico distinto |
| `component-018` | `incendio_objetivo` | 18.12 ha | 589 m | próximo al clúster térmico objetivo |
| `component-017` | `incendio_objetivo` | 16.86 ha | 6 m | próximo al clúster térmico objetivo |
| `component-020` | `incendio_objetivo` | 16.59 ha | 216 m | próximo al clúster térmico objetivo |
| `component-001` | `cambio_no_confirmado` | 15.62 ha | 5930 m | sin continuidad ni evidencia térmica suficiente |
| `component-009` | `incendio_objetivo` | 15.15 ha | 265 m | próximo al clúster térmico objetivo |
| `component-012` | `incendio_objetivo` | 14.87 ha | 15 m | próximo al clúster térmico objetivo |
| `component-010` | `incendio_objetivo` | 12.68 ha | 1702 m | fragmento próximo a un componente objetivo |
| `component-019` | `incendio_objetivo` | 12.68 ha | 891 m | próximo al clúster térmico objetivo |
| `component-003` | `incendio_objetivo` | 11.10 ha | 85 m | próximo al clúster térmico objetivo |
| `component-022` | `cambio_no_confirmado` | 11.08 ha | 2595 m | sin continuidad ni evidencia térmica suficiente |
| `component-006` | `incendio_objetivo` | 10.77 ha | 15 m | próximo al clúster térmico objetivo |
| `component-021` | `incendio_objetivo` | 10.29 ha | 1073 m | próximo al clúster térmico objetivo |
| `component-008` | `incendio_objetivo` | 10.10 ha | 6 m | próximo al clúster térmico objetivo |
| `component-014` | `incendio_objetivo` | 9.96 ha | 222 m | próximo al clúster térmico objetivo |
| `component-013` | `incendio_objetivo` | 8.30 ha | 113 m | próximo al clúster térmico objetivo |
| `component-026` | `otro_incendio_probable` | 7.30 ha | 5723 m | próximo a un clúster térmico distinto |
| `component-002` | `cambio_no_confirmado` | 0.66 ha | 6397 m | sin continuidad ni evidencia térmica suficiente |

## Interpretación

El filtro atribuye objetos mediante reglas explícitas de proximidad a la semilla, detecciones térmicas y continuidad espacial. La ausencia de un hotspot no demuestra ausencia de fuego; las clases rechazadas se conservan para auditoría.
