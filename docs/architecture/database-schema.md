# Esquema de Base de Datos de SetlistGen: modelo relacional y diseño físico SQLite

> Destino en el repositorio: `docs/architecture/database-schema.md`. El DDL es `database/schema/schema.sql`. Pasos 5 y 6 del plan. Parte de `er-model.md` v0.1.

**Versión:** 0.1 (provisional) · **Fecha:** 2026-11-12 · **Estado:** pendiente de validación por tutor y cotutor

> Es el esquema inicial de la **migración 1**. Se aplica con el supuesto de OD-03, OD-04 y OD-06 y sin la entidad `Library` (OD-05). Cada cambio posterior será una migración versionada (RNF-27), por lo que el riesgo R-13 queda acotado.

# 1. Resolución de M-01 a M-07

| ID | Decisión | Aplicación |
|---|---|---|
| M-01 | Unicidad parcial de la ruta | Índice único sobre `path_normalized` para ubicaciones **vigentes** (`active` y `failed`). Ver ajuste abajo |
| M-02, M-03, M-04 | Aprobados | Tabla `request_harmonic_move`; el informe de importación no se persiste; trazabilidad por pista en el manifiesto de ADR-009 |
| M-05 | `'unknown'` en lugar de nulo | `reference_measurement.rekordbox_version NOT NULL DEFAULT 'unknown'` |
| M-06 | `camelot_code` persistido | **Columna generada y almacenada** (`GENERATED ALWAYS ... STORED`). Ver ajuste abajo |
| M-07 | `APP_SETTING` en la base | Tabla de fila única (`settings_id = 1`) |

**Ajuste a M-01.** Tu enunciado permitía dos redacciones y el SQL de ejemplo (`WHERE status NOT IN ('moved')`) no coincide con la primera. Adopto la primera, "ni `moved` ni `absent`", que equivale a `status IN ('active','failed')`. Con la segunda, el flujo CU-02 A3 se rompería: cuando el audio de una ruta cambia, la pista antigua queda `absent` en esa ruta y la nueva queda `active` en la misma. Una ubicación `failed` también es vigente: el fichero existe pero no se pudo leer, así que no puede compartir ruta con otra `active`.

**Ajuste a M-06.** En lugar de una columna ordinaria que la aplicación debe mantener, `camelot_code` es una columna generada y almacenada: ocupa espacio y se indexa igual, pero no puede divergir de `key_tonic` y `key_mode`. Se comprobó que coincide con `MusicalKey.to_camelot()` del dominio en las 24 tonalidades. Si se prefiere una columna ordinaria, basta con quitar la cláusula `GENERATED`.

**Decisión mía: `Library` queda fuera de la migración 1.** OD-05 no está validada. La migración 2 condicional (sección 7) la añade sin reconstruir tablas.

# 2. Modelo relacional (paso 5)

Notación: **clave primaria** en negrita, `*` marca clave foránea, `UK` clave candidata. Las flechas indican la tabla referenciada.

## 2.1 Esquemas de relación

```text
ANALYSIS_ENGINE( **engine_id**, name, version )                              UK(name, version)
APP_SETTING( **settings_id**, active_engine_id* → ANALYSIS_ENGINE )          settings_id = 1

TRACK( **track_id** )
TRACK_METADATA( **track_id***→TRACK, title, artist, genre, year, duration_s, tag_bpm, tag_key_tonic, tag_key_mode )
TRACK_LOCATION( **location_id**, track_id*→TRACK, path, path_normalized, size_bytes, modified_at,
                last_seen_at, status, failure_cause )                         UK(track_id, path_normalized)
TRACK_FINGERPRINT( **track_id***→TRACK, **kind**, **algorithm_version**, digest )

ANALYSIS_RESULT( **result_id**, track_id*→TRACK, engine_id*→ANALYSIS_ENGINE, analyzed_at, bpm, bpm_failure_cause,
                 key_tonic, key_mode, key_failure_cause, confidence, camelot_code )   UK(track_id, engine_id)

SETLIST( **setlist_id**, created_at, optimality, edited )
GENERATION_REQUEST( **setlist_id***→SETLIST, engine_id*→ANALYSIS_ENGINE, target_duration_s, bpm_min, bpm_max,
                    max_bpm_jump, duration_tolerance, weight_alpha, weight_beta, weight_gamma, seed,
                    algorithm_version, node_limit, time_limit_s )
REQUEST_HARMONIC_MOVE( **setlist_id***→GENERATION_REQUEST, **step**, **switches_mode** )
ALLOWED_KEY( **setlist_id***→GENERATION_REQUEST, **camelot_code** )
GENRE_SEGMENT( **setlist_id***→GENERATION_REQUEST, **segment_order**, start_s, end_s, genre )
ANCHOR( **setlist_id***→GENERATION_REQUEST, **position**, track_id*→TRACK )     UK(setlist_id, track_id)
SETLIST_TRACK( **setlist_id***→SETLIST, **position**, track_id*→TRACK, bpm, camelot_code, duration_s, genre,
               original_position )                                            UK(setlist_id, track_id)
TRANSITION( **setlist_id**, **from_position**, bpm_delta, camelot_distance, harmonically_compatible,
            genre_incoherence, cost )          FK(setlist_id, from_position) → SETLIST_TRACK(setlist_id, position)

REFERENCE_MEASUREMENT( **reference_id**, track_id*→TRACK, source, rekordbox_version, bpm, key_tonic, key_mode )
                                                                              UK(track_id, source, rekordbox_version)
EVALUATION_REPORT( **report_id**, engine_id*→ANALYSIS_ENGINE, reference_source, created_at, scope_label,
                   bpm_total, bpm_strict_hits, bpm_octave_hits, key_total, key_exact_hits, key_camelot_hits,
                   bpm_failures, key_failures )
EVALUATION_ERROR_COUNT( **report_id***→EVALUATION_REPORT, **descriptor**, **error_kind**, error_count )
EVALUATION_EXCLUSION( **report_id***→EVALUATION_REPORT, **exclusion_order**, kind, track_id*→TRACK, path,
                      ref_bpm, ref_key_tonic, ref_key_mode )

SCHEMA_MIGRATION( **version**, description, applied_at )                      (técnica, sin entidad de dominio)
```

