# Código fuente de SetlistGen

> Destino en el repositorio: `src/setlistgen/README.md`. Sustituye a `backend/README.md` (ver `docs/architecture/README.md`, sección 4).

**Versión:** 2.0 · **Fecha:** 2026-11-14 · **Estado:** dominio **diseñado y comprobado como especificación**, aún **no incorporado al repositorio**; el resto de capas, sin implementar

> No hay código ejecutable en `src/`. El dominio existe como código de especificación en [`domain-model.md`](../../docs/architecture/domain-model.md) (sección 8). Se copiará a `src/setlistgen/domain/` cuando el modelo se valide y el repositorio se reorganice (N-25). La estructura de paquetes es la propuesta de ADR-008, pendiente de validar (OD-08).

## Requisitos

| Aspecto | Requisito |
|---|---|
| Python | **3.10 o superior**, por las uniones `X \| Y` en tiempo de ejecución y `dataclass(slots=True)`. El dominio v0.2 se ha ejecutado en Python 3.12. **No se ha ejecutado en 3.10**: la cota procede de la inspección del código. La versión definitiva se fija en ADR-008 |
| Dominio | Solo biblioteca estándar (RNF-22) |
| SQLite | 3.37 o superior (infraestructura de persistencia) |
| Instalación | Pendiente: entorno reproducible con dependencias fijadas (RNF-20, ADR-008) |

## Estructura

```text
src/setlistgen/
├── domain/              Dominio puro
├── application/
│   ├── use_cases/       CU-01 a CU-11
│   └── ports/           Puertos (typing.Protocol)
├── infrastructure/      Adaptadores: analysis, metadata, scanning, identification,
│                        persistence (con migrations/), export, reference
├── presentation/        Interfaz gráfica
└── bootstrap/           Composición de dependencias y punto de entrada
```

## Reglas de dependencia

| Capa | Puede importar | No puede importar |
|---|---|---|
| `domain` | Biblioteca estándar | Todo lo demás |
| `application` | `domain` | `infrastructure`, `presentation`, librerías externas |
| `infrastructure` | `application`, `domain`, librerías externas | `presentation` |
| `presentation` | `application`, `domain` (solo para mostrar) | `infrastructure` |
| `bootstrap` | Todas | — |

## Estado por capa

| Capa | Estado |
|---|---|
| `domain` | Especificación ejecutable v0.2, **provisional** (supuestos OD-03 a OD-07). No está en `src/` |
| `application` | Puertos y casos de uso definidos en ADR-002 y `use-cases.md`; sin código |
| `infrastructure` | Sin código. El esquema de persistencia está escrito (`persistence/migrations/`) |
| `presentation` | Sin código. Tecnología propuesta: PySide6 (ADR-008) |
| `bootstrap` | Sin código |

## Aislamiento del dominio

Estado comprobado sobre los diez módulos del dominio v0.2:

| Comprobación | Resultado |
|---|---|
| Importaciones fuera de la biblioteca estándar | **Ninguna.** Solo `dataclasses`, `enum`, `typing`, `collections`, `datetime`, `math`, `uuid`, `unicodedata` y `__future__` |
| Importaciones hacia otras capas | Ninguna. Los únicos `setlistgen.*` importados son del propio dominio |
| Dependencia de SQLite, Rekordbox o librerías MIR | Ninguna |
| Rutas | El dominio las trata como texto Unicode, sin `pathlib` ni formato de sistema operativo (RNF-21) |
| Comprobación automática en CI (T-ARQ-01) | **Pendiente.** Hoy es inspección con `ast`, no una prueba del repositorio |

## Módulos del dominio

| Módulo | Contenido |
|---|---|
| `values.py` | Identificadores y objetos de valor: `Bpm`, `Duration`, `MusicalKey`, `CamelotKey`, `EngineRef`, `DescriptorFailure`, `HarmonicPolicy` |
| `catalog.py` | Agregado Catálogo: `Track`, `TrackLocation`, `TrackFingerprint`, `TrackMetadata` |
| `analysis.py` | `AnalysisResult` |
| `generation.py` | `Setlist`, `SetlistTrack`, `GenerationRequest`, `Transition`, contrato `SetlistGenerator` y resultados `Solution`, `Infeasible`, `LimitReached` |
| `candidates.py` | Selección de candidatas y pre-filtro |
| `request_checks.py` | Validación completa de parámetros |
| `recognition.py` | Reconocimiento de pistas en dos niveles |
| `evaluation.py` | `ReferenceMeasurement`, `EvaluationReport`, `ProportionMetric` |
| `services.py` | Compatibilidad armónica, evaluación de transiciones, validación y ensamblado de setlists |
| `evaluation_services.py` | Emparejamiento de referencias, clasificación de errores y evaluación |

## Lo que el dominio ofrece a las otras capas

- **Servicios sin estado:** los ocho de `domain-model.md`, sección 7.
- **Contrato del resolutor:** `SetlistGenerator.generate(candidates, request)`, que implementa el propio dominio.
- **Puertos que la capa de aplicación debe definir:** `LibraryScanner`, `MetadataReader`, `AudioAnalyzer`, `TrackIdentifier`, `TrackRepository` (solo Catálogo), `AnalysisResultRepository`, `SetlistRepository`, `StatisticsRepository`, `EvaluationRepository`, `SetlistExporter` y `ReferenceDataProvider`.
- **Conversión en el límite:** `None` de `rekordbox_version` ↔ `'unknown'` en la base; `datetime` con zona UTC; rutas decodificadas antes de entrar al dominio.

## Pruebas

Las pruebas de humo que se ejecutaron sobre el dominio v0.2 cubren las 24 tonalidades frente a la tabla de la memoria, la no transitividad de la compatibilidad armónica, los resultados del reconocimiento, la selección de candidatas, el ensamblado y la edición de setlists, el emparejamiento de referencias y las métricas con fallos en el denominador. **No son pruebas del repositorio.** Se convertirán en `pytest` bajo `tests/unit/domain/` y se asociarán a los casos T-CU01-05, T-CU05-xx, T-CU11-xx y T-ID-xx de la matriz.

## Próximos pasos

1. Validar OD-03 a OD-08 con los tutores.
2. Reorganizar el repositorio y copiar el dominio a `src/setlistgen/domain/` con sus pruebas.
3. Crear `tests/architecture/` con la comprobación de la regla de dependencia.
4. Ejecutar la prueba de concepto de identificación y de análisis.
5. Implementar el aplicador de migraciones y los repositorios SQLite.

## Documentación relacionada

[`data-model.md`](../../docs/architecture/data-model.md), [`domain-model.md`](../../docs/architecture/domain-model.md), [`docs/architecture/README.md`](../../docs/architecture/README.md), ADR-002, ADR-005 y ADR-008.
