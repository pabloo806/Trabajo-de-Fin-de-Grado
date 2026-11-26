"""Consultas críticas Q-01 a Q-19 (data-model.md, sección 7).

Para cada consulta se comprueba que:
  1. se ejecuta sin error y devuelve lo esperado (dentro de una transacción que se revierte);
  2. su EXPLAIN QUERY PLAN usa los índices previstos y no recorre ninguna tabla entera (sin «SCAN»).

Se carga un volumen realista (2 DJ x 2 000 pistas, 20 setlists de 30 pistas) y se ejecuta ANALYZE,
para que el optimizador decida como lo haría con datos reales.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable

import pytest

from conftest import AHORA, DESPUES, MTIME, nueva_conexion

N_PISTAS = 2000
N_CUENTAS_EXTRA = 60


# ---------------------------------------------------------------------------------------
# Datos de prueba
# ---------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def ctx():
    conn = nueva_conexion()
    conn.execute("BEGIN")
    ids = {}
    for usuario in ("dj1", "dj2"):
        dj = conn.execute("INSERT INTO dj (usuario, password_hash, fecha_creacion) VALUES (?, 'h', ?)",
                          (usuario, AHORA)).lastrowid
        biblios = [conn.execute(
            "INSERT INTO biblioteca (dj_id, nombre, ruta_raiz, fecha_creacion, fecha_ultima_actualizacion)"
            " VALUES (?, ?, ?, ?, ?)", (dj, f"B{i}", f"/{usuario}/b{i}", AHORA, AHORA)).lastrowid for i in range(2)]
        tonalidades = ["Am", "C", "Dm", "F", "Gm", "A#", "Em", "G"]
        pistas = []
        for i in range(N_PISTAS):
            estado = "disponible" if i % 50 else ("no_disponible" if i % 100 else "disponible")
            pid = conn.execute(
                "INSERT INTO pista (dj_id, ruta_local, titulo, artista, duracion_seg, genero, bpm, tonalidad,"
                " tamano_bytes, fecha_modificacion_archivo, estado, motor_mir, fecha_analisis)"
                " VALUES (?, ?, ?, ?, ?, 'House', ?, ?, ?, ?, ?, 'essentia 2.1', ?)",
                (dj, f"/{usuario}/b{i % 2}/pista{i}.mp3", f"Titulo {i}", f"Artista {i % 40}", 200.0 + i % 120,
                 80.0 + (i % 60) + 0.25, tonalidades[i % 8], 1000 + i, MTIME + i, estado, AHORA)).lastrowid
            pistas.append(pid)
            conn.execute("INSERT INTO biblioteca_pista VALUES (?, ?)", (biblios[i % 2], pid))
        setlists = []
        for s in range(20):
            sid = conn.execute(
                "INSERT INTO setlist (dj_id, nombre, fecha_creacion, fecha_modificacion, duracion_objetivo_seg,"
                " bpm_min, bpm_max, preset_camelot, semilla) VALUES (?, ?, ?, ?, 7200, 85, 125, 'estricta', ?)",
                (dj, f"Setlist {s}", "2026-11-01T09:00:00Z", f"2026-11-{(s % 28) + 1:02d}T10:00:00Z", s)).lastrowid
            setlists.append(sid)
            for orden in range(1, 31):
                conn.execute("INSERT INTO setlist_pista VALUES (?, ?, ?)", (sid, pistas[(s * 30 + orden) % N_PISTAS], orden))
        ids[usuario] = {"dj": dj, "bib": biblios[0], "pistas": pistas, "setlist": setlists[0]}
    # Cuentas adicionales (sin pistas) para que las estadísticas de biblioteca y setlist sean
    # representativas: con 4 o 40 filas el optimizador prefiere recorrer la tabla entera, lo cual es correcto.
    for i in range(N_CUENTAS_EXTRA):
        dj = conn.execute("INSERT INTO dj (usuario, password_hash, fecha_creacion) VALUES (?, 'h', ?)",
                          (f"extra{i}", AHORA)).lastrowid
        for j in range(2):
            conn.execute("INSERT INTO biblioteca (dj_id, nombre, ruta_raiz, fecha_creacion, fecha_ultima_actualizacion)"
                         " VALUES (?, 'B', ?, ?, ?)", (dj, f"/extra{i}/{j}", AHORA, AHORA))
        for j in range(3):
            conn.execute("INSERT INTO setlist (dj_id, nombre, fecha_creacion, fecha_modificacion, duracion_objetivo_seg,"
                         " bpm_min, bpm_max, preset_camelot, semilla)"
                         " VALUES (?, ?, '2026-11-01T09:00:00Z', '2026-11-02T09:00:00Z', 3600, 80, 120, 'estricta', 1)",
                         (dj, f"S{j}"))
    conn.execute("COMMIT")
    conn.execute("ANALYZE")
    yield {"conn": conn, **ids["dj1"], "otro": ids["dj2"]}
    conn.close()


# ---------------------------------------------------------------------------------------
# Catálogo de consultas (idéntico a la sección 7 de data-model.md)
# ---------------------------------------------------------------------------------------
@dataclass
class Q:
    id: str
    sql: str
    params: Callable[[dict], dict]
    usa: tuple[str, ...] = ()          # fragmentos que deben aparecer en el plan (todos)
    usa_alguno: tuple[str, ...] = ()   # al menos uno de estos debe aparecer
    filas: Callable[[list], bool] = field(default=lambda filas: True)  # comprobación del resultado
    modifica: bool = False


QUERIES: list[Q] = [
    Q("Q-01", "SELECT id, password_hash FROM dj WHERE usuario = :usuario",
      lambda c: {"usuario": "DJ1"},  # distinto uso de mayúsculas: COLLATE NOCASE
      usa=("sqlite_autoindex_dj_1",), filas=lambda f: len(f) == 1),

    Q("Q-02", "INSERT INTO dj (usuario, password_hash, fecha_creacion) VALUES (:usuario, :hash, :ahora)",
      lambda c: {"usuario": "nuevo", "hash": "h", "ahora": AHORA}, modifica=True),

    Q("Q-03", "INSERT INTO biblioteca (dj_id, nombre, ruta_raiz, fecha_creacion, fecha_ultima_actualizacion)"
              " VALUES (:dj, :nombre, :ruta, :ahora, :ahora)",
      lambda c: {"dj": c["dj"], "nombre": "N", "ruta": "/nueva", "ahora": AHORA}, modifica=True),

    Q("Q-04", "SELECT id, ruta_local, tamano_bytes, fecha_modificacion_archivo, estado FROM pista WHERE dj_id = :dj",
      lambda c: {"dj": c["dj"]}, usa_alguno=("sqlite_autoindex_pista_1", "ix_pista_candidatas"),
      filas=lambda f: len(f) == N_PISTAS),

    Q("Q-05", """INSERT INTO pista (dj_id, ruta_local, titulo, artista, duracion_seg, genero, bpm, tonalidad,
                   tamano_bytes, fecha_modificacion_archivo, estado, motivo_fallo, motor_mir, fecha_analisis)