## 2.2 Reglas de borrado

| Relación | Regla | Motivo |
|---|---|---|
| Hijas de `TRACK` (metadatos, ubicaciones, huellas) | CASCADE | Composición del agregado Catálogo |
| `SETLIST` → solicitud, entradas, transiciones; solicitud → hijas | CASCADE | Composición del agregado Generación |
| `EVALUATION_REPORT` → errores, exclusiones | CASCADE | Composición del agregado Evaluación |
| Referencias a `TRACK` desde otros agregados | RESTRICT | Una pista nunca se borra, se marca ausente (RF-09c) |
| Referencias a `ANALYSIS_ENGINE` | RESTRICT | Un motor con resultados no se elimina |
| `APP_SETTING.active_engine_id` | SET NULL | La configuración no debe bloquear |

## 2.3 Formas normales

Todas las relaciones están en **BCNF** salvo dos dependencias derivadas, introducidas a propósito:

| Relación | Dependencia | Tratamiento |
|---|---|---|
| `TRACK_LOCATION` | `path → path_normalized` (atributo no clave que depende de otro no clave: viola 3FN) | Almacenado para poder indexar la búsqueda por ruta (RNF-04). Lo calcula el repositorio con `normalize_path` y la columna no se actualiza de forma independiente |
| `ANALYSIS_RESULT` | `(key_tonic, key_mode) → camelot_code` | Columna generada: el motor de la base la mantiene, sin anomalía de modificación |

Otras redundancias son **instantáneas aceptadas** (OD-06 y CM-06), no dependencias dentro de una relación: `SETLIST_TRACK` copia valores que cambiarán en `TRACK_METADATA`; `TRANSITION` guarda un cálculo de dos entradas; `EVALUATION_REPORT` guarda agregados. Son deliberadas: el histórico no debe cambiar al editar etiquetas ni al reanalizar.

# 3. Diseño físico (paso 6)

## 3.1 Supuestos

| Aspecto | Decisión |
|---|---|
| Versión mínima | SQLite **3.37** (tablas `STRICT`). La comprobación en arranque `sqlite3.sqlite_version_info >= (3, 37, 0)` debe estar en el punto de entrada. La versión que incluye Python varía por sistema (ADR-008, R-11) |
| Tipado | `STRICT`: TEXT, INTEGER y REAL. Sin `BLOB` en esta migración |
| UUID | TEXT de 36 caracteres en minúsculas con guiones, con `CHECK (length(...) = 36)` en las claves primarias |
| Enums | TEXT con `CHECK (col IN (...))`, valor `Enum.value` del dominio |
| Booleanos | INTEGER 0/1 con `CHECK` |
| Fechas | TEXT ISO 8601 en UTC (`2026-11-12T10:00:00.000000Z`) |
| Rutas | TEXT Unicode, sin conversión (RNF-16) |
| `WITHOUT ROWID` | En tablas hijas pequeñas con clave compuesta |

PRAGMAs por conexión (no se guardan en el fichero, salvo el modo de diario):

