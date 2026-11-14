# Revisión Técnica de la Documentación

> Destino en el repositorio: `docs/project-management/audit-review.md`.

**Proyecto:** SetlistGen · Sistema de Generación Automática de Setlists para DJs
**Versión:** 3.2 (auditoría previa a la reunión con tutores; sustituye a todas las anteriores)
**Fecha:** 2026-11-14
**Estado:** línea base documental consistente, con diseño detallado **provisional**, pendiente de validación por tutor y cotutor

---

# 1. Propósito y alcance

Este documento recoge el estado real del proyecto tras tres revisiones técnicas: la auditoría inicial, la consolidación documental y esta **auditoría cruzada** realizada al cerrar el diseño detallado de forma provisional. Sirve para tres fines:

1. Dejar constancia de qué está cerrado, qué está pendiente y qué es una hipótesis sin verificar.
2. Fijar los hallazgos, riesgos y dependencias que condicionan la reunión con tutor y cotutor y la fase siguiente.
3. Servir de punto de partida para congelar la línea base documental y el modelo de datos.

Las decisiones que esperan validación de los tutores están en `open-decisions.md` (v3.2).

## 1.1 Cobertura de la revisión

| Fuente | Revisión |
|---|---|
| Requisitos v4.0, casos de uso v1.1, matriz v3.0, glosario v2.1 | Completa, con comprobaciones automáticas y lectura cruzada |
| ADR-001 a ADR-010 | Completa; contrastados con el diseño detallado |
| Serie de datos (`data-model.md`, `domain-model.md`, `conceptual-model.md`, `er-model.md`, `database-schema.md`, DDL) | Completa, con comprobaciones automáticas y ejecución del DDL |
| READMEs de `docs/architecture`, `src/setlistgen` y persistencia | Completa |
| READMEs antiguos (`backend`, `frontend`, `database`, `docs`, `tests`, `scripts`, `docs/project-management`) y `README.md` raíz | Leídos como parte del material aportado; ver N-47, N-58 y N-59 |
| Memoria (`book.pdf`, capítulos 1 a 4) | Completa, sin cambios desde la revisión anterior (N-27) |
| Anteproyecto aprobado | Contrastado en lo relativo a objetivos (N-47) |
| Estructura real de `src/` y estado de `main` y `develop` | **No verificado.** Se toma el informe del autor |
| Normativa específica de la EPS | Parcial: artículos 1 a 9 (revisión anterior). **No revisada de nuevo** |
| Normativa general de TFG y CV | **No revisadas** |
| Repositorio de GitHub e issues | **No verificados** |

## 1.2 Método de esta auditoría

| Técnica | Alcance |
|---|---|
| Comprobaciones automáticas | Identificadores definidos y referenciados; prioridades MoSCoW; trazabilidad RF → CU; cobertura de pruebas; estados de los ADR; correspondencia entre el MER y el DDL (entidades, columnas y tipos); redacción conversacional en documentos de repositorio |
| Ejecución | DDL en SQLite 3.45.1 con batería de integridad (`database-schema.md`, sección 5); dominio v0.2 con pruebas de humo; análisis de importaciones con `ast` |
| Lectura cruzada | Dominio ↔ ADR ↔ casos de uso ↔ glosario ↔ esquema ↔ READMEs |

**Límites.** Las comprobaciones automáticas no cubren la equivalencia de nulabilidad y restricciones entre el MER y el DDL, ni recalculan las puntuaciones de los ADR (no han cambiado desde la segunda auditoría). El script usado no está en el repositorio (acción 10, sección 9).

## 1.3 Correcciones aplicadas durante la auditoría

| Documento | Versión | Corrección |
|---|---|---|
| `er-model.md` | 0.1.1 → 0.1.2 | RI-06, `rekordbox_version`, `camelot_code` y estado de M-01 a M-07 alineados con el esquema (N-55) |
| `database-schema.md` | 0.1 → 0.1.1 | Redacción neutra (N-54) y referencia a N-46 |
| `data-model.md` | 1.0 → 1.0.1 | Referencias de versión |
| `docs/architecture/README.md` | 3.0 → 3.0.1 | Referencias de versión y de los documentos de gestión |

---

# 2. Estado de madurez del proyecto

| Fase | Estado | Observación |
|---|---|---|
| Análisis (requisitos, casos de uso, trazabilidad, glosario) | **Cerrado** a nivel de línea base | SRS v4.0, casos de uso v1.1, matriz v3.0, glosario v2.1. Pendiente de validación y de los ajustes N-49 y N-50 |
| Arquitectura de alto nivel | **Cerrada** a nivel de línea base | ADR-001 a ADR-006 aceptados; N-32 y N-48 piden retoques menores |
| Decisiones complementarias | Redactadas, **no validadas** | ADR-007 a ADR-010 propuestos |
| Diseño detallado (dominio, conceptual, MER, esquema SQLite) | **Completado de forma provisional** | Dominio v0.2, conceptual v0.1, MER v0.1.2, esquema v0.1.1 e índice `data-model.md` v1.0.1. Depende de OD-03 a OD-07 |
| Estructura del repositorio | **Aplicada** según el autor | `src/setlistgen/`. No validada (OD-08, N-56) |
| Prueba de concepto (hito H2) | No realizada | Condiciona librería, importación en Rekordbox, identificación, interfaz y empaquetado |
| Implementación, pruebas y validación experimental | No iniciadas | No existe código en `src/`. El dominio es una especificación ejecutable |
| Memoria | Capítulos 1 a 4 redactados | Requiere actualización (sección 7) |