VALUES (:dj, :ruta, :titulo, :artista, :duracion, :genero, :bpm, :tonalidad,
        :tamano, :mtime_ns, :estado, :motivo, :motor, :fecha)
ON CONFLICT (dj_id, ruta_local) DO UPDATE SET
    titulo = excluded.titulo, artista = excluded.artista, duracion_seg = excluded.duracion_seg,
    genero = excluded.genero, bpm = excluded.bpm, tonalidad = excluded.tonalidad,
    tamano_bytes = excluded.tamano_bytes, fecha_modificacion_archivo = excluded.fecha_modificacion_archivo,
    estado = excluded.estado, motivo_fallo = excluded.motivo_fallo,
    motor_mir = excluded.motor_mir, fecha_analisis = excluded.fecha_analisis""",
      lambda c: {"dj": c["dj"], "ruta": "/dj1/b0/pista0.mp3", "titulo": "Nuevo", "artista": "A", "duracion": 300.0,
                 "genero": "Techno", "bpm": 130.5, "tonalidad": "Am", "tamano": 5, "mtime_ns": MTIME + 99,
                 "estado": "disponible", "motivo": None, "motor": "essentia 2.1", "fecha": DESPUES},
      modifica=True),

    Q("Q-06", "INSERT OR IGNORE INTO biblioteca_pista (biblioteca_id, pista_id) VALUES (:bib, :pista)",
      lambda c: {"bib": c["bib"], "pista": c["pistas"][0]}, modifica=True),

    Q("Q-07", """SELECT p.id, p.ruta_local, p.estado