```sql
PRAGMA foreign_keys = ON;      -- obligatorio: SQLite no aplica claves foráneas por defecto
PRAGMA journal_mode = WAL;     -- se mantiene en el fichero; lecturas concurrentes con un escritor
PRAGMA synchronous = NORMAL;   -- compromiso habitual con WAL; la atomicidad (RNF-17) se mantiene
```

`journal_mode = WAL` es una propuesta: genera ficheros auxiliares `-wal` y `-shm` junto a la base, lo que afecta a la copia de seguridad "copiar un fichero" de ADR-004. Se decide con el diseño de infraestructura; el esquema no depende de ello.

## 3.2 Script DDL

El script completo está en `schema.sql`. Se reproduce aquí para la memoria.

```sql
-- =====================================================================================
-- SetlistGen · esquema inicial de SQLite (migración 1)          Versión del documento: 0.1
-- Requiere SQLite >= 3.37 (tablas STRICT). Columnas generadas: >= 3.31. Índices parciales: >= 3.8.
-- Convenciones: UUID = TEXT (36 caracteres, minúsculas, con guiones). Enum = TEXT con CHECK.
--               Booleano = INTEGER 0/1. Fechas = TEXT ISO 8601 en UTC. Rutas = TEXT Unicode.
-- Cada conexión debe ejecutar antes:  PRAGMA foreign_keys = ON;  (no persiste en el fichero)
-- Provisional hasta validar OD-03 a OD-07 (R-13). OD-05 (Library) queda fuera: ver migración 2 condicional.
-- =====================================================================================

BEGIN;

-- ---------- Configuración y trazabilidad del esquema ----------------------------------

CREATE TABLE schema_migration (
    version     INTEGER PRIMARY KEY CHECK (version > 0),
    description TEXT    NOT NULL CHECK (length(trim(description)) > 0),
    applied_at  TEXT    NOT NULL
) STRICT;

CREATE TABLE analysis_engine (
    engine_id TEXT PRIMARY KEY CHECK (length(engine_id) = 36),
    name      TEXT NOT NULL CHECK (length(trim(name)) > 0),
    version   TEXT NOT NULL CHECK (length(trim(version)) > 0),
    UNIQUE (name, version)
) STRICT;

CREATE TABLE app_setting (
    settings_id      INTEGER PRIMARY KEY CHECK (settings_id = 1),  -- fila única
    active_engine_id TEXT REFERENCES analysis_engine (engine_id) ON DELETE SET NULL
) STRICT;

-- ---------- Agregado Catálogo ----------------------------------------------------------

CREATE TABLE track (
    track_id TEXT PRIMARY KEY CHECK (length(track_id) = 36)
) STRICT;

CREATE TABLE track_metadata (
    track_id      TEXT PRIMARY KEY REFERENCES track (track_id) ON DELETE CASCADE,
    title         TEXT,
    artist        TEXT,
    genre         TEXT,
    year          INTEGER CHECK (year IS NULL OR year > 0),
    duration_s    REAL    CHECK (duration_s IS NULL OR duration_s > 0),
    tag_bpm       REAL    CHECK (tag_bpm IS NULL OR tag_bpm > 0),
    tag_key_tonic INTEGER CHECK (tag_key_tonic IS NULL OR tag_key_tonic BETWEEN 0 AND 11),
    tag_key_mode  TEXT    CHECK (tag_key_mode IS NULL OR tag_key_mode IN ('A', 'B')),
    CHECK ((tag_key_tonic IS NULL) = (tag_key_mode IS NULL))
) STRICT;

CREATE TABLE track_location (
    location_id     TEXT PRIMARY KEY CHECK (length(location_id) = 36),
    track_id        TEXT    NOT NULL REFERENCES track (track_id) ON DELETE CASCADE,
    path            TEXT    NOT NULL CHECK (length(trim(path)) > 0),
    path_normalized TEXT    NOT NULL CHECK (length(path_normalized) > 0),  -- derivado de path (normalize_path)
    size_bytes      INTEGER NOT NULL CHECK (size_bytes >= 0),
    modified_at     TEXT    NOT NULL,
    last_seen_at    TEXT    NOT NULL,
    status          TEXT    NOT NULL CHECK (status IN ('active', 'absent', 'moved', 'failed')),
    failure_cause   TEXT    CHECK (failure_cause IS NULL OR length(trim(failure_cause)) > 0),
    CHECK ((status = 'failed') = (failure_cause IS NOT NULL)),            -- IN-15
    UNIQUE (track_id, path_normalized)                                    -- IN-05
) STRICT;

CREATE TABLE track_fingerprint (
    track_id          TEXT NOT NULL REFERENCES track (track_id) ON DELETE CASCADE,
    kind              TEXT NOT NULL CHECK (kind IN ('quick', 'content')),
    algorithm_version TEXT NOT NULL CHECK (length(trim(algorithm_version)) > 0),
    digest            TEXT NOT NULL CHECK (length(digest) > 0),
    PRIMARY KEY (track_id, kind, algorithm_version)                       -- IN-07
) STRICT, WITHOUT ROWID;

-- ---------- Agregado Análisis ----------------------------------------------------------

CREATE TABLE analysis_result (
    result_id         TEXT PRIMARY KEY CHECK (length(result_id) = 36),
    track_id          TEXT NOT NULL REFERENCES track (track_id)           ON DELETE RESTRICT,
    engine_id         TEXT NOT NULL REFERENCES analysis_engine (engine_id) ON DELETE RESTRICT,
    analyzed_at       TEXT NOT NULL,
    bpm               REAL    CHECK (bpm IS NULL OR bpm > 0),
    bpm_failure_cause TEXT    CHECK (bpm_failure_cause IS NULL OR length(trim(bpm_failure_cause)) > 0),
    key_tonic         INTEGER CHECK (key_tonic IS NULL OR key_tonic BETWEEN 0 AND 11),
    key_mode          TEXT    CHECK (key_mode IS NULL OR key_mode IN ('A', 'B')),
    key_failure_cause TEXT    CHECK (key_failure_cause IS NULL OR length(trim(key_failure_cause)) > 0),
    confidence        REAL    CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1),
    -- Código Camelot derivado de la tonalidad (RF-06). Persistido y siempre coherente con key_tonic/key_mode.
    camelot_code      TEXT GENERATED ALWAYS AS (
        CASE WHEN key_tonic IS NULL THEN NULL
             ELSE (((7 * (CASE key_mode WHEN 'B' THEN key_tonic ELSE (key_tonic + 3) % 12 END)) % 12 + 7) % 12 + 1)
                  || key_mode
        END
    ) STORED,
    CHECK ((bpm IS NULL) <> (bpm_failure_cause IS NULL)),                  -- IN-04: valor o fallo
    CHECK ((key_tonic IS NULL) = (key_mode IS NULL)),
    CHECK ((key_tonic IS NULL) <> (key_failure_cause IS NULL)),
    UNIQUE (track_id, engine_id)                                          -- IN-08
) STRICT;

-- ---------- Agregado Generación --------------------------------------------------------

CREATE TABLE setlist (
    setlist_id TEXT PRIMARY KEY CHECK (length(setlist_id) = 36),
    created_at TEXT    NOT NULL,
    optimality TEXT    NOT NULL CHECK (optimality IN ('proven', 'not_proven')),
    edited     INTEGER NOT NULL CHECK (edited IN (0, 1))
) STRICT;

CREATE TABLE generation_request (
    setlist_id         TEXT PRIMARY KEY REFERENCES setlist (setlist_id) ON DELETE CASCADE,
    engine_id          TEXT    NOT NULL REFERENCES analysis_engine (engine_id) ON DELETE RESTRICT,
    target_duration_s  REAL    NOT NULL CHECK (target_duration_s > 0),
    bpm_min            REAL    NOT NULL CHECK (bpm_min > 0),
    bpm_max            REAL    NOT NULL,
    max_bpm_jump       REAL    NOT NULL CHECK (max_bpm_jump >= 0),
    duration_tolerance REAL    NOT NULL CHECK (duration_tolerance >= 0 AND duration_tolerance < 1),
    weight_alpha       REAL    NOT NULL CHECK (weight_alpha >= 0),
    weight_beta        REAL    NOT NULL CHECK (weight_beta >= 0),
    weight_gamma       REAL    NOT NULL CHECK (weight_gamma >= 0),
    seed               INTEGER NOT NULL,
    algorithm_version  TEXT    NOT NULL CHECK (length(trim(algorithm_version)) > 0),
    node_limit         INTEGER NOT NULL CHECK (node_limit > 0),
    time_limit_s       REAL    CHECK (time_limit_s IS NULL OR time_limit_s > 0),
    CHECK (bpm_max >= bpm_min)
) STRICT;

CREATE TABLE request_harmonic_move (
    setlist_id    TEXT    NOT NULL REFERENCES generation_request (setlist_id) ON DELETE CASCADE,
    step          INTEGER NOT NULL CHECK (step BETWEEN -5 AND 6),
    switches_mode INTEGER NOT NULL CHECK (switches_mode IN (0, 1)),
    PRIMARY KEY (setlist_id, step, switches_mode)
) STRICT, WITHOUT ROWID;

CREATE TABLE allowed_key (
    setlist_id   TEXT NOT NULL REFERENCES generation_request (setlist_id) ON DELETE CASCADE,
    camelot_code TEXT NOT NULL CHECK (camelot_code GLOB '[1-9][AB]' OR camelot_code GLOB '1[0-2][AB]'),
    PRIMARY KEY (setlist_id, camelot_code)
) STRICT, WITHOUT ROWID;

CREATE TABLE genre_segment (
    setlist_id    TEXT    NOT NULL REFERENCES generation_request (setlist_id) ON DELETE CASCADE,
    segment_order INTEGER NOT NULL CHECK (segment_order >= 0),
    start_s       REAL    NOT NULL CHECK (start_s >= 0),
    end_s         REAL    NOT NULL,
    genre         TEXT    NOT NULL CHECK (length(trim(genre)) > 0),
    PRIMARY KEY (setlist_id, segment_order),
    CHECK (end_s > start_s)
) STRICT, WITHOUT ROWID;

CREATE TABLE anchor (
    setlist_id TEXT    NOT NULL REFERENCES generation_request (setlist_id) ON DELETE CASCADE,
    position   INTEGER NOT NULL CHECK (position >= 0),
    track_id   TEXT    NOT NULL REFERENCES track (track_id) ON DELETE RESTRICT,
    PRIMARY KEY (setlist_id, position),
    UNIQUE (setlist_id, track_id)                                         -- una pista, un ancla
) STRICT, WITHOUT ROWID;

-- Instantánea de los descriptores en el momento de generar [SUPUESTO · OD-06]
CREATE TABLE setlist_track (
    setlist_id        TEXT    NOT NULL REFERENCES setlist (setlist_id) ON DELETE CASCADE,
    position          INTEGER NOT NULL CHECK (position >= 0),
    track_id          TEXT    NOT NULL REFERENCES track (track_id) ON DELETE RESTRICT,
    bpm               REAL    NOT NULL CHECK (bpm > 0),
    camelot_code      TEXT    NOT NULL CHECK (camelot_code GLOB '[1-9][AB]' OR camelot_code GLOB '1[0-2][AB]'),
    duration_s        REAL    NOT NULL CHECK (duration_s > 0),
    genre             TEXT,
    original_position INTEGER CHECK (original_position IS NULL OR original_position >= 0),
    PRIMARY KEY (setlist_id, position),
    UNIQUE (setlist_id, track_id)                                         -- RF-18
) STRICT, WITHOUT ROWID;

-- Origen = from_position; destino = from_position + 1 (no se guardan)
CREATE TABLE transition (
    setlist_id              TEXT    NOT NULL,
    from_position           INTEGER NOT NULL,
    bpm_delta               REAL    NOT NULL CHECK (bpm_delta >= 0),
    camelot_distance        INTEGER NOT NULL CHECK (camelot_distance BETWEEN 0 AND 6),
    harmonically_compatible INTEGER NOT NULL CHECK (harmonically_compatible IN (0, 1)),
    genre_incoherence       REAL    NOT NULL CHECK (genre_incoherence >= 0),
    cost                    REAL    NOT NULL CHECK (cost >= 0),
    PRIMARY KEY (setlist_id, from_position),
    FOREIGN KEY (setlist_id, from_position) REFERENCES setlist_track (setlist_id, position) ON DELETE CASCADE
) STRICT, WITHOUT ROWID;

-- ---------- Agregado Evaluación --------------------------------------------------------

-- rekordbox_version = 'unknown' cuando no se conoce (el dominio la representa con None)
CREATE TABLE reference_measurement (
    reference_id      TEXT PRIMARY KEY CHECK (length(reference_id) = 36),
    track_id          TEXT NOT NULL REFERENCES track (track_id) ON DELETE RESTRICT,
    source            TEXT NOT NULL CHECK (source IN ('rekordbox_xml', 'csv')),
    rekordbox_version TEXT NOT NULL DEFAULT 'unknown' CHECK (length(trim(rekordbox_version)) > 0),
    bpm               REAL    CHECK (bpm IS NULL OR bpm > 0),
    key_tonic         INTEGER CHECK (key_tonic IS NULL OR key_tonic BETWEEN 0 AND 11),
    key_mode          TEXT    CHECK (key_mode IS NULL OR key_mode IN ('A', 'B')),
    CHECK ((key_tonic IS NULL) = (key_mode IS NULL)),
    CHECK (bpm IS NOT NULL OR key_tonic IS NOT NULL),
    UNIQUE (track_id, source, rekordbox_version)
) STRICT;

CREATE TABLE evaluation_report (
    report_id         TEXT PRIMARY KEY CHECK (length(report_id) = 36),
    engine_id         TEXT NOT NULL REFERENCES analysis_engine (engine_id) ON DELETE RESTRICT,
    reference_source  TEXT NOT NULL CHECK (reference_source IN ('rekordbox_xml', 'csv')),
    created_at        TEXT NOT NULL,
    scope_label       TEXT NOT NULL CHECK (length(trim(scope_label)) > 0),
    bpm_total         INTEGER NOT NULL CHECK (bpm_total > 0),             -- incluye fallos (D-11)
    bpm_strict_hits   INTEGER NOT NULL CHECK (bpm_strict_hits >= 0),
    bpm_octave_hits   INTEGER NOT NULL,
    key_total         INTEGER CHECK (key_total IS NULL OR key_total > 0),
    key_exact_hits    INTEGER CHECK (key_exact_hits IS NULL OR key_exact_hits >= 0),
    key_camelot_hits  INTEGER,
    bpm_failures      INTEGER NOT NULL CHECK (bpm_failures >= 0),
    key_failures      INTEGER NOT NULL CHECK (key_failures >= 0),
    CHECK (bpm_strict_hits <= bpm_octave_hits AND bpm_octave_hits <= bpm_total),
    CHECK (bpm_failures <= bpm_total - bpm_strict_hits),
    CHECK ((key_total IS NULL) = (key_exact_hits IS NULL) AND (key_total IS NULL) = (key_camelot_hits IS NULL)),
    CHECK (key_total IS NULL OR (key_exact_hits <= key_camelot_hits AND key_camelot_hits <= key_total)),
    CHECK (key_total IS NULL OR key_failures <= key_total - key_exact_hits),
    CHECK (key_total IS NOT NULL OR key_failures = 0)
) STRICT;

CREATE TABLE evaluation_error_count (
    report_id   TEXT    NOT NULL REFERENCES evaluation_report (report_id) ON DELETE CASCADE,
    descriptor  TEXT    NOT NULL CHECK (descriptor IN ('bpm', 'key')),
    error_kind  TEXT    NOT NULL,
    error_count INTEGER NOT NULL CHECK (error_count >= 0),
    PRIMARY KEY (report_id, descriptor, error_kind),
    CHECK ((descriptor = 'bpm' AND error_kind IN ('octave', 'other'))
        OR (descriptor = 'key' AND error_kind IN ('relative', 'fifth', 'parallel', 'other')))
) STRICT, WITHOUT ROWID;

CREATE TABLE evaluation_exclusion (
    report_id       TEXT    NOT NULL REFERENCES evaluation_report (report_id) ON DELETE CASCADE,
    exclusion_order INTEGER NOT NULL CHECK (exclusion_order >= 0),
    kind            TEXT    NOT NULL CHECK (kind IN ('not_analyzed', 'track_without_reference',
                                                     'reference_without_track', 'ambiguous_reference')),
    track_id        TEXT    REFERENCES track (track_id) ON DELETE RESTRICT,
    path            TEXT,
    ref_bpm         REAL    CHECK (ref_bpm IS NULL OR ref_bpm > 0),
    ref_key_tonic   INTEGER CHECK (ref_key_tonic IS NULL OR ref_key_tonic BETWEEN 0 AND 11),
    ref_key_mode    TEXT    CHECK (ref_key_mode IS NULL OR ref_key_mode IN ('A', 'B')),
    PRIMARY KEY (report_id, exclusion_order),
    CHECK ((ref_key_tonic IS NULL) = (ref_key_mode IS NULL)),
    CHECK (
        (kind IN ('not_analyzed', 'track_without_reference')
            AND track_id IS NOT NULL AND path IS NULL
            AND ref_bpm IS NULL AND ref_key_tonic IS NULL)
     OR (kind IN ('reference_without_track', 'ambiguous_reference')
            AND track_id IS NULL AND path IS NOT NULL AND length(trim(path)) > 0)
    )
) STRICT;

-- ---------- Índices ---------------------------------------------------------------------

-- M-01: una ruta normalizada solo puede tener una ubicación vigente (active o failed).
-- absent y moved son históricas y pueden coexistir con la vigente de otra pista (CU-02 A3, ADR-010).
CREATE UNIQUE INDEX ux_track_location_current_path
    ON track_location (path_normalized) WHERE status IN ('active', 'failed');

-- Reconocimiento por ruta (nivel 1a, RNF-04): incluye ubicaciones históricas.
CREATE INDEX ix_track_location_path ON track_location (path_normalized);
-- Disponibilidad de una pista (candidatas, CU-05 paso 5).
CREATE INDEX ix_track_location_track_status ON track_location (track_id, status);

-- Reconocimiento por huella (nivel 1b y 2, RNF-04).
CREATE INDEX ix_fingerprint_lookup ON track_fingerprint (kind, algorithm_version, digest);

-- Consultas y ordenación de la biblioteca (RF-11, RF-11b).
CREATE INDEX ix_track_metadata_title    ON track_metadata (title);
CREATE INDEX ix_track_metadata_genre    ON track_metadata (genre);
CREATE INDEX ix_track_metadata_year     ON track_metadata (year);
CREATE INDEX ix_track_metadata_duration ON track_metadata (duration_s);

-- Candidatas del motor activo por BPM y por tonalidad (RF-11, RNF-03). UNIQUE(track_id, engine_id) cubre la pista.
CREATE INDEX ix_analysis_result_engine_bpm   ON analysis_result (engine_id, bpm) WHERE bpm IS NOT NULL;
CREATE INDEX ix_analysis_result_engine_camelot ON analysis_result (engine_id, camelot_code) WHERE camelot_code IS NOT NULL;

-- Historial y ranking de uso (RF-24, RF-25) y comprobación de claves foráneas con RESTRICT.
CREATE INDEX ix_setlist_created_at         ON setlist (created_at);
CREATE INDEX ix_setlist_track_track        ON setlist_track (track_id);
CREATE INDEX ix_anchor_track               ON anchor (track_id);
CREATE INDEX ix_generation_request_engine  ON generation_request (engine_id);
CREATE INDEX ix_evaluation_report_engine   ON evaluation_report (engine_id, created_at);
CREATE INDEX ix_evaluation_exclusion_track ON evaluation_exclusion (track_id) WHERE track_id IS NOT NULL;

-- ---------- Datos iniciales -------------------------------------------------------------

INSERT INTO app_setting (settings_id, active_engine_id) VALUES (1, NULL);
INSERT INTO schema_migration (version, description, applied_at)
VALUES (1, 'Esquema inicial', strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));

COMMIT;
```

