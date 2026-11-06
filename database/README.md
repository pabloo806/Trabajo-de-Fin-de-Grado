# Base de Datos

## Descripción

Este directorio contendrá la implementación física de la persistencia del proyecto SetlistGen.

La tecnología de persistencia aceptada es:

```text
SQLite
```

según ADR-004.

Actualmente no existe todavía un esquema físico definitivo. El proyecto se encuentra en fase de diseño del dominio y del modelo de datos.

La fuente de verdad para el diseño de persistencia será:

```text
docs/architecture/data-model.md
```

---

# Estado Actual

🔄 Diseño en progreso.

Situación del proyecto:

```text
Análisis ✅
Arquitectura ✅
Modelo de Dominio 🔄
Modelo de Datos 🔄
Persistencia SQLite ⏳
Implementación ⏳
```

---

# Objetivos de Persistencia

La persistencia deberá permitir:

- Mantener una identidad estable para las pistas musicales.
- Evitar reanálisis innecesarios.
- Gestionar múltiples motores de análisis.
- Mantener trazabilidad de resultados.
- Mantener histórico de generación de setlists.
- Permitir evaluación frente a Rekordbox.
- Garantizar reproducibilidad de los resultados.

---

# Entidades Actualmente Propuestas

Estas entidades proceden del SRS v4.0, casos de uso, glosario y ADRs consolidados.

## Entidades principales

- Track
- TrackLocation
- TrackMetadata
- AnalysisRun
- AnalysisResult
- GenerationRequest
- GenreSegment
- Anchor
- Setlist
- SetlistTrack
- Transition
- ReferenceMeasurement
- EvaluationReport

---

# Decisiones Abiertas

Las siguientes decisiones afectan directamente al diseño de persistencia:

## OD-03 · Identificación permanente de pistas

Pendiente de validación.

Impacta sobre:

- Track
- TrackLocation

---

## OD-04 · Persistencia multi-motor

Pendiente de validación.

Impacta sobre:

- AnalysisRun
- AnalysisResult

---

## OD-05 · Entidad Library

Pendiente de validación.

Impacta sobre el modelo conceptual.

---

## OD-06 · Persistencia de transiciones

Pendiente de validación.

Impacta sobre:

- Transition

---

## OD-07 · Validación del modelo de dominio

Pendiente de validación.

Impacta sobre el conjunto final de entidades.

---

# Principios de Diseño

## Identidad independiente de la ruta

La identidad lógica de una pista no dependerá de:

- ruta,
- carpeta,
- nombre del fichero.

## Persistencia histórica

Los resultados históricos no se sobrescribirán.

## Multi-motor

Una misma pista podrá disponer de múltiples resultados de análisis.

## Reproducibilidad

Todo setlist deberá poder reconstruirse a partir de:

- parámetros,
- semilla,
- biblioteca.

## Trazabilidad

Todo resultado almacenado deberá registrar:

- motor,
- versión,
- fecha,
- configuración.

---

# Contenido Futuro

Este directorio albergará:

```text
database/
├── README.md
├── schema/
│   └── schema.sql
├── migrations/
├── seed/
├── scripts/
└── diagrams/
```

---

# Dependencias

El diseño de persistencia depende de:

- requirements.md
- use-cases.md
- traceability-matrix.md
- glosario.md
- ADR-004
- ADR-009
- ADR-010
- data-model.md

---

# Próximo Hito

Completar:

```text
docs/architecture/data-model.md
```

incluyendo:

- Modelo de dominio.
- Modelo conceptual.
- MER.
- Modelo relacional.
- Justificación de entidades.
- Diseño físico preliminar SQLite.

Una vez validado dicho documento comenzará la implementación del esquema SQLite definitivo.
