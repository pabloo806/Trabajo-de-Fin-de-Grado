# Requisitos de SetlistGen

**Versión:** 1.2.1 · **Estado:** listo para revisión con el tutor

Este directorio contiene la especificación funcional de SetlistGen: qué debe hacer el sistema, quién lo usa, cómo se comprueba y cómo se relaciona cada requisito con las acciones del usuario.

## Alcance en una vista

| Elemento | Cantidad |
|---|---:|
| Actor | 1 (el **DJ**) |
| Requisitos funcionales (RF) | 22 |
| Requisitos no funcionales (RNF) | 12 |
| Casos de uso (CU) | 8 (2 críticos) |

SetlistGen es una aplicación local que analiza las bibliotecas musicales del DJ, genera setlists según parámetros de duración, BPM y compatibilidad Camelot, permite editarlos y los guarda en SQLite. La exportación a Rekordbox es una ampliación opcional.

## Documentos

| Documento | Contenido |
|---|---|
| [`requirements.md`](requirements.md) | Alcance, actor, 22 RF y 12 RNF con prioridad MoSCoW, criterios de aceptación y decisiones funcionales |
| [`use-cases.md`](use-cases.md) | Diagrama de casos de uso, especificación de los 8 CU y diagramas de secuencia de los 2 casos críticos |
| [`traceability-matrix.md`](traceability-matrix.md) | Relación entre casos de uso, requisitos, componentes y pruebas previstas, con la cobertura bidireccional |

Los diagramas UML están en [`../diagrams/`](../diagrams/).

## Cómo leerlos

1. **`requirements.md`:** para saber qué hace el sistema y con qué umbrales.
2. **`use-cases.md`:** para ver cómo lo usa el DJ, paso a paso.
3. **`traceability-matrix.md`:** para comprobar de un vistazo que cada requisito está cubierto y cómo se verifica.

## Estado y siguientes pasos

- Los umbrales marcados **(P)** son provisionales y se ratifican con datos reales.
- La validación de exactitud (RNF-02 y RNF-03) se realiza fuera de la aplicación, con un script sobre un CSV anotado a mano.
- Tras la revisión del tutor, estos documentos son la base del modelado de datos y de la implementación.