# 4. Índices y rutas de acceso

| Índice | Sirve a | Consulta |
|---|---|---|
| `ux_track_location_current_path` (parcial, único) | M-01 | Una ruta, una ubicación vigente |
| `ix_track_location_path` | RNF-04, nivel 1a | `WHERE path_normalized = ?` (incluye históricas) |
| `ix_track_location_track_status` | CU-05 paso 5 | Disponibilidad de una pista |
| `ix_fingerprint_lookup` | RNF-04, nivel 1b y 2 | `WHERE kind, algorithm_version, digest` (índice de cobertura) |
| `ix_analysis_result_engine_bpm`, `..._camelot` | RF-11, RNF-03 | Candidatas del motor activo por BPM o tonalidad |
| `ix_track_metadata_*` | RF-11, RF-11b | Filtro y ordenación por título, género, año y duración |
| `ix_setlist_created_at`, `ix_setlist_track_track` | RF-24, RF-25 | Historial y ranking de uso |
| `ix_anchor_track`, `ix_generation_request_engine`, `ix_evaluation_*` | Claves foráneas con RESTRICT | Evitan escaneos al comprobar |

Observación de ordenación: la ordenación por título en SQLite distingue mayúsculas y no normaliza tildes por defecto. RF-11b puede requerir una `COLLATE` propia (registrada desde Python) o ordenar en memoria; se decide al implementar la consulta (N-42).

