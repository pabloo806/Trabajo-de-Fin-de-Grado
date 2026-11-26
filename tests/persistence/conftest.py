"""Fixtures compartidas por los tests de persistencia (SQLite en memoria)."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

SCHEMA = (
    Path(__file__).resolve().parents[2]
    / "src" / "setlistgen" / "infrastructure" / "persistence" / "schema.sql"
)

AHORA = "2026-11-23T10:00:00Z"
DESPUES = "2026-11-23T11:00:00Z"
ANTES = "2026-11-23T09:00:00Z"
MTIME = 1_700_000_000_000_000_000  # st_mtime_ns de ejemplo


def nueva_conexion() -> sqlite3.Connection:
    """Base en memoria con el esquema aplicado, claves foráneas activas y autocommit."""
    conn = sqlite3.connect(":memory:", isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    conn.execute("PRAGMA foreign_keys = ON")  # executescript no la altera, pero se asegura
    return conn


class Datos:
    """Atajos para insertar filas válidas. Cada método devuelve el id creado."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self.c = conn

    def dj(self, usuario: str = "dj1", password_hash: str = "scrypt$x") -> int:
        return self.c.execute(
            "INSERT INTO dj (usuario, password_hash, fecha_creacion) VALUES (?, ?, ?)",
            (usuario, password_hash, AHORA),
        ).lastrowid

    def biblioteca(self, dj_id: int, ruta: str = "/musica", **over) -> int:
        v = dict(nombre="Mi biblioteca", fecha_creacion=AHORA, fecha_ultima_actualizacion=AHORA)
        v.update(over)
        return self.c.execute(
            "INSERT INTO biblioteca (dj_id, nombre, ruta_raiz, fecha_creacion, fecha_ultima_actualizacion)"
            " VALUES (?, ?, ?, ?, ?)",
            (dj_id, v["nombre"], ruta, v["fecha_creacion"], v["fecha_ultima_actualizacion"]),
        ).lastrowid

    def pista(self, dj_id: int, ruta: str = "/musica/a.mp3", **over) -> int:
        v = dict(titulo="Titulo", artista="Artista", duracion_seg=240.0, genero="House", bpm=124.0,
                 tonalidad="Am", tamano_bytes=1000, fecha_modificacion_archivo=MTIME,
                 estado="disponible", motivo_fallo=None, motor_mir="essentia 2.1", fecha_analisis=AHORA)
        v.update(over)
        return self.c.execute(
            "INSERT INTO pista (dj_id, ruta_local, titulo, artista, duracion_seg, genero, bpm, tonalidad,"
            " tamano_bytes, fecha_modificacion_archivo, estado, motivo_fallo, motor_mir, fecha_analisis)"
            " VALUES (:dj, :ruta, :titulo, :artista, :duracion_seg, :genero, :bpm, :tonalidad,"
            " :tamano_bytes, :fecha_modificacion_archivo, :estado, :motivo_fallo, :motor_mir, :fecha_analisis)",
            {"dj": dj_id, "ruta": ruta, **v},
        ).lastrowid

    def pista_fallida(self, dj_id: int, ruta: str = "/musica/mala.mp3", motivo: str = "fichero corrupto") -> int:
        return self.pista(dj_id, ruta, estado="fallida", motivo_fallo=motivo, duracion_seg=None,
                          bpm=None, tonalidad=None, motor_mir=None, fecha_analisis=None)

    def vincular(self, biblioteca_id: int, pista_id: int) -> None:
        self.c.execute("INSERT INTO biblioteca_pista (biblioteca_id, pista_id) VALUES (?, ?)",
                       (biblioteca_id, pista_id))

    def setlist(self, dj_id: int, nombre: str = "Sesion", **over) -> int:
        v = dict(fecha_creacion=AHORA, fecha_modificacion=AHORA, duracion_objetivo_seg=9000.0,
                 bpm_min=85.0, bpm_max=110.0, preset_camelot="estricta", semilla=42)
        v.update(over)
        cols = ["dj_id", "nombre"] + list(v)
        marcas = ", ".join("?" for _ in cols)
        return self.c.execute(
            f"INSERT INTO setlist ({', '.join(cols)}) VALUES ({marcas})",
            [dj_id, nombre, *v.values()],
        ).lastrowid

    def anadir(self, setlist_id: int, pista_id: int, orden: int) -> None:
        self.c.execute("INSERT INTO setlist_pista (setlist_id, pista_id, orden) VALUES (?, ?, ?)",
                       (setlist_id, pista_id, orden))


@pytest.fixture
def conn():
    c = nueva_conexion()
    yield c
    c.close()


@pytest.fixture
def datos(conn):
    return Datos(conn)
