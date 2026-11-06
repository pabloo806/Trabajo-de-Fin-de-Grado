# Backend

## Descripción

Este directorio contendrá la implementación principal de SetlistGen.

El backend será responsable de:

- Importación de bibliotecas musicales.
- Extracción de metadatos.
- Identificación permanente de pistas.
- Análisis musical.
- Persistencia SQLite.
- Generación de setlists.
- Exportación a Rekordbox.
- Evaluación frente a datos de referencia.

La implementación seguirá los principios definidos en:

- ADR-001 Distribución.
- ADR-002 Arquitectura General.
- ADR-003 Motor de Análisis Musical.
- ADR-004 Persistencia.
- ADR-005 Generación de Setlists.

---

## Arquitectura

El backend se desarrollará siguiendo:

```text
Clean Architecture
```

y una organización basada en:

```text
domain
application
infrastructure
presentation
```

---

## Estructura prevista

```text
backend/
└── src/
    └── setlistgen/
        ├── domain/
        ├── application/
        ├── infrastructure/
        └── presentation/
```

---

## Componentes previstos

### Importación

- LibraryScanner
- MetadataReader
- TrackIdentifier

### Análisis

- AudioAnalyzer
- AnalysisRun
- AnalysisResult

### Persistencia

- TrackRepository
- SetlistRepository
- StatisticsRepository
- EvaluationRepository

### Generación

- SetlistGenerationService
- TransitionEvaluationService

### Exportación

- SetlistExporter

### Evaluación

- ReferenceDataProvider
- EvaluationService

---

## Tecnologías previstas

| Área | Tecnología |
|--------|------------|
| Lenguaje | Python |
| Persistencia | SQLite |
| Testing | pytest |

---

## Estado

🔄 Pendiente de implementación.

El diseño de dominio y persistencia se encuentra actualmente en elaboración mediante:

```text
docs/architecture/data-model.md
```