# 5. Verificación realizada

Se ejecutó `schema.sql` en SQLite 3.45.1 con una batería de pruebas de integridad. No sustituye a T-ARQ-06 ni a las pruebas de integración.

| Comprobación | Resultado |
|---|---|
| El script crea 20 tablas (19 del MER más `schema_migration`) | Correcto |
| `camelot_code` generado coincide con el dominio en las 24 tonalidades | Correcto |
| Rechazos: resultado sin BPM ni causa, BPM y causa a la vez, `failed` sin causa, causa con `active`, pista repetida en un setlist, código Camelot inválido, `bpm_min > bpm_max`, transición sin entrada de origen, métricas incoherentes, exclusión incoherente, segunda fila de `app_setting` | Correcto |
| M-01: `absent` y `active` coexisten en una ruta; dos `active` o `failed` + `active` se rechazan; `moved` se permite | Correcto |
| `UNIQUE (pista, motor)` y `UNIQUE` de referencia con `'unknown'` | Correcto |
| Borrar una pista referenciada falla; borrar un setlist elimina solicitud, entradas y transiciones | Correcto |
| `foreign_key_check` e `integrity_check` | Sin incidencias |
| Planes de consulta | Ruta, huella, BPM y Camelot usan sus índices; la huella se resuelve con índice de cobertura |
| Migración 2 condicional | Se aplica sobre la 1 sin incidencias |
| Prueba de carga: 5 000 pistas, 5 000 búsquedas por ruta y 5 000 por huella | 29 ms y 22 ms en memoria |

