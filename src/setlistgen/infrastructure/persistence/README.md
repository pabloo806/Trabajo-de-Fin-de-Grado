# Persistencia (SQLite)

> Destino en el repositorio: `src/setlistgen/infrastructure/persistence/README.md`. Sustituye a `database/README.md` (ver `docs/architecture/README.md`, sección 4).

**Versión:** 2.0 · **Fecha:** 2026-11-14 · **Estado:** esquema inicial **provisional**, verificado en SQLite 3.45.1; sin repositorios implementados

> La persistencia **no está cerrada**: el esquema depende de supuestos sobre OD-03 a OD-07 que los tutores no han validado (ADR-004, riesgo R-13). Cualquier cambio posterior se hace con una migración nueva.

## Motor

| Aspecto | Decisión |
|---|---|
| Base de datos | SQLite, un único fichero local (ADR-004) |
| Versión mínima | **3.37** (tablas `STRICT`). Columnas generadas requieren 3.31 |
| Comprobación | Al arrancar: `sqlite3.sqlite_version_info >= (3, 37, 0)`. La versión que incluye Python varía por sistema (R-11) |
| Modo de diario | `WAL` (propuesta) |
| Claves foráneas | `PRAGMA foreign_keys = ON` en **cada** conexión; SQLite no las aplica por defecto |
| Escritor | Uno a la vez. Un coordinador persiste los resultados del análisis en paralelo (ADR-004) |
| Nombre del fichero | Convención propuesta: `*.setlistgen` (es un fichero SQLite normal) |

Pragmas de conexión:

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;     -- se guarda en el fichero
PRAGMA synchronous = NORMAL;
```

`WAL` crea los ficheros auxiliares `-wal` y `-shm` junto a la base. **Una copia de seguridad no debe ser un simple copiado del fichero principal**: use la API de copia de `sqlite3.Connection.backup()` o `VACUUM INTO`.

## Contenido de esta carpeta

```text
persistence/
├── README.md
├── migrations/
│   ├── 0001_initial.sql              Esquema inicial (20 tablas STRICT)
│   └── pending/
│       └── 0002_library_od05.sql     CONDICIONAL: solo si se valida OD-05
└── repositories/                     Repositorios SQLite (pendientes de implementar)
```

El contenido de `0001_initial.sql` es el `schema.sql` entregado con [`database-schema.md`](../../../../docs/architecture/database-schema.md), que contiene el DDL comentado y la verificación. El aplicador de migraciones **no** ejecuta nada de `pending/`.

## Convenciones del esquema

| Aspecto | Convención |
|---|---|
| UUID | `TEXT` de 36 caracteres, minúsculas, con guiones |
| Enumeraciones | `TEXT` con `CHECK (columna IN (...))`, valores `Enum.value` del dominio |
| Booleanos | `INTEGER` 0 o 1 |
| Fechas | `TEXT` ISO 8601 en UTC. El repositorio exige `datetime` con zona UTC (N-43) |
| Rutas | `TEXT` Unicode sin conversión; `path_normalized` la calcula el repositorio |

## Tablas

| Agregado | Tablas |
|---|---|
| Catálogo | `track`, `track_metadata`, `track_location`, `track_fingerprint` |
| Análisis | `analysis_engine`, `analysis_result`, `app_setting` |
| Generación | `setlist`, `generation_request`, `request_harmonic_move`, `allowed_key`, `genre_segment`, `anchor`, `setlist_track`, `transition` |
| Evaluación | `reference_measurement`, `evaluation_report`, `evaluation_error_count`, `evaluation_exclusion` |
| Técnica | `schema_migration` |

Particularidades que importan al implementar los repositorios:

- `analysis_result.camelot_code` es una **columna generada y almacenada**: no se inserta ni se actualiza.
- `track_location` tiene un índice único parcial: una ruta normalizada solo puede tener **una** ubicación vigente (`active` o `failed`). `absent` y `moved` son históricas.
- `reference_measurement.rekordbox_version` usa `'unknown'` cuando no se conoce. El repositorio traduce `None` del dominio a `'unknown'` y viceversa.
- `setlist_track` y `transition` son **instantáneas**: no se actualizan cuando cambian los metadatos de la pista. Al editar un setlist se reescriben (CU-08).
- Un setlist siempre tiene solicitud: se inserta `setlist` y `generation_request` **en la misma transacción**.
- Una pista **no se borra** nunca: se marca ausente (RF-09c). Las claves foráneas con `RESTRICT` lo impiden.

Lo que el esquema **no** impone (posiciones contiguas, solapes de segmentos, suma de errores, normalización de la ruta) queda en el dominio y en el repositorio. Lista completa en `database-schema.md`, sección 6.

## Aplicar el esquema inicial

Comprobar la versión de SQLite que usa Python:

```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

