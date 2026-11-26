-- =====================================================================================
-- SetlistGen · esquema SQLite v1.0                      (docs/architecture/data-model.md)
-- Requiere SQLite >= 3.31 (columnas generadas).
-- Cada conexión debe ejecutar PRAGMA foreign_keys = ON (no persiste en el fichero).
-- Convenciones: fechas en TEXT ISO 8601 UTC con formato fijo (2026-11-23T10:15:00Z);
--               fecha_modificacion_archivo en nanosegundos (st_mtime_ns);
--               BPM redondeado a 2 decimales por la aplicación.
-- =====================================================================================
PRAGMA foreign_keys = ON;

BEGIN;

CREATE TABLE dj (
    id             INTEGER PRIMARY KEY,
    usuario        TEXT NOT NULL COLLATE NOCASE UNIQUE CHECK (length(trim(usuario)) > 0),
    password_hash  TEXT NOT NULL CHECK (length(password_hash) > 0),
    fecha_creacion TEXT NOT NULL
);

CREATE TABLE biblioteca (
    id                         INTEGER PRIMARY KEY,
    dj_id                      INTEGER NOT NULL REFERENCES dj (id) ON DELETE CASCADE,
    nombre                     TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    ruta_raiz                  TEXT NOT NULL CHECK (length(trim(ruta_raiz)) > 0),
    fecha_creacion             TEXT NOT NULL,
    fecha_ultima_actualizacion TEXT NOT NULL,
    UNIQUE (dj_id, ruta_raiz),
    CHECK (fecha_ultima_actualizacion >= fecha_creacion)
);

CREATE TABLE pista (
    id                         INTEGER PRIMARY KEY,
    dj_id                      INTEGER NOT NULL REFERENCES dj (id) ON DELETE CASCADE,
    ruta_local                 TEXT NOT NULL CHECK (length(trim(ruta_local)) > 0),
    titulo                     TEXT,
    artista                    TEXT,
    duracion_seg               REAL CHECK (duracion_seg IS NULL OR duracion_seg > 0),
    genero                     TEXT,
    bpm                        REAL CHECK (bpm IS NULL OR bpm > 0),
    tonalidad                  TEXT CHECK (tonalidad IS NULL OR tonalidad IN (
                                   'G#m','D#m','A#m','Fm','Cm','Gm','Dm','Am','Em','Bm','F#m','C#m',
                                   'B','F#','C#','G#','D#','A#','F','C','G','D','A','E')),
    codigo_camelot             TEXT GENERATED ALWAYS AS (
                                   CASE tonalidad
                                       WHEN 'G#m' THEN '1A'  WHEN 'D#m' THEN '2A'  WHEN 'A#m' THEN '3A'
                                       WHEN 'Fm'  THEN '4A'  WHEN 'Cm'  THEN '5A'  WHEN 'Gm'  THEN '6A'
                                       WHEN 'Dm'  THEN '7A'  WHEN 'Am'  THEN '8A'  WHEN 'Em'  THEN '9A'
                                       WHEN 'Bm'  THEN '10A' WHEN 'F#m' THEN '11A' WHEN 'C#m' THEN '12A'
                                       WHEN 'B'   THEN '1B'  WHEN 'F#'  THEN '2B'  WHEN 'C#'  THEN '3B'
                                       WHEN 'G#'  THEN '4B'  WHEN 'D#'  THEN '5B'  WHEN 'A#'  THEN '6B'
                                       WHEN 'F'   THEN '7B'  WHEN 'C'   THEN '8B'  WHEN 'G'   THEN '9B'
                                       WHEN 'D'   THEN '10B' WHEN 'A'   THEN '11B' WHEN 'E'   THEN '12B'
                                   END) STORED,
    tamano_bytes               INTEGER NOT NULL CHECK (tamano_bytes >= 0),
    fecha_modificacion_archivo INTEGER NOT NULL,
    estado                     TEXT NOT NULL CHECK (estado IN ('disponible', 'no_disponible', 'fallida')),
    motivo_fallo               TEXT CHECK (motivo_fallo IS NULL OR length(trim(motivo_fallo)) > 0),
    motor_mir                  TEXT CHECK (motor_mir IS NULL OR length(trim(motor_mir)) > 0),
    fecha_analisis             TEXT,
    UNIQUE (dj_id, ruta_local),
    CHECK ((estado = 'fallida') = (motivo_fallo IS NOT NULL)),
    CHECK (estado = 'fallida'
           OR (duracion_seg IS NOT NULL AND bpm IS NOT NULL AND tonalidad IS NOT NULL
               AND motor_mir IS NOT NULL AND fecha_analisis IS NOT NULL))
);