La última cifra mide solo el acceso a la base en memoria. **No verifica RNF-04**, cuyo coste dominante es leer ficheros (N-36), ni refleja un disco real.

# 6. Qué no puede imponer el esquema

| Invariante | Dónde queda |
|---|---|
| Una solicitud tiene siempre al menos un movimiento armónico | Dominio (IN-09) |
| Posiciones contiguas, n − 1 transiciones, segmentos sin solape y `original_position` solo con `edited` | Dominio (IN-10, IN-17) |
| Un setlist siempre tiene solicitud (1:1 obligatorio) | Repositorio: se inserta en la misma transacción |
| Errores clasificados + fallos = total − aciertos | Dominio (IN-16) |
| Normalización de `path_normalized` | Repositorio |

# 7. Migración 2 condicional (OD-05)

Solo si los tutores validan la entidad `Library`:

```sql
-- Migración 2 (CONDICIONAL: solo si se valida OD-05, entidad Library)
BEGIN;
CREATE TABLE library (
    library_id TEXT PRIMARY KEY CHECK (length(library_id) = 36),
    root_path  TEXT NOT NULL CHECK (length(trim(root_path)) > 0)
) STRICT;
ALTER TABLE track_location ADD COLUMN library_id TEXT REFERENCES library (library_id) ON DELETE SET NULL;
CREATE INDEX ix_track_location_library ON track_location (library_id) WHERE library_id IS NOT NULL;
INSERT INTO schema_migration (version, description, applied_at)
VALUES (2, 'Entidad Library (OD-05)', strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));
COMMIT;
```