> **Lectura correcta del estado.** Cerrado significa consistente y suficiente para pasar a la fase siguiente. No significa validado por los tutores ni verificado con datos reales.

---

# 3. Línea base documental

## 3.1 Documentos y versiones

| Documento | Versión | Estado |
|---|---|---|
| `requirements.md` (SRS) | 4.0 | Consolidado; 36 RF y 27 RNF |
| `use-cases.md` | 1.1 | Consolidado; 11 casos de uso, 4 críticos |
| `traceability-matrix.md` | 3.0 | Consolidado; 67 casos de prueba |
| `glosario.md` | 2.1 | Consolidado; desactualizado en puntos concretos (N-49) |
| ADR-001 a ADR-006 | Revisados el 2026-10-30 | Aceptados |
| ADR-007 a ADR-010 | Primera redacción | Propuestos |
| `docs/architecture/README.md` | 3.0.1 | Alineado |
| `docs/architecture/data-model.md` | 1.0.1 | Índice de la serie de datos |
| `domain-model.md`, `conceptual-model.md`, `er-model.md`, `database-schema.md` | 0.2, 0.1, 0.1.2, 0.1.1 | Provisionales |
| `open-decisions.md` | 3.2 | Para la reunión |
| `README.md` raíz | Dos versiones aportadas | **Ver N-47** |

## 3.2 Estado de los ADR y condiciones

| ADR | Decisión | Estado | Condición pendiente |
|---|---|---|---|
| ADR-001 | Aplicación de escritorio | Aceptado | Ninguna sobre la decisión |
| ADR-002 | Clean Architecture con puertos y adaptadores | Aceptado | Incorporar `AnalysisResultRepository`, `EvaluationRepository` y retirar `AnalysisRun` (N-32, N-49) |
| ADR-003 | Puerto `AudioAnalyzer`; librería por prueba de concepto | Aceptado | Selección de librería tras la prueba de concepto y ADR-007 |
| ADR-004 | SQLite | Aceptado | Entregable y criterio de cierre: `database-schema.md` y OD-03 a OD-07 (N-32) |
| ADR-005 | Restricciones con función de coste | Aceptado | Validar la búsqueda con prototipo; precisar la reducción previa por género (N-48) |
| ADR-006 | XML de Rekordbox con M3U8 complementario | Aceptado | Verificación mediante la prueba de importación |
| ADR-007 | Licencias y compatibilidad legal | Propuesto | Inventario verificado y validación (OD-08) |
| ADR-008 | Lenguaje, interfaz y empaquetado | Propuesto | Prueba de interfaz y empaquetado; recoger la estructura adoptada (N-57) |
| ADR-009 | Conjunto de evaluación y protocolo | Propuesto | Prueba de concepto; tratamiento de fallos (N-52) |
| ADR-010 | Identificación permanente de pistas | Propuesto | Prueba de identificación y validación (OD-03) |

## 3.3 Resultado de las comprobaciones automáticas

| Comprobación | Resultado |
|---|---|
| IDs definidos | 36 RF, 27 RNF, 11 CU y 10 ADR; 67 pruebas |
| Referencias a RF, RNF, CU, ADR, OD y CMP | **Ninguna rota**, incluidos los documentos nuevos |
| Pruebas citadas | Todas existen en la matriz |
| Cobertura de pruebas | Cada RF y cada RNF tiene al menos una (sin cambios) |
| Prioridades MoSCoW | RF: 27 Must, 3 Should y 6 Could. RNF: 22 Must y 5 Should |
| Trazabilidad RF → CU | Idéntica en casos de uso y matriz (36 de 36) |
| Casos de uso críticos | CU-01, CU-05, CU-07 y CU-11 en matriz y casos de uso |
| MER ↔ DDL | 19 entidades del MER ↔ 19 tablas del DDL, más `schema_migration` (técnica). La única diferencia es `LIBRARY` y `track_location.library_id`, condicionadas a OD-05 |
| Tipos MER ↔ DDL | Sin incoherencias con la correspondencia UUID, String y DateTime → TEXT; Integer y Boolean → INTEGER; Float → REAL |
| DDL ejecutado | Creado en SQLite 3.45.1; restricciones, claves foráneas, índice parcial, columna generada y migración 2 verificados |
| Dominio v0.2 | Solo importa la biblioteca estándar; sus únicos `setlistgen.*` son del propio dominio |
| Redacción de documentos de repositorio | Dos fragmentos conversacionales en `database-schema.md` (corregidos) |
| Vocabulario obsoleto | `AnalysisRun` sigue en ADR-002, el glosario y el README antiguo de arquitectura (N-49) |

---

# 4. Hallazgos

Gravedad: **Alta**, **Media** o **Baja**. Estados: *Resuelto*, *Resuelto (provisional)* (depende de validación), *Aceptado como limitación*, *Abierto*, *Pendiente*.

## 4.1 Resumen de la fase

| Concepto | Cifra |
|---|---|
| Hallazgos **abiertos o pendientes** | **35** (Alta 3, Media 20, Baja 12) |
| Resueltos o cerrados en esta fase | 12 (más M-01 a M-07 y C-01 a C-08) |
| Hallazgos del MER (M-01 a M-07) | 7: 5 resueltos y 2 aceptados como limitación |
| Hallazgos del contraste con los casos de uso (C-01 a C-08) | 8, todos aplicados en `domain-model.md` v0.2 |

Las tres de gravedad **Alta** abiertas: N-03 y N-04 (dependen de la prueba de concepto) y **N-47** (README raíz), que debe corregirse **antes de la reunión**.