FROM biblioteca_pista bp JOIN pista p ON p.id = bp.pista_id
WHERE bp.biblioteca_id = :bib AND p.dj_id = :dj""",
      lambda c: {"bib": c["bib"], "dj": c["dj"]}, usa_alguno=("PRIMARY KEY (biblioteca_id=?)", "biblioteca_id=?"),
      filas=lambda f: len(f) == N_PISTAS // 2),

    Q("Q-08a", "UPDATE pista SET estado = 'no_disponible' WHERE id = :pista AND dj_id = :dj AND estado = 'disponible'",
      lambda c: {"pista": c["pistas"][1], "dj": c["dj"]}, usa=("INTEGER PRIMARY KEY",), modifica=True),

    Q("Q-08b", "UPDATE pista SET estado = 'disponible' WHERE id = :pista AND dj_id = :dj AND estado = 'no_disponible'",
      lambda c: {"pista": c["pistas"][50], "dj": c["dj"]}, usa=("INTEGER PRIMARY KEY",), modifica=True),

    Q("Q-09", "UPDATE biblioteca SET fecha_ultima_actualizacion = :ahora WHERE id = :bib AND dj_id = :dj",
      lambda c: {"ahora": DESPUES, "bib": c["bib"], "dj": c["dj"]}, usa=("INTEGER PRIMARY KEY",), modifica=True),

    Q("Q-10", """SELECT b.id, b.nombre, b.ruta_raiz, b.fecha_ultima_actualizacion,
       (SELECT COUNT(*) FROM biblioteca_pista bp WHERE bp.biblioteca_id = b.id) AS n_pistas,
       (SELECT COUNT(*) FROM biblioteca_pista bp JOIN pista p ON p.id = bp.pista_id
         WHERE bp.biblioteca_id = b.id AND p.estado = 'no_disponible') AS n_no_disponibles,
       (SELECT COUNT(*) FROM biblioteca_pista bp JOIN pista p ON p.id = bp.pista_id
         WHERE bp.biblioteca_id = b.id AND p.estado = 'fallida') AS n_fallidas
FROM biblioteca b
WHERE b.dj_id = :dj""",
      lambda c: {"dj": c["dj"]}, usa=("sqlite_autoindex_biblioteca_1",),
      filas=lambda f: len(f) == 2 and f[0][4] == N_PISTAS // 2),

    Q("Q-11", """SELECT id, bpm, codigo_camelot, duracion_seg
FROM pista
WHERE dj_id = :dj AND estado = 'disponible' AND bpm BETWEEN :bpm_min AND :bpm_max""",
      lambda c: {"dj": c["dj"], "bpm_min": 100.0, "bpm_max": 110.0}, usa=("ix_pista_candidatas",),
      filas=lambda f: 0 < len(f) < N_PISTAS),

    Q("Q-12", """SELECT p.id, p.bpm, p.codigo_camelot, p.duracion_seg
FROM biblioteca_pista bp JOIN pista p ON p.id = bp.pista_id
WHERE bp.biblioteca_id = :bib AND p.dj_id = :dj AND p.estado = 'disponible'
  AND p.bpm BETWEEN :bpm_min AND :bpm_max""",
      lambda c: {"bib": c["bib"], "dj": c["dj"], "bpm_min": 100.0, "bpm_max": 110.0},
      usa_alguno=("biblioteca_id=?", "ix_pista_candidatas"), filas=lambda f: len(f) > 0),

    Q("Q-13", """SELECT id, titulo, artista, bpm, codigo_camelot, duracion_seg
FROM pista
WHERE dj_id = :dj AND estado = 'disponible'
  AND (:texto IS NULL OR titulo LIKE '%' || :texto || '%' OR artista LIKE '%' || :texto || '%')
  AND (:bpm_min IS NULL OR bpm BETWEEN :bpm_min AND :bpm_max)
  AND (:camelot IS NULL OR codigo_camelot = :camelot)
ORDER BY titulo COLLATE NOCASE
LIMIT 50""",
      lambda c: {"dj": c["dj"], "texto": "Titulo 12", "bpm_min": None, "bpm_max": None, "camelot": "8A"},
      usa_alguno=("ix_pista_candidatas", "sqlite_autoindex_pista_1"), filas=lambda f: len(f) > 0),

    Q("Q-14", "SELECT id FROM setlist WHERE dj_id = :dj AND nombre = :nombre",
      lambda c: {"dj": c["dj"], "nombre": "Setlist 3"}, usa=("sqlite_autoindex_setlist_1",),
      filas=lambda f: len(f) == 1),

    Q("Q-15a", """INSERT INTO setlist (dj_id, nombre, fecha_creacion, fecha_modificacion, duracion_objetivo_seg,
                     tolerancia_pct, bpm_min, bpm_max, preset_camelot, semilla)