# 8. Hallazgos nuevos

| ID | Gravedad | Problema | Propuesta |
|---|---|---|---|
| N-40 | Media | `modified_at` se compara por igualdad en `TrackRecognitionService` (nivel 1a). Un sistema de ficheros con resolución de nanosegundos o de dos segundos puede dar falsos "modificado" | Normalizar en el adaptador a una resolución fija (p. ej. microsegundos) antes de comparar y guardar |
| N-41 | Media | `path_normalized` ignora mayúsculas (`casefold`), lo que en sistemas sensibles puede unir rutas distintas y chocar con `ux_track_location_current_path` | Confirmar en la prueba de importación (R-02, N-37) |
| N-42 | Baja | Orden por título sin tratar tildes ni mayúsculas | Decidir `COLLATE` propia al implementar RF-11b |
| N-43 | Baja | El dominio usa `datetime` sin zona horaria; el esquema espera UTC | Exigir `datetime` con zona UTC en el repositorio |
| N-44 | Baja | `ix_analysis_result_engine_bpm` y `..._camelot` se crearon sin medir su utilidad real | Revisar tras el benchmark de RNF-03 |
| N-45 | Media | El recuento de tablas del MER decía dieciocho y son diecinueve | Corregido en `er-model.md` |
| N-46 | Media | ADR-004 y `database/README.md` citan `data-model.md` como entregable único | Ver "Actualización documental" |