Crear una base nueva:

```python
import sqlite3
from pathlib import Path

con = sqlite3.connect("biblioteca.setlistgen")
con.execute("PRAGMA foreign_keys = ON")
con.execute("PRAGMA journal_mode = WAL")
con.executescript(Path("migrations/0001_initial.sql").read_text(encoding="utf-8"))
con.close()
```

El script lleva su propia transacción (`BEGIN`/`COMMIT`) y registra la versión en `schema_migration`.

Comprobar el resultado:

```sql
PRAGMA integrity_check;     -- debe devolver "ok"
PRAGMA foreign_key_check;   -- sin filas
SELECT version, description FROM schema_migration;
```

Con la herramienta de línea de comandos (de versión 3.37 o posterior) también sirve `sqlite3 biblioteca.setlistgen < migrations/0001_initial.sql`.

## Gestión de migraciones (RNF-27)

| Regla | Detalle |
|---|---|
| Nombre | `NNNN_descripcion.sql`, con número correlativo de cuatro cifras |
| Dirección | Solo hacia delante |
| Inmutabilidad | **Una migración aplicada no se edita.** Un cambio es una migración nueva |
| Transacción | Cada fichero se ejecuta completo o no se ejecuta, y se registra a sí misma en `schema_migration` |
| Orden | Se aplican las que no figuran en `schema_migration`, por número |
| Datos | Se migra sin pérdida: una base de versión anterior pasa la prueba `T-ARQ-06` |
| Cambios que SQLite no admite con `ALTER` | Reconstrucción de tabla: crear la nueva, copiar, borrar la antigua y renombrar, con las claves foráneas desactivadas durante el proceso |
| Condicionales | Se guardan en `pending/` hasta que la decisión se valide; entonces se mueven a `migrations/` con el siguiente número |

### Migración 2 condicional (OD-05, entidad `Library`)

Solo si los tutores validan OD-05. Añade la tabla `library` y una columna nullable `track_location.library_id` con su clave foránea (`ON DELETE SET NULL`) y un índice parcial. Está probada sobre la migración 1 y no obliga a reconstruir tablas. El texto completo está en `database-schema.md`, sección 7.

### Migraciones previsibles según las decisiones abiertas

| OD | Si se rechaza el supuesto | Alcance de la migración |
|---|---|---|
| OD-03 | Huellas por ubicación | Mover `track_fingerprint` (copia de datos) |
| OD-04 | Un resultado por pista | Cambiar la unicidad de `analysis_result` y eliminar `analysis_engine` o `app_setting` |
| OD-06 | Recalcular siempre | Eliminar `transition` y las columnas de instantánea de `setlist_track` |

## Estado

| Elemento | Estado |
|---|---|
| Esquema inicial | Escrito y verificado (integridad, restricciones, planes de consulta) |
| Migración 2 (OD-05) | Preparada, sin aplicar |
| Aplicador de migraciones | Pendiente |
| Repositorios SQLite | Pendientes |
| Prueba de migración desde versión anterior (T-ARQ-06) | Pendiente (hay una sola versión) |
| Medición de RNF-04 con ficheros reales | Pendiente. La prueba de acceso a la base en memoria (29 ms por 5 000 búsquedas por ruta) **no verifica** el requisito |

## Documentación relacionada

[`data-model.md`](../../../../docs/architecture/data-model.md) (índice), [`domain-model.md`](../../../../docs/architecture/domain-model.md), [`conceptual-model.md`](../../../../docs/architecture/conceptual-model.md), [`er-model.md`](../../../../docs/architecture/er-model.md), [`database-schema.md`](../../../../docs/architecture/database-schema.md) y [ADR-004](../../../../docs/architecture/adrs/ADR-004-persistencia.md).