## 4.2 Resueltos o cerrados en esta fase

| ID | Gravedad | Problema | Resolución |
|---|---|---|---|
| N-25 | Alta | El repositorio conservaba `backend`, `frontend` y `database`, propios de una arquitectura cliente-servidor descartada. | Resuelto según informe del autor: estructura `src/setlistgen/` adoptada y carpetas eliminadas. **No verificado en esta auditoría.** Pendiente de OD-08 (N-56). |
| N-26 | Media | `Track` tenía un único campo `fingerprint`; ADR-010 exige al menos dos huellas. | Resuelto en el diseño (provisional): `TrackFingerprint` con tipo y versión (D-04) y tabla `track_fingerprint`. Depende de OD-03 y OD-07. |
| N-31 | Media | `AnalysisRun` sin identidad ni comportamiento propios. | Resuelto en el diseño (provisional): absorbido en `EngineRef` y `analysis_engine`. La propagación al glosario y a ADR-002 se sigue en N-49. |
| N-33 | Media | Faltaba un criterio de clasificación de errores (octava, relativa, quinta, paralela). | Resuelto: `EstimationErrorClassifier` en el dominio v0.2. |
| N-35 | Baja | La instrucción de «transitividad Camelot» era inexacta. | Resuelto: la compatibilidad no es transitiva (IN-12). |
| N-41 | Baja | `path_normalized` ignora mayúsculas. | Cerrado por duplicado de N-37. |
| N-45 | Media | El recuento de tablas del MER decía dieciocho y son diecinueve (más `LIBRARY` condicionada). | Resuelto en `er-model.md`. |
| N-46 | Media | ADR-004 y `database/README.md` citaban `data-model.md` como entregable único. | Resuelto: `data-model.md` es el índice de la serie (v1.0.1). El texto de ADR-004 se sigue en N-32. |
| N-23 | Baja | Existían dos versiones del README de arquitectura. | Resuelto: `docs/architecture/README.md` v3.0.1. Comprobar que no queda `README-architecture.md`. |
| N-54 | Media | `database-schema.md` contenía redacción conversacional («Tu enunciado…», «Decisión mía…»). | Resuelto en esta auditoría: v0.1.1. |
| N-55 | Media | `er-model.md` quedó desactualizado frente al esquema: RI-06 decía «distinto de `moved`», `rekordbox_version` aparecía nulable, `camelot_code` pendiente y M-01 a M-07 como abiertos. | Resuelto en esta auditoría: v0.1.2. |
| H-35 | Alta | Modelo de dominio completo. | Resuelto en el diseño (provisional): `domain-model.md` v0.2. Pendiente de validar OD-07. |

## 4.3 Hallazgos del MER (M-01 a M-07)

| ID | Gravedad | Problema | Resolución |
|---|---|---|---|
| M-01 | Alta | Una ruta puede reaparecer en otra pista cuando la anterior quedó histórica. | Resuelto: índice único parcial sobre ubicaciones vigentes (`active` y `failed`). `absent` y `moved` quedan fuera para no romper CU-02 A3. |
| M-02 | Media | La política armónica es un conjunto de movimientos, no columnas simples. | Resuelto: tabla hija `request_harmonic_move`. |
| M-03 | Media | El informe de importación no se persiste. | Aceptado como limitación (DD-11). Confirmar con los tutores junto con OD-05. |
| M-04 | Media | Un informe de evaluación no se recalcula pista a pista. | Aceptado como limitación (DD-12). La trazabilidad por pista vive en el manifiesto de ADR-009. Confirmar con OD-10. |
| M-05 | Baja | `rekordbox_version` nulo complica la unicidad. | Resuelto: valor `'unknown'` por defecto, no nulo. |
| M-06 | Baja | `camelot_code` es derivado. | Resuelto: columna generada y almacenada. |
| M-07 | Baja | `APP_SETTING` como tabla de una fila. | Resuelto: se mantiene en la base (un único fichero, ADR-004). |

## 4.4 Hallazgos del contraste con los casos de uso (C-01 a C-08)

| ID | Gravedad | Problema | Resolución en `domain-model.md` v0.2 |
|---|---|---|---|
| C-01 | Alta | Nadie decidía si un fichero era nuevo, movido, duplicado, modificado o ambiguo (CU-01, CU-02). | `TrackRecognitionService`, `TrackIndex` y `FileObservation`; resultado `NEEDS_FINGERPRINT` añadido. |
| C-02 | Media | Un fichero ilegible no tenía dónde guardar su causa; faltaban operaciones de ubicación. | `failure_cause`, `mark_failed`, `refresh_location` y `last_known_location`. |
| C-03 | Media | Faltaba la regla que construye los descriptores de entrada del generador. | `build_descriptors` y `select_candidates` con motivos de exclusión. |
| C-04 | Alta | Faltaba el contrato del generador y el resultado «solución, inviable o límite agotado» (RF-19). | `SetlistGenerator`, `Solution`, `Infeasible`, `LimitReached`, `OptimalityStatus`, `node_limit` y `time_limit_s`. |
| C-05 | Media | RF-14 permite «tonalidades admitidas» y el modelo solo tenía política. | `allowed_keys` como pre-filtro (DD-04). |
| C-06 | Media | Una referencia sin pista no podía representarse; el informe guardaba solo contadores. | `ReferenceRecord`, `ReferenceMatchResult`, listas de exclusión y `estimation_failures`. |
| C-07 | Baja | El constructor lanzaba un solo error por solicitud inválida. | `check_request_inputs` devuelve todas las incidencias con acción sugerida. |
| C-08 | Media | Faltaba la instantánea del setlist y la posición original. | `SetlistTrack` con instantánea y `original_position`; `SetlistAssemblyService` (supuesto OD-06). |