CREATE TABLE biblioteca_pista (
    biblioteca_id INTEGER NOT NULL REFERENCES biblioteca (id) ON DELETE CASCADE,
    pista_id      INTEGER NOT NULL REFERENCES pista (id)      ON DELETE CASCADE,
    PRIMARY KEY (biblioteca_id, pista_id)
) WITHOUT ROWID;

CREATE TABLE setlist (
    id                    INTEGER PRIMARY KEY,
    dj_id                 INTEGER NOT NULL REFERENCES dj (id) ON DELETE CASCADE,
    nombre                TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    fecha_creacion        TEXT NOT NULL,
    fecha_modificacion    TEXT NOT NULL,
    duracion_objetivo_seg REAL NOT NULL CHECK (duracion_objetivo_seg > 0),
    tolerancia_pct        REAL NOT NULL DEFAULT 5 CHECK (tolerancia_pct >= 0 AND tolerancia_pct < 100),
    bpm_min               REAL NOT NULL CHECK (bpm_min > 0),
    bpm_max               REAL NOT NULL,
    preset_camelot        TEXT NOT NULL CHECK (preset_camelot IN ('estricta', 'energetica')),
    semilla               INTEGER NOT NULL CHECK (semilla >= 0),
    UNIQUE (dj_id, nombre),
    CHECK (bpm_max >= bpm_min),
    CHECK (fecha_modificacion >= fecha_creacion)
);

CREATE TABLE setlist_pista (
    setlist_id INTEGER NOT NULL REFERENCES setlist (id) ON DELETE CASCADE,
    pista_id   INTEGER NOT NULL REFERENCES pista (id)   ON DELETE RESTRICT,
    orden      INTEGER NOT NULL CHECK (orden >= 1),
    PRIMARY KEY (setlist_id, pista_id),
    UNIQUE (setlist_id, orden)
) WITHOUT ROWID;

-- Índices. Las claves UNIQUE ya indexan (dj_id, ruta_local), (dj_id, ruta_raiz) y (dj_id, nombre).
CREATE INDEX ix_pista_candidatas  ON pista (dj_id, estado, bpm);          -- generación, búsqueda y recuentos
CREATE INDEX ix_setlist_pista_rev ON setlist_pista (pista_id);            -- RESTRICT y usos de una pista
CREATE INDEX ix_setlist_dj_fecha  ON setlist (dj_id, fecha_modificacion); -- lista de setlists guardados

-- Aislamiento entre cuentas (RNF-12): la pista y su biblioteca o setlist son del mismo DJ.
CREATE TRIGGER trg_biblioteca_pista_mismo_dj
BEFORE INSERT ON biblioteca_pista
WHEN (SELECT dj_id FROM biblioteca WHERE id = NEW.biblioteca_id)
     IS NOT (SELECT dj_id FROM pista WHERE id = NEW.pista_id)
BEGIN
    SELECT RAISE(ABORT, 'La biblioteca y la pista pertenecen a DJ distintos');
END;

CREATE TRIGGER trg_setlist_pista_mismo_dj
BEFORE INSERT ON setlist_pista
WHEN (SELECT dj_id FROM setlist WHERE id = NEW.setlist_id)
     IS NOT (SELECT dj_id FROM pista WHERE id = NEW.pista_id)
BEGIN
    SELECT RAISE(ABORT, 'El setlist y la pista pertenecen a DJ distintos');
END;

-- El propietario no puede cambiar.
CREATE TRIGGER trg_pista_dj_inmutable BEFORE UPDATE OF dj_id ON pista
WHEN NEW.dj_id IS NOT OLD.dj_id
BEGIN SELECT RAISE(ABORT, 'dj_id no es modificable'); END;

CREATE TRIGGER trg_biblioteca_dj_inmutable BEFORE UPDATE OF dj_id ON biblioteca
WHEN NEW.dj_id IS NOT OLD.dj_id
BEGIN SELECT RAISE(ABORT, 'dj_id no es modificable'); END;

CREATE TRIGGER trg_setlist_dj_inmutable BEFORE UPDATE OF dj_id ON setlist
WHEN NEW.dj_id IS NOT OLD.dj_id
BEGIN SELECT RAISE(ABORT, 'dj_id no es modificable'); END;

PRAGMA user_version = 1;

COMMIT;
