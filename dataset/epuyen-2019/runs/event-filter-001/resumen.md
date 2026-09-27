# Resumen: Incendio de Epuyén 2019 / event-filter-001

- Estado: `completed`
- Algoritmo: `event-filter-v1-1`
- Run padre: `baseline-001`
- Candidatos del baseline: 1598.39 ha
- Incendio objetivo: 1544.64 ha
- Otro incendio probable: 0.00 ha
- Cambio no confirmado: 53.75 ha
- Candidatos conservados: 96.64%
- Componentes: 6 (3 objetivo, 0 otro fuego, 3 no confirmados)
- Detecciones térmicas: 50
- Clústeres térmicos: 1

- Superficie oficial de referencia: 1553.00 ha
- Diferencia exploratoria: -8.36 ha

## Componentes

| ID | Clase | Área | Dist. hotspot objetivo | Motivo |
| --- | --- | ---: | ---: | --- |
| `component-002` | `incendio_objetivo` | 1518.61 ha | 12 m | próximo a la semilla del evento |
| `component-004` | `cambio_no_confirmado` | 33.32 ha | 3306 m | sin continuidad ni evidencia térmica suficiente |
| `component-006` | `cambio_no_confirmado` | 12.95 ha | 4702 m | sin continuidad ni evidencia térmica suficiente |
| `component-001` | `incendio_objetivo` | 9.10 ha | 1603 m | fragmento próximo a un componente objetivo |
| `component-003` | `incendio_objetivo` | 7.86 ha | 1017 m | próximo al clúster térmico objetivo |
| `component-005` | `cambio_no_confirmado` | 7.26 ha | 2420 m | sin continuidad ni evidencia térmica suficiente |

## Interpretación

El filtro atribuye objetos mediante reglas explícitas de proximidad a la semilla, detecciones térmicas y continuidad espacial. La ausencia de un hotspot no demuestra ausencia de fuego; las clases rechazadas se conservan para auditoría.
