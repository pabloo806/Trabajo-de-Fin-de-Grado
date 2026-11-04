# Revisión Técnica de la Documentación

## Contexto

Este documento recoge el resultado de la auditoría técnica realizada sobre la documentación del proyecto SetlistGen.

La auditoría se realizó tras la finalización de las fases de:

- Ingeniería de requisitos.
- Casos de uso.
- Matriz de trazabilidad.
- Glosario.
- Arquitectura.
- ADR-001 a ADR-006.

Posteriormente se inició una fase de consolidación documental que dio lugar a:

- requirements.md v4.0
- use-cases.md v1.1
- traceability-matrix.md v3.0
- glosario.md v2.1
- ADR-001 a ADR-010
- README principal actualizado
- README de arquitectura actualizado

Fecha de actualización:

2026-11-04

---

# Hallazgos Resueltos

## H-01

Estado: Resuelto

Resultado:

requirements.md alineado con ADR-001 a ADR-006.

---

## H-03

Estado: Resuelto

Resultado:

ADR-005 reformulado.

Se introducen restricciones explícitas R1-R7.

---

## H-04

Estado: Resuelto

Resultado:

RF-13b incorporado.

El salto máximo de BPM pasa a ser un parámetro configurable.

---

## H-07

Estado: Resuelto

Resultado:

RF-29 promovido a Must.

CU-11 pasa a considerarse un caso de uso crítico.

---

## H-08

Estado: Resuelto

Resultado:

Se incorpora soporte explícito para análisis multi-motor.

---

## H-17

Estado: Resuelto

Resultado:

Se define RF-29b para importación de datos de referencia desde Rekordbox.

---

## H-19

Estado: Resuelto

Resultado:

RF-09c incorpora:

- pistas movidas,
- pistas ausentes,
- pistas duplicadas.

---

## H-26

Estado: Resuelto

Resultado:

ADR-002 actualizado:

- PostgreSQL eliminado.
- Vocabulario de puertos unificado.
- Puertos reubicados en Aplicación.

---

## H-35

Estado: Parcialmente resuelto

Resultado:

Se han identificado y documentado las entidades candidatas del dominio.

Pendiente:

- validación con tutor,
- modelado definitivo.

---

# Hallazgos Convertidos en ADR

## H-11

Convertido en:

ADR-008

---

## H-12

Convertido en:

ADR-007
ADR-009

---

## H-38

Convertido en:

ADR-010

---

# Hallazgos Pendientes

## H-05

Estado: Pendiente

Motivo:

Evaluar si RNF-18 debe reformularse tras la prueba de concepto.

---

## H-20

Estado: Pendiente

Motivo:

Validación de semántica de géneros.

Asociado a:

OD-06
OD-07

---

## H-21

Estado: Pendiente

Motivo:

Definición formal de las métricas de transición.

---

## H-22

Estado: Pendiente

Motivo:

Extender trazabilidad RNF ↔ pruebas.

---

## H-29

Estado: Pendiente

Motivo:

Revisión de métricas de evaluación tras ADR-009.

---

## H-32

Estado: Pendiente

Motivo:

Diseño detallado del solver COP.

---

## H-37

Estado: Pendiente

Motivo:

Modelo de concurrencia de la aplicación.

Relacionado con:

ADR-008.

---

# Hallazgos Aparcados

Se consideran fuera del alcance inmediato.

Serán revisados durante:

- Implementación.
- Validación.
- Redacción final de la memoria.

Lista:

- H-02
- H-13
- H-14
- H-15
- H-16
- H-18
- H-23
- H-24
- H-25
- H-30
- H-31
- H-33
- H-34
- H-40
- H-41
- H-42
- H-43

---

# Nuevos Hallazgos Detectados Durante la Consolidación

## N-01

Faltaban ADR-007, ADR-008 y ADR-009.

Estado:

Resuelto.

---

## N-02

M3U8 no estaba respaldado por requisitos.

Estado:

Resuelto.

RF-21b añadido.

---

## N-03

Conflicto entre identidad acústica y rendimiento de reescaneo.

Estado:

Abierto.

Se gestiona mediante ADR-010.

---

## N-04

Compatibilidad de licencias.

Estado:

Abierto.

Gestionado mediante ADR-007.

---

## N-05

README principal desalineado.

Estado:

Resuelto.

---

## N-06

Vocabulario inconsistente entre documentos.

Estado:

Parcialmente resuelto.

Pendiente validación final.

---

## N-07

ADR-005 describía CSP mientras el problema era realmente COP.

Estado:

Resuelto.

---

## N-08

Cobertura insuficiente de RNF en trazabilidad.

Estado:

Parcialmente resuelto.

---

# Riesgos Abiertos

## R-01

Viabilidad de Essentia en Windows.

Impacto:

Alto.

Documentos afectados:

ADR-003
ADR-007
ADR-008

---

## R-02

Prueba de importación/exportación Rekordbox.

Impacto:

Alto.

Documento afectado:

ADR-006

---

## R-03

Identificación permanente de pistas.

Impacto:

Alto.

Documento afectado:

ADR-010

---

## R-04

Definición definitiva del dominio.

Impacto:

Alto.

Documento afectado:

data-model.md

---

# Decisiones Abiertas

Consultar:

open-decisions.md

Actualmente:

- OD-01
- OD-02
- OD-03
- OD-04
- OD-05
- OD-06
- OD-07
- OD-08

continúan abiertas.

---

# Próximas Acciones

## Prioridad 1

Validar con los tutores:

- OD-01
- OD-02
- OD-03
- OD-04
- OD-05
- OD-06
- OD-07
- OD-08

---

## Prioridad 2

Diseñar:

docs/architecture/data-model.md

Incluyendo:

- dominio,
- MER,
- modelo relacional,
- diseño físico SQLite.

---

## Prioridad 3

Actualizar memoria:

Capítulo 4

para reflejar:

- ADR-001..ADR-010.
- Cambios de alcance.
- Desviaciones respecto al anteproyecto.

---

# Veredicto

La fase de análisis puede considerarse cerrada.

La arquitectura de alto nivel puede considerarse cerrada.

El proyecto está preparado para iniciar:

- diseño del dominio,
- diseño del modelo de datos,
- diseño físico SQLite,

manteniendo abiertas únicamente las decisiones registradas en open-decisions.md.