## 4.5 Abiertos y pendientes: gravedad Alta

| ID | Problema | Impacto | Propuesta de corrección | Estado |
|---|---|---|---|---|
| N-03 | Identidad acústica frente al rendimiento de reescaneo (RNF-04). | Dominio y persistencia: reconocimiento, huellas e índices. | Dos niveles (ADR-010), ya reflejado en `TrackRecognitionService` y `track_fingerprint`. Falta validar OD-03 y medir en la prueba de identificación (T-ID-08). | Abierto (diseño listo, sin medir) |
| N-04 | Licencias e instalación de las librerías candidatas, incluida la versión de SQLite y de Python que traen los sistemas. | Elección de motor, empaquetado y creación del esquema (`STRICT` exige SQLite 3.37 o superior). | Verificar en la prueba de concepto (ADR-003, ADR-007, ADR-008). Comprobar la versión de SQLite al arrancar y probar en Windows y macOS (R-11). | Abierto |
| N-47 | Se aportaron **dos versiones distintas** de `README.md`. La titulada «Generador Inteligente» renumera los objetivos (O3 estimar, O4 Camelot, O5 base de datos, O6 generar, O7 evaluar), omite exportación y panel y no coincide con el anteproyecto, el SRS ni la memoria 1.3.2. Su tabla de estado da por pendientes el dominio, el modelo de datos y SQLite, su «Próximo hito» ya está cumplido y describe la estructura anterior. | Contradice la fuente oficial (anteproyecto) y la trazabilidad O1 a O7. Es la primera página que ven tutores y tribunal. | Verificar cuál está en `main`. Restaurar los objetivos de la memoria 1.3.2, actualizar estado, estructura `src/` y enlaces, y corregirlo **antes de la reunión**. | Abierto |

## 4.6 Abiertos y pendientes: gravedad Media

