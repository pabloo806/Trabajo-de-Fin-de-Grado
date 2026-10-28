# ADR-006: Exportación e Integración con Rekordbox

## Estado

Propuesto

## Contexto

SetlistGen debe integrarse con el flujo de trabajo real del DJ mediante la exportación de listas compatibles con Rekordbox.

## Problema

Determinar el mecanismo de exportación e interoperabilidad.

## Alternativas

- XML de Rekordbox.
- M3U8.
- XML y M3U8 simultáneamente.
- Otros formatos compatibles.

## Criterios de evaluación

- Compatibilidad con Rekordbox.
- Robustez de la importación.
- Simplicidad de implementación.
- Facilidad de uso para el DJ.
- Compatibilidad entre versiones de Rekordbox.
- Posibilidad de automatización.
- Portabilidad.

## Evaluación de alternativas

| Criterio | Peso |
|-----------|------:|
| Compatibilidad con Rekordbox | 5 |
| Robustez | 5 |
| Facilidad de implementación | 4 |
| Facilidad de uso para el DJ | 5 |
| Compatibilidad futura | 3 |
| Portabilidad | 3 |

## Matriz de decisión

| Alternativa | Compatibilidad | Robustez | Implementación | UX | Evolución | Portabilidad | Total |
|------------|---------------:|----------:|---------------:|---:|----------:|-------------:|------:|
| XML Rekordbox | | | | | | | |
| M3U8 | | | | | | | |
| XML + M3U8 | | | | | | | |

## Decisión final

Pendiente.

## Justificación

La decisión dependerá de las pruebas de integración realizadas con Rekordbox.

## Consecuencias

Influirá en la experiencia de usuario y en la compatibilidad final del sistema.