VALUES (:dj, :nombre, :ahora, :ahora, :duracion, :tolerancia, :bpm_min, :bpm_max, :preset, :semilla)""",
      lambda c: {"dj": c["dj"], "nombre": "Nuevo", "ahora": AHORA, "duracion": 3600.0, "tolerancia": 5.0,
                 "bpm_min": 90.0, "bpm_max": 120.0, "preset": "energetica", "semilla": 1}, modifica=True),

    Q("Q-15b", "INSERT INTO setlist_pista (setlist_id, pista_id, orden) VALUES (:set, :pista, :orden)",
      lambda c: {"set": c["setlist"], "pista": c["pistas"][1999], "orden": 99}, modifica=True),

    Q("Q-16a", """UPDATE setlist SET fecha_modificacion = :ahora, duracion_objetivo_seg = :duracion, tolerancia_pct = :tolerancia,
                   bpm_min = :bpm_min, bpm_max = :bpm_max, preset_camelot = :preset
WHERE id = :set AND dj_id = :dj""",
      lambda c: {"ahora": DESPUES, "duracion": 5000.0, "tolerancia": 4.0, "bpm_min": 90.0, "bpm_max": 118.0,
                 "preset": "estricta", "set": c["setlist"], "dj": c["dj"]}, usa=("INTEGER PRIMARY KEY",), modifica=True),

    Q("Q-16b", "DELETE FROM setlist_pista WHERE setlist_id = :set",
      lambda c: {"set": c["setlist"]}, usa_alguno=("PRIMARY KEY (setlist_id=?)", "setlist_id=?"), modifica=True),

    Q("Q-16c", "INSERT INTO setlist_pista (setlist_id, pista_id, orden) VALUES (:set, :pista, :orden)",
      lambda c: {"set": c["setlist"], "pista": c["pistas"][1500], "orden": 31}, modifica=True),

    Q("Q-17", """SELECT s.id, s.nombre, s.fecha_modificacion,
       (SELECT COUNT(*) FROM setlist_pista sp WHERE sp.setlist_id = s.id) AS n_pistas,
       (SELECT SUM(p.duracion_seg) FROM setlist_pista sp JOIN pista p ON p.id = sp.pista_id
         WHERE sp.setlist_id = s.id) AS duracion_total_seg
FROM setlist s
WHERE s.dj_id = :dj
ORDER BY s.fecha_modificacion DESC""",
      lambda c: {"dj": c["dj"]}, usa=("ix_setlist_dj_fecha",),
      filas=lambda f: len(f) == 20 and f[0][3] == 30 and f[0][4] > 0
      and [r[2] for r in f] == sorted((r[2] for r in f), reverse=True)),

    Q("Q-18", """SELECT sp.orden, p.id, p.titulo, p.artista, p.bpm, p.codigo_camelot, p.duracion_seg, p.estado, p.ruta_local