| ID | Problema | Impacto | Propuesta de corrección | Estado |
|---|---|---|---|---|
| N-16 | Los ADR se aceptaron antes de la prueba de concepto, contra el plan del anteproyecto. | Planificación y memoria. | Registrar la desviación en la memoria (4.4). Cuestión C-03. | Abierto |
| N-17 | `Transition` y `Library` tienen definiciones distintas según el documento: el SRS (sección 7) y el glosario los listan como entidades de dominio; el diseño trata `Transition` como objeto de valor con instantánea y deja `Library` fuera. | Modelo de dominio y vocabulario. | Resolver con OD-05, OD-06 y OD-07 y alinear SRS 7 y glosario (N-49). | Abierto (parcial) |
| N-27 | La memoria (4.1.3, 4.4 y 4.6) describe 29 requisitos funcionales y todas las decisiones como abiertas. | Memoria. | Actualizar (sección 7) después de la reunión. | Abierto |
| N-28 | El límite de la búsqueda se expresa en nodos (determinismo, RNF-11) y RNF-03 exige 60 s. El valor por defecto `node_limit = 100 000` no tiene base. | Calibración del generador. | Calibrar con el benchmark de RNF-03 y el prototipo (H-32). | Abierto |
| N-29 | El intervalo de género por instante de inicio es un supuesto de ADR-005, ya implementado en `SetlistValidatorService`. | Dominio, RF-15. | Confirmar en OD-07, cuestión 4. | Abierto (supuesto aplicado) |
| N-32 | ADR-002 y ADR-004 no reflejan `AnalysisResultRepository` (`TrackRepository` queda solo para Catálogo), la desaparición de `AnalysisRun` ni los puertos propuestos. ADR-004 mantiene `data-model.md` como entregable único y criterio de cierre. | Coherencia entre ADR aceptados y diseño detallado. | Revisión menor de ADR-002 (tabla de puertos y entidades) y de ADR-004 (entregable y criterio de cierre). Texto exacto en `data-model.md`, sección 5. Aplicar tras la reunión. | Abierto (confirmado en diseño) |
| N-36 | El nivel 1b exige una pasada de lectura por fichero nuevo o modificado. Su coste real no está medido. | RNF-04. | Medir en la prueba de identificación (T-ID-08). | Abierto |
| N-38 | `ReferenceMatchingService` asocia por ruta. Depende de que el XML de Rekordbox traiga ubicación, BPM y tonalidad (H-17). | RF-29b, CU-11. | Verificar en la prueba de concepto. CSV como alternativa. | Abierto |
| N-40 | `modified_at` se compara por igualdad en el reconocimiento (nivel 1a). Distintos sistemas de ficheros tienen resolución distinta y pueden dar falsos «modificado». | RNF-04, `TrackRecognitionService`. | Normalizar en el adaptador a una resolución fija (microsegundos) antes de comparar y guardar. | Abierto |
| N-48 | ADR-005 (aceptado) dice que la reducción previa filtra candidatas por rango de BPM, **género** y disponibilidad. El dominio v0.2 no filtra por género, porque los segmentos pueden no cubrir todo el setlist (D-12). | Discrepancia entre un ADR aceptado y el dominio; afecta a RNF-03 y a la explicación de conflictos (RF-19). | Mantener D-12 y precisar ADR-005 (filtrar por género solo si los segmentos cubren toda la duración), o implementar el filtro condicional. Cuestión DD-16. | Abierto |
| N-49 | Glosario v2.1, SRS 7 y ADR-002 están desactualizados respecto al diseño: `AnalysisRun` como entidad; `Library` y `Transition` como entidades de dominio; ausencia de `EngineRef` y `AnalysisEngine` en el vocabulario canónico; `Transition` con «persistencia pendiente»; «Biblioteca candidata» sin rango de BPM, tonalidades admitidas ni duración. | Línea base documental frente al diseño. | Tras la reunión: glosario (sustituir `AnalysisRun`; añadir `AnalysisEngine`, `EngineRef`, `TrackFingerprint`, instantánea, `OptimalityStatus`; redefinir candidata y `Transition`), SRS 7.0 y 7 (vocabulario y entidades) y ADR-002 (entidades y puertos). No reabrir antes. | Abierto (tras la reunión) |
| N-50 | Huecos de pruebas tras el diseño detallado. Sin caso en la matriz: `allowed_keys` (RF-14); ancla excluida del pre-filtro; motivos de exclusión de candidatas; setlist histórico inmutable ante cambios de etiquetas (OD-06); reconocimiento sin leer el fichero (`UNCHANGED` y `NEEDS_FINGERPRINT`); audio sustituido en la misma ruta (CU-02 A3); fallos en el denominador (DD-05); restricciones del esquema. | Trazabilidad requisito, prueba. | Añadir a la matriz: T-CU04-02, T-CU05-13, T-CU05-14, T-CU05-15, T-ID-09, T-ID-10, T-CU11-06 y T-ARQ-10 (75 pruebas). Tras la reunión. | Abierto |
| N-51 | RF-03 admite una duración nula, pero RF-12 necesita la duración de cada pista. El dominio excluye de las candidatas las pistas sin duración (`NO_DURATION`) y CU-05 paso 5 no lo menciona. | CU-05, glosario. | Obtener la duración al decodificar el audio durante el análisis o informar de la exclusión al DJ. Cuestión DD-17. | Abierto |
| N-52 | ADR-009 excluye «ficheros ilegibles» de la muestra, pero el diseño cuenta como fallo cualquier fallo de estimación (DD-05). El límite entre ambos no está definido. | Interpretación de RNF-05 a RNF-09. | Distinguir fichero ilegible para todos los motores (excluido) y fallo propio de un motor (cuenta como fallo). Cuestión OD-10, 5. | Abierto |
| N-56 | La reorganización de `src/` y la línea base provisional se han consolidado en `main` antes de validar OD-08. La memoria (4.2.1) describe `main` como rama de versiones estables. | Planificación (como N-16) y gestión de la configuración. | Registrar la desviación en la memoria (4.4). Etiquetar `baseline-provisional-2026-11-14` y, tras la validación, `baseline-v1`. Cuestiones C-03 y C-06. | Abierto |
| H-20 | Semántica de los géneros: el dominio normaliza mayúsculas y espacios y compara por igualdad. No hay jerarquías ni sinónimos. | RF-15, coherencia de género. | Decisión de dominio con OD-07; medir con las etiquetas reales (R-03). | Pendiente |
| H-21 | Definición formal de las métricas de transición: la disonancia es la distancia Camelot (+1 si cambia el modo) y la incoherencia de género es 0 o 1. Formas provisionales. | ADR-005, RF-17. | Ratificar con la prueba de concepto y el benchmark (N-34). | Pendiente |
| H-29 | Los umbrales de RNF-05 a RNF-09 son provisionales. ADR-009 define el protocolo. | Validación experimental. | Ratificar tras la prueba de concepto con el conjunto piloto. | Pendiente |
| H-32 | Diseño detallado del resolutor COP. Está definido el contrato `SetlistGenerator` y sus resultados; faltan el algoritmo, el orden de búsqueda y el análisis de relajación. | RNF-03, RF-19. | Prototipo y benchmark; repliegue a Beam Search si no cumple (ADR-005, R-07). | Pendiente (contrato definido) |
| H-37 | Modelo de concurrencia: ADR-004 impone un único escritor. Falta el diseño del coordinador y de `WAL`. | RNF-02, RNF-17. | Diseño de infraestructura e interfaz. | Pendiente |

## 4.7 Abiertos y pendientes: gravedad Baja