# 9. Impacto y siguiente paso

- **Documentación:** registrar M-01 a M-07 como resueltos y N-40 a N-46 en `audit-review.md`. ADR-004 y `database/README.md` deben remitir a la serie `domain-model`, `conceptual-model`, `er-model` y `database-schema`; se propone que `data-model.md` quede como índice de esos cuatro documentos. Revisar ADR-002 por `AnalysisResultRepository`.
- **Estado de la persistencia:** el esquema es ejecutable, pero **no queda cerrada** hasta que los tutores validen OD-03 a OD-07 (ADR-004). Hasta entonces es la migración 1 provisional.
- **Siguiente fase:** con el esquema, el siguiente hito es el diseño de los repositorios (puertos y adaptadores SQLite) y de la prueba de concepto de identificación, que mide el coste real del nivel 1b (N-36). La implementación no debería empezar antes de reorganizar el repositorio (N-25).

Guardar este contenido para la memoria del TFG (capítulo 6, sección 6.3, y capítulo 7, sección 7.5):

- **Contexto:** el modelo lógico debía convertirse en un esquema SQLite verificable y con migraciones.
- **Problema:** imponer en la base la mayor parte de los invariantes del dominio.
- **Alternativas:** columna ordinaria o generada para el código Camelot; unicidad total o parcial de la ruta.
- **Solución adoptada:** tablas `STRICT` con `CHECK`, índice único parcial y columna generada.
- **Justificación:** los invariantes se comprueban en la base y no solo en el código.
- **Ventajas:** el estado inválido no se puede almacenar y el rendimiento de las búsquedas está respaldado por índices.
- **Limitaciones:** los invariantes de varias filas siguen en el dominio.
- **Impacto:** condiciona los repositorios y las migraciones.
