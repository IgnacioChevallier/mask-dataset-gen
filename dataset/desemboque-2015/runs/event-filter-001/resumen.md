# Resumen: Incendio Desemboque, Lago Puelo–Epuyén 2015 / event-filter-001

- Estado: `completed`
- Algoritmo: `event-filter-v1-1`
- Run padre: `baseline-002`
- Candidatos del baseline: 558.04 ha
- Incendio objetivo: 558.04 ha
- Otro incendio probable: 0.00 ha
- Cambio no confirmado: 0.00 ha
- Candidatos conservados: 100.00%
- Componentes: 2 (2 objetivo, 0 otro fuego, 0 no confirmados)
- Detecciones térmicas: 36
- Clústeres térmicos: 1

- Superficie oficial de referencia: 2306.80 ha
- Diferencia exploratoria: -1748.76 ha

## Componentes

| ID | Clase | Área | Dist. hotspot objetivo | Motivo |
| --- | --- | ---: | ---: | --- |
| `component-002` | `incendio_objetivo` | 529.38 ha | 6 m | próximo a la semilla del evento |
| `component-001` | `incendio_objetivo` | 28.65 ha | 228 m | próximo al clúster térmico objetivo |

## Interpretación

El filtro atribuye objetos mediante reglas explícitas de proximidad a la semilla, detecciones térmicas y continuidad espacial. La ausencia de un hotspot no demuestra ausencia de fuego; las clases rechazadas se conservan para auditoría.