| ID | Problema | Impacto | Propuesta de corrección | Estado |
|---|---|---|---|---|
| N-24 | Anotaciones de la consolidación en filas fechadas el 2026-10-30. | Trazabilidad documental. | Unificar al congelar la línea base. | Abierto |
| N-34 | Formas provisionales de la incoherencia de género (0 o 1) y de la disonancia armónica. | Calidad musical del generador. | Ratificar con la prueba de concepto y el benchmark (H-21). | Abierto |
| N-37 | `normalize_path` ignora mayúsculas y unifica separadores. En sistemas sensibles a mayúsculas puede unir rutas distintas y chocar con el índice único parcial. Además asume separadores de Windows dentro del dominio, lo que RNF-21 reserva a infraestructura. | RNF-21, RNF-16, M-01. | Confirmar en la prueba de importación. Alternativa: mover la normalización a infraestructura y que el dominio reciba la clave ya normalizada. (Absorbe a N-41.) | Abierto |
| N-39 | `OptimalityStatus` solo es útil si el resolutor puede demostrar la optimalidad. | ADR-005. | Confirmar en el prototipo (H-32). | Abierto |
| N-42 | La ordenación por título en SQLite distingue mayúsculas y no trata tildes. | RF-11b. | Decidir una `COLLATE` propia o ordenar en memoria al implementar la consulta. | Abierto |
| N-43 | El dominio usa `datetime` sin zona; el esquema espera UTC. | Persistencia, N-40. | Exigir `datetime` con zona UTC en el repositorio. | Abierto |
| N-44 | Los índices `ix_analysis_result_engine_bpm` y `..._camelot` se crearon sin medir su utilidad. | RNF-03, RF-11. | Revisar tras el benchmark de RNF-03. | Abierto |
| N-53 | `EvaluationService` exige al menos una referencia de BPM evaluable. CU-11 no define el caso de una referencia con solo tonalidad. | CU-11, RF-29b. | Definir un flujo alternativo o permitir informes solo de tonalidad. | Abierto |
| N-57 | ADR-008 (sección 4) no recoge la estructura adoptada: `persistence/migrations/` y `pending/`, `repositories/`, `tests/architecture/` y `tests/performance/`. | ADR-008, OD-08. | Actualizar ADR-008 tras la validación. | Abierto |
| N-58 | `docs/project-management/README.md` lista `meeting-notes.md` y `risks.md`, que no figuran entre los documentos aportados. | Gestión. | Verificarlos. Crear `meeting-notes.md` para la reunión (registro de resultados de `open-decisions.md`, sección 8). | Abierto |
| N-59 | La documentación de la interfaz (`presentation/README.md`, antes `frontend/README.md`) enumera funciones sin requisito, como la cancelación de procesos. | Trazabilidad. | Trazar a un requisito (RNF-14) o retirarlas. | Abierto |
| H-05 | Reformulación de RNF-18: ya es medible (cociente ≤ 2,5, provisional). | RNF-18. | Ratificar tras la prueba de concepto. | Pendiente |

## 4.8 Histórico de revisiones anteriores

### Hallazgos de la auditoría inicial resueltos

| ID | Gravedad | Resumen | Resolución |
|---|---|---|---|
| H-01 | Alta | SRS desalineado con los ADR | SRS v4.0 alineado con ADR-001 a ADR-010 |
| H-03 | Alta | Restricciones del generador mal formuladas | ADR-005: restricciones R1 a R7 |
| H-04 | Media | «Salto moderado» de BPM no verificable | RF-13b (OD-02) |
| H-07 | Alta | La evidencia principal dependía de un RF secundario | RF-29 a Must; CU-11 crítico (OD-01) |
| H-08 | Alta | Sin soporte multi-motor | RF-07 a Must; motor activo (OD-04) |
| H-17 | Media | Sin mecanismo para la referencia de Rekordbox | RF-29b |
| H-19 | Alta | Pistas movidas, duplicadas y ausentes sin tratar | RF-09c y flujos de CU-02 y CU-07 |
| H-26 | Media | `PostgreSQLAdapter` y puertos mal ubicados en ADR-002 | ADR-002 corregido |
| H-22 | Media | Trazabilidad RNF ↔ pruebas incompleta | Matriz v3.0 |

Convertidos en ADR: H-11 (ADR-008), H-12 (ADR-007 y ADR-009) y H-38 (ADR-010).

### Hallazgos de la consolidación resueltos

N-01, N-02, N-05 a N-15 (ADR-007 a ADR-009 redactados, RF-21b, READMEs, vocabulario canónico, ADR-005 como COP, matriz v3.0, cabeceras del SRS, requisitos en cada ADR, `PostgreSQLAdapter`, puertos en Aplicación, RF-07 a Must, recuentos y flujos alternativos) y, en la segunda auditoría, N-18 a N-22 (pruebas inexistentes citadas, pruebas T-ID, `EvaluationRepository`, tonalidad paralela en RNF-09 y RNF-12 en la tabla de capas). N-30 (numeración de riesgos) se resolvió adoptando la de la memoria.

### Aparcados

Se revisarán durante la implementación, la validación y la redacción final de la memoria: H-02, H-13, H-14, H-15, H-16, H-18, H-23, H-24, H-25, H-30, H-31, H-33, H-34, H-40, H-41, H-42 y H-43.

---

# 5. Riesgos abiertos

Numeración de la memoria (capítulo 4, tabla 4.2). R-11 a R-14 son propuestas y deben añadirse a la memoria.

