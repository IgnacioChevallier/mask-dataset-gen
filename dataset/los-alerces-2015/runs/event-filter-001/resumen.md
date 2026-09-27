# Resumen: Incendio Los Alerces, cordón Situación 2015 / event-filter-001

- Estado: `completed`
- Algoritmo: `event-filter-v1-1`
- Run padre: `baseline-001`
- Candidatos del baseline: 1202.33 ha
- Incendio objetivo: 1202.33 ha
- Otro incendio probable: 0.00 ha
- Cambio no confirmado: 0.00 ha
- Candidatos conservados: 100.00%
- Componentes: 2 (2 objetivo, 0 otro fuego, 0 no confirmados)
- Detecciones térmicas: 30
- Clústeres térmicos: 1

- Superficie oficial de referencia: 1500.00 ha
- Diferencia exploratoria: -297.67 ha

## Componentes

| ID | Clase | Área | Dist. hotspot objetivo | Motivo |
| --- | --- | ---: | ---: | --- |
| `component-001` | `incendio_objetivo` | 1176.15 ha | 6 m | próximo a la semilla del evento |
| `component-002` | `incendio_objetivo` | 9.80 ha | 1163 m | próximo a la semilla del evento |

## Interpretación

El filtro atribuye objetos mediante reglas explícitas de proximidad a la semilla, detecciones térmicas y continuidad espacial. La ausencia de un hotspot no demuestra ausencia de fuego; las clases rechazadas se conservan para auditoría.
