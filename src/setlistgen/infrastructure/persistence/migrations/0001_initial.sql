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