| ID | Riesgo | Prob. | Impacto | Estado | Mitigación | Documentos |
|---|---|---|---|---|---|---|
| R-01 | Exactitud insuficiente de BPM y tonalidad | Alta | Alto | Abierto | Prueba de concepto comparativa; desglose de errores; analizador sustituible | ADR-003, ADR-009 |
| R-02 | El fichero exportado no se carga en Rekordbox | Media | Alto | Abierto | Prueba de importación; verificación manual registrada | ADR-006 |
| R-03 | Etiquetas de género incompletas | Alta | Medio | Abierto | RF-15 es Should; promoción según calidad medida | RF-15, ADR-005 |
| R-04 | La referencia de Rekordbox no es una verdad absoluta | Media | Medio | Mitigado en diseño | Discusión en la evaluación; contraste público; auditoría manual; fallos en el denominador | ADR-009 |
| R-05 | Ampliación excesiva del alcance | Alta | Alto | **Vigilar** | RF-09c, RF-13b, RF-29b y RNF-27 amplían el anteproyecto (C-01). Evitar nuevas funciones sin consulta | SRS 9.1 |
| R-06 | Redacción concentrada al final y solapada con la validación | Alta | Alto | Abierto | Memoria incremental. El diseño detallado alimenta los capítulos 6 y 7 | Memoria 4.4 |
| R-07 | El generador no encuentra solución o su coste crece en exceso | Media | Medio | Abierto | Prototipo y benchmark; repliegue a Beam Search | ADR-005 |
| R-08 | Licencias incompatibles con la del repositorio | Media | Medio | Abierto | Inventario y política de ADR-007 | ADR-007 |
| R-09 | Poca disponibilidad de DJs para la valoración | Media | Medio | Abierto | Plan alternativo con métricas objetivas | ADR-009 |
| R-10 | Decisiones tecnológicas tardías que bloquean el diseño | Media | Alto | **Activo** | Cierre tras la reunión y la prueba de concepto; supuestos explícitos | ADR-003 a ADR-010 |
| R-11 | La instalación de las librerías MIR o la versión de SQLite del sistema fallan en Windows o macOS **(propuesto)** | Media | Alto | Abierto | Comprobar SQLite ≥ 3.37 y Python ≥ 3.10 al arrancar; PoC; CI en ambos sistemas | ADR-003, ADR-008 |
| R-12 | La identificación de pistas incumple RNF-04 o fusiona pistas distintas **(propuesto)** | Media | Alto | Abierto | Dos niveles; preferir el falso negativo; prueba de identificación | ADR-010 |
| R-13 | El modelo de datos se congela antes de validar las decisiones abiertas **(propuesto)** | Media | Alto | **Activo, parcialmente mitigado** | Supuestos explícitos, esquema como migración 1, migración 2 preparada y coste de cambio documentado (`open-decisions.md` 3.2) | ADR-004 |
| R-14 | La especificación del dominio (documento) y el código de `src/` divergen **(propuesto)** | Media | Medio | Nuevo | Tras la validación, `src/` es la fuente y el documento remite a él; las pruebas de humo pasan a `pytest` | `domain-model.md` |

---

# 6. Hipótesis sin verificar

Ninguna de estas afirmaciones está comprobada. Cada una tiene un documento y un momento de verificación.

| Hipótesis | Dónde se usa | Verificación |
|---|---|---|
| Essentia tiene licencia copyleft fuerte y puede no instalarse con facilidad en Windows | ADR-003, ADR-007 | Prueba de concepto y lectura de la licencia vigente |
| Los modelos de madmom tienen restricciones de uso no comercial | ADR-003, ADR-007 | Ídem |
| Mutagen tiene licencia copyleft | ADR-003, ADR-007 | Ídem |
| El XML de colección de Rekordbox contiene ubicación, BPM y tonalidad por pista | SRS 2.4, RF-29b, ADR-009, N-38 | Prueba de concepto |
| Formato de rutas, codificación y esquema de validación del XML de Rekordbox | ADR-006 | Prueba de importación |
| Costes de identificación de ADR-010 (órdenes de magnitud), en particular el nivel 1b | ADR-010, N-36 | Medición en la prueba de identificación |
| Licencia de la interfaz gráfica y del empaquetador | ADR-007, ADR-008 | Verificación de licencias |
| El dominio funciona en Python 3.10 (se ejecutó en 3.12) | `src/setlistgen/README.md`, OD-08 | Ejecutar en 3.10 y fijar la versión mínima |
| El Python de Windows y macOS incluye SQLite 3.37 o superior | `persistence/README.md`, N-04 | Probar en ambos sistemas |
| `WAL` y la copia de seguridad con la API de copia son compatibles con el flujo de ADR-004 | `persistence/README.md` | Diseño de infraestructura |
| Normativa de la UAH sobre propiedad intelectual de los TFG | ADR-007 | Lectura de la normativa |
| Correspondencia entre issues de GitHub y casos de uso | Matriz, sección 8 | Revisión del tablero |

---

# 7. Estado de la memoria

Ruta de trabajo: `docs/memory/Book/`.

| Capítulo o sección | Estado | Actualización necesaria |
|---|---|---|
| 1 Introducción | Redactado | Coherente con la línea base |
| 2 Estado del arte | Redactado | Sin cambios |
| 3 Fundamentos teóricos | Redactado | Sin cambios |
| 4.1.3 Gestión de requisitos | Redactado | Actualizar recuentos (36 RF y 27 RNF) (N-27) |
| 4.2.1 Control de versiones | Redactado | `main` contiene línea base provisional; etiquetas (N-56) |
| 4.4 Seguimiento y desviaciones | Redactado | Registrar N-16, N-56 y las ampliaciones de requisitos |
| 4.5 Gestión de riesgos | Redactado | Añadir R-11 a R-14 |
| 4.6 Gestión de decisiones | Redactado | Sustituir «todas abiertas» por el estado de los diez ADR |
| 5 Análisis de requisitos | Sin redactar | Se alimenta del SRS, los casos de uso y la matriz |
| 6.2 y 6.3 Dominio y datos | Sin redactar | **Material disponible** en la serie de datos; bloque reutilizable al final de cada documento. Esperar a congelar |
| 6.4 a 6.7, 7 a 9 y apéndices | Sin redactar | Se alimentan de los ADR (sección «Impacto en la memoria» de cada uno) |

---

# 8. Dependencias de diseño

## 8.1 Qué condiciona el modelo de dominio y de datos

Cumplido de forma provisional en `domain-model.md` v0.2 y en el esquema v0.1.1. Lo que sigue condicionando el **cierre**:

| Elemento | Origen |
|---|---|
| Identidad de pista, ubicaciones y huellas | OD-03, ADR-010 |
| Resultados por motor y versión | OD-04 |
| Existencia de `Library` | OD-05 |
| Instantánea de transiciones y de entradas del setlist | OD-06 |
| Conjunto de entidades y nombres | OD-07 |
| Reducción previa por género, duración de las candidatas y fallos en las métricas | N-48, N-51, N-52 |

