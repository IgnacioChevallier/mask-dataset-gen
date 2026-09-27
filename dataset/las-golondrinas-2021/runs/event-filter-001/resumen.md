# Resumen: Incendio Las Golondrinas–Cerro Radal 2021 / event-filter-001

- Estado: `completed`
- Algoritmo: `event-filter-v1-1`
- Run padre: `baseline-001`
- Candidatos del baseline: 14683.42 ha
- Incendio objetivo: 10655.60 ha
- Otro incendio probable: 3983.08 ha
- Cambio no confirmado: 44.73 ha
- Candidatos conservados: 72.57%
- Componentes: 17 (6 objetivo, 7 otro fuego, 4 no confirmados)
- Detecciones térmicas: 102
- Clústeres térmicos: 7

- Superficie oficial de referencia: 12901.00 ha
- Diferencia exploratoria: -2245.40 ha

## Componentes

| ID | Clase | Área | Dist. hotspot objetivo | Motivo |
| --- | --- | ---: | ---: | --- |
| `component-007` | `incendio_objetivo` | 10479.83 ha | 12 m | próximo a la semilla del evento |
| `component-001` | `otro_incendio_probable` | 3255.10 ha | 6565 m | próximo a un clúster térmico distinto |
| `component-005` | `otro_incendio_probable` | 556.82 ha | 15786 m | próximo a un clúster térmico distinto |
| `component-016` | `otro_incendio_probable` | 75.90 ha | 17984 m | próximo a un clúster térmico distinto |
| `component-004` | `otro_incendio_probable` | 49.58 ha | 14573 m | próximo a un clúster térmico distinto |
| `component-015` | `incendio_objetivo` | 35.04 ha | 7460 m | fragmento próximo a un componente objetivo |
| `component-013` | `incendio_objetivo` | 20.00 ha | 2966 m | próximo a la semilla del evento |
| `component-011` | `incendio_objetivo` | 15.53 ha | 8445 m | fragmento próximo a un componente objetivo |
| `component-017` | `cambio_no_confirmado` | 14.50 ha | 9782 m | sin continuidad ni evidencia térmica suficiente |
| `component-006` | `otro_incendio_probable` | 12.96 ha | 15077 m | próximo a un clúster térmico distinto |
| `component-010` | `cambio_no_confirmado` | 11.23 ha | 16836 m | sin continuidad ni evidencia térmica suficiente |
| `component-008` | `cambio_no_confirmado` | 11.03 ha | 18000 m | sin continuidad ni evidencia térmica suficiente |
| `component-014` | `incendio_objetivo` | 10.58 ha | 8430 m | fragmento próximo a un componente objetivo |
| `component-012` | `cambio_no_confirmado` | 7.97 ha | 2541 m | sin continuidad ni evidencia térmica suficiente |
| `component-009` | `incendio_objetivo` | 7.92 ha | 2925 m | fragmento próximo a un componente objetivo |
| `component-003` | `otro_incendio_probable` | 3.03 ha | 15014 m | próximo a un clúster térmico distinto |
| `component-002` | `otro_incendio_probable` | 0.06 ha | 10889 m | próximo a un clúster térmico distinto |

## Interpretación

El filtro atribuye objetos mediante reglas explícitas de proximidad a la semilla, detecciones térmicas y continuidad espacial. La ausencia de un hotspot no demuestra ausencia de fuego; las clases rechazadas se conservan para auditoría.