FROM setlist s
JOIN setlist_pista sp ON sp.setlist_id = s.id
JOIN pista p ON p.id = sp.pista_id
WHERE s.id = :set AND s.dj_id = :dj
ORDER BY sp.orden""",
      lambda c: {"set": c["setlist"], "dj": c["dj"]}, usa_alguno=("setlist_id=?",),
      filas=lambda f: [r[0] for r in f] == list(range(1, 31))),

    Q("Q-19", "DELETE FROM setlist WHERE id = :set AND dj_id = :dj",
      lambda c: {"set": c["setlist"], "dj": c["dj"]}, usa=("INTEGER PRIMARY KEY",), modifica=True),
]

IDS = [q.id for q in QUERIES]
ES_SCAN = re.compile(r"^SCAN\b")


def plan(conn, sql: str, params: dict) -> list[str]:
    return [fila["detail"] for fila in conn.execute("EXPLAIN QUERY PLAN " + sql, params)]


# ---------------------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------------------
def test_cubre_todas_las_consultas_de_la_documentacion():
    ids = {i.rstrip("abc") for i in IDS}
    assert ids == {f"Q-{n:02d}" for n in range(1, 20)}


@pytest.mark.parametrize("q", QUERIES, ids=IDS)
def test_se_ejecuta_y_devuelve_lo_esperado(ctx, q):
    conn = ctx["conn"]
    conn.execute("BEGIN")
    try:
        cur = conn.execute(q.sql, q.params(ctx))
        filas = cur.fetchall() if not q.modifica else []
        if q.modifica:
            assert cur.rowcount >= 0
        else:
            assert q.filas(filas), f"{q.id}: resultado inesperado ({len(filas)} filas)"
    finally:
        conn.execute("ROLLBACK")


@pytest.mark.parametrize("q", QUERIES, ids=IDS)
def test_el_plan_no_recorre_tablas_enteras(ctx, q):
    detalles = plan(ctx["conn"], q.sql, q.params(ctx))
    scans = [d for d in detalles if ES_SCAN.match(d)]
    assert not scans, f"{q.id} recorre tablas enteras: {scans}\nPlan completo: {detalles}"


@pytest.mark.parametrize("q", [q for q in QUERIES if q.usa or q.usa_alguno], ids=lambda q: q.id)
def test_el_plan_usa_los_indices_previstos(ctx, q):
    texto = "\n".join(plan(ctx["conn"], q.sql, q.params(ctx)))
    for fragmento in q.usa:
        assert fragmento in texto, f"{q.id}: falta «{fragmento}» en el plan:\n{texto}"
    if q.usa_alguno:
        assert any(f in texto for f in q.usa_alguno), f"{q.id}: ninguno de {q.usa_alguno} en el plan:\n{texto}"


def test_el_optimizador_recorre_las_tablas_diminutas_y_usa_el_indice_cuando_hay_volumen():
    """Documenta un matiz de data-model.md (7.5): con solo 4 bibliotecas y 40 setlists, SCAN es la opción
    correcta. El índice se elige en cuanto hay varias cuentas, que es lo que simula la fixture."""
    conn = nueva_conexion()
    dj = conn.execute("INSERT INTO dj (usuario, password_hash, fecha_creacion) VALUES ('a', 'h', ?)", (AHORA,)).lastrowid
    conn.execute("INSERT INTO biblioteca (dj_id, nombre, ruta_raiz, fecha_creacion, fecha_ultima_actualizacion)"
                 " VALUES (?, 'B', '/m', ?, ?)", (dj, AHORA, AHORA))
    sql = next(q.sql for q in QUERIES if q.id == "Q-10")
    detalles = plan(conn, sql, {"dj": dj})
    assert detalles  # el plan existe; con una sola fila no se exige uso de índice
    conn.close()


def test_q13_el_like_con_comodin_inicial_no_usa_indice_de_texto(ctx):
    """Documenta la limitación conocida: la búsqueda por título recorre solo las pistas del DJ."""
    q = next(q for q in QUERIES if q.id == "Q-13")
    texto = "\n".join(plan(ctx["conn"], q.sql, q.params(ctx)))
    assert "dj_id=?" in texto, texto  # acotada al DJ, no a toda la tabla


def test_las_consultas_filtran_por_el_dj_y_no_filtran_datos_de_otra_cuenta(ctx):
    conn = ctx["conn"]
    otra = ctx["otro"]
    q11 = next(q for q in QUERIES if q.id == "Q-11")
    mias = {f["id"] for f in conn.execute(q11.sql, q11.params(ctx))}
    assert mias and mias.isdisjoint(set(otra["pistas"]))
    q17 = next(q for q in QUERIES if q.id == "Q-17")
    nombres_ids = {f["id"] for f in conn.execute(q17.sql, {"dj": otra["dj"]})}
    assert nombres_ids and ctx["setlist"] not in nombres_ids
    q18 = next(q for q in QUERIES if q.id == "Q-18")  # setlist ajeno: no devuelve nada
    assert conn.execute(q18.sql, {"set": otra["setlist"], "dj": ctx["dj"]}).fetchall() == []


def test_las_estadisticas_por_estado_usan_un_indice_de_cobertura(ctx):
    sql = "SELECT estado, COUNT(*) FROM pista WHERE dj_id = :dj GROUP BY estado"
    detalles = plan(ctx["conn"], sql, {"dj": ctx["dj"]})
    assert not [d for d in detalles if ES_SCAN.match(d)], detalles
    assert any("ix_pista_candidatas" in d for d in detalles), detalles