## 8.2 Decisiones abiertas que condicionan el cierre

El detalle, el supuesto aplicado y el coste de cambio están en `open-decisions.md` v3.2.

| ID | Decisión | Prioridad | ¿Bloquea congelar el modelo? | Estado |
|---|---|---|---|---|
| OD-01 | RF-29 como Must | Alta | No | Supuesto aplicado |
| OD-02 | Salto máximo de BPM | Alta | No | Supuesto aplicado |
| OD-03 | Identificación permanente | Crítica | **Sí** | Supuesto aplicado |
| OD-04 | Resultados de varios motores | Crítica | **Sí** | Supuesto aplicado |
| OD-05 | Entidad `Library` | Alta | **Sí** | Supuesto aplicado; migración 2 preparada |
| OD-06 | Persistencia de transiciones | Crítica | **Sí** | Instantánea adoptada por el autor, sin validar |
| OD-07 | Conjunto de entidades de dominio | Crítica | **Sí** | Supuesto aplicado |
| OD-08 | ADR-007 a ADR-010 y estructura del repositorio | Media | No | Pendiente |
| OD-09 | Motor MIR definitivo | Media | No | Condicionada a la prueba de concepto |
| OD-10 | Protocolo de evaluación final | Media | No | Supuesto aplicado |

**Ninguna decisión ha sido validada todavía por tutor y cotutor.**

---

# 9. Próximas acciones

| Prioridad | Acción | Hallazgos | Responsable |
|---|---|---|---|
| 1 | **Corregir el README raíz** antes de la reunión: objetivos de la memoria 1.3.2, estado, estructura `src/` y enlaces | N-47 | Autor |
| 2 | Integrar los documentos corregidos: `er-model.md` 0.1.2, `database-schema.md` 0.1.1, `data-model.md` 1.0.1 y README de arquitectura 3.0.1 | N-54, N-55 | Autor |
| 3 | Etiquetar el estado actual de `main` como línea base provisional | N-56, C-06 | Autor |
| 4 | Reunión con tutor y cotutor: `open-decisions.md` v3.2, en el orden de la sección 2.1 | OD-01 a OD-10, DD-xx | Autor |
| 5 | Registrar los resultados y crear `meeting-notes.md` | N-58 | Autor |
| 6 | Tras la reunión, actualizar glosario, SRS 7, ADR-002, ADR-004, ADR-005 y ADR-008 | N-32, N-48, N-49, N-57 | Autor |
| 7 | Añadir a la matriz las ocho pruebas de N-50 y convertir las pruebas de humo del dominio en `pytest` | N-50 | Autor |
| 8 | Prueba de concepto: identificación (N-36), análisis, importación en Rekordbox, interfaz y empaquetado | N-03, N-04, N-38 | Autor |
| 9 | Actualizar la memoria (sección 7) | N-27 | Autor |
| 10 | Guardar el script de comprobación documental en `scripts/`, ampliado con la comprobación MER ↔ DDL | — | Autor |
| 11 | Revisar la normativa general y el resto de la específica de la EPS (formato, plazos y depósito) antes de redactar | — | Autor |
| 12 | Congelar la línea base y el modelo de datos con los resultados de la reunión | R-13 | Autor |

---

# 10. Veredicto

| Cuestión | Respuesta |
|---|---|
| ¿Está cerrado el diseño detallado? | **Sí, de forma provisional.** Dominio, conceptual, MER y esquema son coherentes entre sí tras las correcciones de esta auditoría |
| ¿Quedan contradicciones graves entre la línea base y el diseño? | **No graves.** La única de gravedad Alta nueva es documental (N-47, README raíz). Hay discrepancias medias que piden decisión (N-48, N-51, N-52) |
| ¿Hay huecos de trazabilidad? | **Sí, acotados** (N-50): ocho pruebas sin caso en la matriz. Cada RF y RNF sigue teniendo al menos una |
| ¿Está validada la línea base por los tutores? | **No** |
| ¿Se ha verificado con datos reales? | **No.** La prueba de concepto está pendiente; la prueba del DDL se hizo en memoria |
| ¿Puede celebrarse la reunión? | **Sí**, preferiblemente tras corregir N-47 |
| ¿Puede congelarse el modelo de datos? | **No** hasta validar OD-03 a OD-07 |
| ¿Puede empezar la implementación? | Solo la de las capas independientes de las decisiones abiertas; el dominio y la persistencia esperan al cierre |

El siguiente paso es la **reunión con tutor y cotutor**, y después congelar la línea base y actualizar la memoria.

---

# 11. Control de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-10 | Auditoría técnica inicial |
| 2.0 | 2026-11-04 | Actualización tras la consolidación documental |
| 3.0 | 2026-11-05 | Reescritura completa: estado de madurez, línea base, segunda auditoría, hallazgos, riesgos, hipótesis, memoria, dependencias y veredicto |
| 3.1 | 2026-11-06 | Revisión de la 3.0 contra la línea base; resumen de decisiones abiertas |
| 3.2 | 2026-11-14 | Auditoría cruzada previa a la reunión con tutores. Diseño detallado y estructura `src/` incorporados. Hallazgos N-31 a N-59, M-01 a M-07 y C-01 a C-08 registrados; resueltos N-25, N-26, N-31, N-33, N-35, N-41, N-45, N-46, N-23, N-54, N-55 y H-35. Nuevo hallazgo Alto N-47. Riesgo R-14 propuesto. Correcciones a `er-model.md`, `database-schema.md`, `data-model.md` y al README de arquitectura |
