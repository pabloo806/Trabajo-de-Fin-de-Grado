# Documentación de SetlistGen

Esta carpeta reúne la documentación del Trabajo de Fin de Grado: requisitos, arquitectura, modelo de datos, diagramas, pruebas, gestión y memoria.

## Estructura

```text
docs/
├── architecture/        Arquitectura, decisiones (ADR) y modelo de datos
├── diagrams/            Todos los diagramas: .drawio (fuente) y .svg (exportado)
├── memory/              Memoria del TFG (LaTeX)
├── project-management/  Seguimiento y reuniones con los tutores
├── requirements/        Requisitos, casos de uso y matriz de trazabilidad
└── testing/             Estrategia de pruebas y validación
```

## Estado de la documentación

| Documento | Versión | Estado |
|---|---|---|
| [`requirements/requirements.md`](requirements/requirements.md) | 1.2.2 | Listo para revisión con los tutores |
| [`requirements/use-cases.md`](requirements/use-cases.md) | 1.2.2 | Listo para revisión con los tutores |
| [`requirements/traceability-matrix.md`](requirements/tracability-matrix.md) | Alineada con requisitos 1.2.2 | Listo para revisión con los tutores |
| [`architecture/README.md`](architecture/README.md) | — | Cerrado: componentes, capas y resumen de decisiones |
| [`architecture/adrs/`](architecture/adrs/) | ADR-001 a ADR-010 | Cerrados. ADR-006 (exportación) reescrito como ampliación opcional |
| [`architecture/data-model.md`](architecture/data-model.md) | 1.0.1 | Cerrado: ER, modelo relacional, diccionario, DDL, consultas e índices |
| [`schema.sql`](../src/setlistgen/infrastructure/persistence/schema.sql) | 1.0 | Verificado |
| [`tests/persistence/`](../tests/persistence/) | 178 tests | Todos en verde (Windows, Python 3.14 y SQLite) |
| [`memory/`](memory/) | — | Capítulos 1 a 4 redactados. Pendiente actualizar el alcance y redactar Análisis, Arquitectura y Diseño de datos |
| [`testing/`](testing/) | — | Por completar con la validación de exactitud |
| [`project-management/`](project-management/) | — | Seguimiento con los tutores |

## Contenido de cada carpeta

| Carpeta | Propósito | Contenido |
|---|---|---|
| [`requirements/`](requirements/README.md) | Qué debe hacer el sistema | 22 requisitos funcionales, 12 no funcionales, 8 casos de uso y la matriz de trazabilidad |
| [`architecture/`](architecture/README.md) | Cómo está construido | Diagrama de componentes, capas, ADR y modelo de datos |
| [`diagrams/`](diagrams/) | Fuente única de los diagramas | Componentes, casos de uso, secuencia, entidad-relación y modelo relacional |
| [`testing/`](testing/) | Cómo se comprueba | Estrategia de pruebas y validación frente a Rekordbox |
| [`project-management/`](project-management/) | Seguimiento | Documentos de las reuniones y decisiones con tutor y cotutor |
| [`memory/`](memory/) | Memoria académica | Capítulos y apéndices en LaTeX sobre la plantilla oficial |

## Diagramas

### Convención

Todos los diagramas viven en `docs/diagrams/` en formato nativo de **Draw.io**, con dos ficheros por diagrama:

| Fichero | Función |
|---|---|
| `nombre.drawio` | Fuente editable (se abre y edita directamente en VS Code con la extensión de Draw.io) |
| `nombre.svg` | Exportación vectorial, con copia editable embebida, que se incluye en los documentos |

No hay ficheros `.puml` paralelos: una sola fuente evita que los diagramas se desincronicen.

### Diagramas del proyecto

| Diagrama | Ficheros | Aparece en |
|---|---|---|
| Componentes (UML) | `componentes` | [`architecture/README.md`](architecture/README.md) |
| Casos de uso (UML) | `casos-de-uso` | [`requirements/use-cases.md`](requirements/use-cases.md) |
| Secuencia: Seleccionar biblioteca local | `secuencia-seleccionar-biblioteca` | [`requirements/use-cases.md`](requirements/use-cases.md) |
| Secuencia: Establecer parámetros para generar setlist | `secuencia-generar-setlist` | [`requirements/use-cases.md`](requirements/use-cases.md) |
| Entidad-Relación (notación de Chen) | `modelo-er` | [`architecture/data-model.md`](architecture/data-model.md) |
| Modelo relacional | `modelo-relacional` | [`architecture/data-model.md`](architecture/data-model.md) |

Los pequeños diagramas Mermaid incrustados en `requirements.md` y `traceability-matrix.md` son vistas de apoyo sin fichero propio.

### Cómo añadir o modificar un diagrama

1. Edita o crea `docs/diagrams/nombre.drawio` en VS Code.
2. Exporta a SVG marcando **«Incluir una copia de mi diagrama»** y guarda `nombre.svg` junto al `.drawio`.
3. Referencia el SVG desde el documento con una ruta relativa: `![Descripción](../diagrams/nombre.svg)`.
4. Haz commit de ambos ficheros.

Para la memoria en LaTeX, exporta el diagrama desde Draw.io en PDF recortado o SVG a la máxima calidad.

## Flujo documental

```text
Requisitos → Casos de uso → Trazabilidad → Arquitectura → Modelo de datos → Pruebas → Implementación → Memoria
```

Cada documento alimenta el siguiente y el capítulo correspondiente de la memoria, que se redacta de forma incremental para no acumular trabajo al final.

**Si algo cambia**, se actualiza en este orden: requisitos y casos de uso → matriz de trazabilidad → modelo de datos y `schema.sql` → tests → memoria. Cada documento mantiene su control de cambios.