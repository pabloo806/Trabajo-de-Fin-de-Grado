# Base de Datos

## Descripción

Este directorio contendrá la implementación física de la persistencia del proyecto SetlistGen.

La tecnología de persistencia aceptada es:

```text
SQLite
```

de acuerdo con:

- ADR-004 Persistencia.
- ADR-002 Arquitectura General.
- ADR-001 Forma de Distribución del Sistema.

La definición conceptual y lógica del modelo de datos se desarrolla en:

```text
docs/architecture/data-model.md
```

y constituye la fuente de verdad para cualquier implementación física futura.

---

# Estado Actual

🔄 Diseño en progreso.

Actualmente el proyecto se encuentra en la fase:

```text
Modelo de Dominio
↓
Modelo Conceptual
↓
Modelo Entidad-Relación
↓
Modelo Relacional
↓
Diseño Físico SQLite
```

Todavía no existe un esquema físico definitivo.

---

# Objetivos de Persistencia

La persistencia deberá permitir:

- Mantener una identidad estable para las pistas musicales.
- Evitar reanálisis innecesarios.
- Gestionar múltiples motores de análisis.
- Mantener histórico completo de análisis.
- Mantener histórico completo de generación de setlists.
- Soportar comparación frente a Rekordbox.
- Garantizar trazabilidad de resultados.
- Garantizar reproducibilidad de la generación.
- Mantener compatibilidad con los requisitos RF y RNF definidos en el SRS.

---

# Entidades Candidatas

Las entidades actualmente identificadas durante la fase de diseño son:

## Track

Representa una pista musical única dentro del sistema.

---

## TrackLocation

Representa una ubicación física concreta de una pista.

Permite gestionar:

- pistas movidas,
- pistas duplicadas,
- pistas ausentes.

---

## TrackMetadata

Representa los metadatos obtenidos desde etiquetas.

---

## AnalysisRun

Representa una ejecución concreta de un motor MIR.

---

## AnalysisResult

Representa el resultado producido por un motor de análisis.

---

## GenerationRequest

Representa una solicitud de generación de setlist.

---

## GenreSegment

Representa restricciones temporales de género.

---

## Anchor

Representa una pista anclada en una posición determinada.

---

## Setlist

Representa un setlist generado.

---

## SetlistTrack

Relaciona pistas y setlists.

---

## Transition

Representa la evaluación de una transición entre dos pistas.

⚠️ Su persistencia sigue pendiente de validación (OD-06).

---

## ReferenceMeasurement

Representa los datos obtenidos desde Rekordbox para validación.

---

## EvaluationReport

Representa los resultados agregados del proceso de evaluación.

---

# Decisiones Abiertas que Afectan a la Persistencia

## OD-03 · Identidad Permanente de Pistas

Puede modificar:

- Track
- TrackLocation

---

## OD-04 · Persistencia Multi-Motor

Puede modificar:

- AnalysisRun
- AnalysisResult

---

## OD-05 · Entidad Library

Puede introducir o eliminar relaciones de agrupación de pistas.

---

## OD-06 · Persistencia de Transiciones

Puede modificar:

- Transition

---

## OD-07 · Validación del Modelo de Dominio

Puede afectar al conjunto definitivo de entidades.

---

# Principios de Diseño

## P01 · Identidad independiente de la ruta

La identidad lógica de una pista no depende de:

- nombre de fichero,
- ruta,
- carpeta.

---

## P02 · Soporte Multi-Motor

Una pista puede disponer de múltiples resultados de análisis.

Ejemplo:

```text
Track
 ├── Essentia
 ├── Librosa
 └── Madmom
```

---

## P03 · Trazabilidad

Todo resultado deberá registrar:

- motor,
- versión,
- fecha,
- configuración.

---

## P04 · Reproducibilidad

Todo setlist generado deberá poder reconstruirse mediante:

- parámetros,
- semilla,
- biblioteca.

---

## P05 · Persistencia Histórica

Los análisis y setlists históricos no deben sobrescribirse.

---

# Diseño Físico Previsto

La estructura definitiva se generará a partir del documento:

```text
docs/architecture/data-model.md
```

e incluirá:

```text
PK
FK
UNIQUE
CHECK
Índices
Restricciones de integridad
```

adaptadas a SQLite.

---

# Migraciones

Pendiente de diseño.

La estrategia deberá cumplir:

- RNF-17 Integridad de datos.
- RNF-27 Migraciones de esquema.

---

# Estructura Prevista

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

# Dependencias Documentales

Este directorio depende directamente de:

```text
requirements.md
use-cases.md
traceability-matrix.md
glosario.md

ADR-004
ADR-005
ADR-009
ADR-010

data-model.md
```

---

# Próximo Hito

Generar:

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

Una vez validado dicho documento, podrá iniciarse la implementación del esquema SQLite definitivo.
