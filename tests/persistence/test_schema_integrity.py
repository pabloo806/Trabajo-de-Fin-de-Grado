"""Integridad del esquema SQLite de SetlistGen (data-model.md v1.0).

Cubre: restricciones CHECK / UNIQUE / NOT NULL, columna generada codigo_camelot, claves foráneas
(CASCADE y RESTRICT), triggers de aislamiento entre cuentas (RNF-12) e inmutabilidad de dj_id,
y el ciclo de estados de la pista junto con la actualización sin romper setlists guardados.
"""
from __future__ import annotations

import sqlite3

import pytest

from conftest import AHORA, ANTES, DESPUES, MTIME

TABLAS = {"dj", "biblioteca", "pista", "biblioteca_pista", "setlist", "setlist_pista"}
TRIGGERS = {
    "trg_biblioteca_pista_mismo_dj", "trg_setlist_pista_mismo_dj",
    "trg_pista_dj_inmutable", "trg_biblioteca_dj_inmutable", "trg_setlist_dj_inmutable",
}
INDICES = {"ix_pista_candidatas", "ix_setlist_pista_rev", "ix_setlist_dj_fecha"}

# Tabla 4.3.1 de data-model.md: tonalidad -> código Camelot.
CAMELOT = {
    "G#m": "1A", "D#m": "2A", "A#m": "3A", "Fm": "4A", "Cm": "5A", "Gm": "6A",
    "Dm": "7A", "Am": "8A", "Em": "9A", "Bm": "10A", "F#m": "11A", "C#m": "12A",
    "B": "1B", "F#": "2B", "C#": "3B", "G#": "4B", "D#": "5B", "A#": "6B",
    "F": "7B", "C": "8B", "G": "9B", "D": "10B", "A": "11B", "E": "12B",
}

UPSERT_PISTA = """
INSERT INTO pista (dj_id, ruta_local, titulo, artista, duracion_seg, genero, bpm, tonalidad,
                   tamano_bytes, fecha_modificacion_archivo, estado, motivo_fallo, motor_mir, fecha_analisis)
VALUES (:dj, :ruta, :titulo, :artista, :duracion, :genero, :bpm, :tonalidad,
        :tamano, :mtime_ns, :estado, :motivo, :motor, :fecha)
ON CONFLICT (dj_id, ruta_local) DO UPDATE SET
    titulo = excluded.titulo, artista = excluded.artista, duracion_seg = excluded.duracion_seg,
    genero = excluded.genero, bpm = excluded.bpm, tonalidad = excluded.tonalidad,
    tamano_bytes = excluded.tamano_bytes, fecha_modificacion_archivo = excluded.fecha_modificacion_archivo,
    estado = excluded.estado, motivo_fallo = excluded.motivo_fallo,
    motor_mir = excluded.motor_mir, fecha_analisis = excluded.fecha_analisis
"""


def params_pista(dj: int, ruta: str = "/musica/a.mp3", **over) -> dict:
    p = dict(dj=dj, ruta=ruta, titulo="T", artista="A", duracion=240.0, genero="House", bpm=124.0,
             tonalidad="Am", tamano=1000, mtime_ns=MTIME, estado="disponible", motivo=None,
             motor="essentia 2.1", fecha=AHORA)
    p.update(over)
    return p


def n(conn, tabla: str) -> int:
    return conn.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]


# ---------------------------------------------------------------------------------------
# Estructura
# ---------------------------------------------------------------------------------------
class TestEstructura:
    def test_version_minima_de_sqlite(self):
        assert sqlite3.sqlite_version_info >= (3, 31, 0), "Se necesitan columnas generadas (SQLite >= 3.31)"

    def test_seis_tablas(self, conn):
        filas = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        assert {f["name"] for f in filas} == TABLAS

    def test_triggers_e_indices(self, conn):
        trg = {f["name"] for f in conn.execute("SELECT name FROM sqlite_master WHERE type='trigger'")}
        idx = {f["name"] for f in conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'ix_%'")}
        assert trg == TRIGGERS
        assert idx == INDICES

    def test_user_version(self, conn):
        assert conn.execute("PRAGMA user_version").fetchone()[0] == 1

    def test_claves_foraneas_activas(self, conn):
        assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1

    def test_integridad_y_claves_foraneas_de_base_vacia(self, conn):
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []


# ---------------------------------------------------------------------------------------
# DJ y biblioteca
# ---------------------------------------------------------------------------------------
class TestDj:
    def test_usuario_unico_sin_distinguir_mayusculas(self, datos):
        datos.dj("Pablo")
        with pytest.raises(sqlite3.IntegrityError):
            datos.dj("pablo")

    @pytest.mark.parametrize("usuario", ["", "   "])
    def test_usuario_vacio_rechazado(self, datos, usuario):
        with pytest.raises(sqlite3.IntegrityError):
            datos.dj(usuario)

    def test_hash_vacio_rechazado(self, datos):
        with pytest.raises(sqlite3.IntegrityError):
            datos.dj("x", password_hash="")

    def test_campos_obligatorios(self, conn):
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO dj (usuario, password_hash) VALUES ('x', 'h')")  # sin fecha_creacion


class TestBiblioteca:
    def test_ruta_unica_por_dj_pero_repetible_entre_dj(self, datos):
        a, b = datos.dj("a"), datos.dj("b")
        datos.biblioteca(a, "/musica")
        with pytest.raises(sqlite3.IntegrityError):
            datos.biblioteca(a, "/musica", nombre="Otra")
        datos.biblioteca(b, "/musica")  # otro DJ puede registrar la misma carpeta

    def test_fecha_de_actualizacion_no_anterior_a_la_de_creacion(self, datos):
        a = datos.dj()
        with pytest.raises(sqlite3.IntegrityError):
            datos.biblioteca(a, fecha_creacion=AHORA, fecha_ultima_actualizacion=ANTES)

    @pytest.mark.parametrize("campo", ["nombre"])
    def test_nombre_vacio_rechazado(self, datos, campo):
        a = datos.dj()
        with pytest.raises(sqlite3.IntegrityError):
            datos.biblioteca(a, **{campo: " "})


# ---------------------------------------------------------------------------------------
# Pista: restricciones y columna generada
# ---------------------------------------------------------------------------------------
class TestPista:
    @pytest.mark.parametrize("over", [
        {"bpm": 0}, {"bpm": -5}, {"duracion_seg": 0}, {"duracion_seg": -1},
        {"tamano_bytes": -1}, {"estado": "otro"}, {"tonalidad": "H"}, {"tonalidad": "am"},
        {"motor_mir": "  "},
    ])
    def test_valores_invalidos_rechazados(self, datos, over):
        a = datos.dj()
        with pytest.raises(sqlite3.IntegrityError):
            datos.pista(a, **over)

    def test_ruta_vacia_rechazada(self, datos):
        a = datos.dj()
        with pytest.raises(sqlite3.IntegrityError):
            datos.pista(a, "  ")

    def test_ruta_unica_por_dj_pero_repetible_entre_dj(self, datos):
        a, b = datos.dj("a"), datos.dj("b")
        datos.pista(a, "/musica/a.mp3")
        with pytest.raises(sqlite3.IntegrityError):
            datos.pista(a, "/musica/a.mp3")
        datos.pista(b, "/musica/a.mp3")  # aislamiento: otra cuenta, otra fila

    def test_fallida_exige_motivo_y_solo_ella_lo_admite(self, datos):
        a = datos.dj()
        with pytest.raises(sqlite3.IntegrityError):
            datos.pista(a, "/m/1.mp3", estado="fallida", motivo_fallo=None, bpm=None, tonalidad=None,
                        duracion_seg=None, motor_mir=None, fecha_analisis=None)
        with pytest.raises(sqlite3.IntegrityError):
            datos.pista(a, "/m/2.mp3", estado="disponible", motivo_fallo="no deberia")
        with pytest.raises(sqlite3.IntegrityError):
            datos.pista_fallida(a, "/m/3.mp3", motivo="  ")

    @pytest.mark.parametrize("campo", ["bpm", "tonalidad", "duracion_seg", "motor_mir", "fecha_analisis"])
    def test_no_fallida_exige_descriptores_y_trazabilidad(self, datos, campo):
        a = datos.dj()
        with pytest.raises(sqlite3.IntegrityError):
            datos.pista(a, **{campo: None})

    @pytest.mark.parametrize("estado", ["disponible", "no_disponible"])
    def test_estados_con_descriptores_validos(self, datos, estado):
        a = datos.dj()
        assert datos.pista(a, estado=estado) > 0

    def test_fallida_puede_no_tener_descriptores(self, datos, conn):
        a = datos.dj()
        pid = datos.pista_fallida(a)
        fila = conn.execute("SELECT bpm, tonalidad, codigo_camelot, motivo_fallo FROM pista WHERE id=?", (pid,)).fetchone()
        assert fila["bpm"] is None and fila["tonalidad"] is None and fila["codigo_camelot"] is None
        assert fila["motivo_fallo"] == "fichero corrupto"

    def test_titulo_artista_genero_pueden_ser_nulos(self, datos):
        a = datos.dj()
        assert datos.pista(a, titulo=None, artista=None, genero=None) > 0

    def test_campos_obligatorios_sin_valor_por_defecto(self, conn, datos):
        a = datos.dj()
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO pista (dj_id, ruta_local) VALUES (?, '/x.mp3')", (a,))

    def test_bpm_decimal_se_conserva(self, datos, conn):
        a = datos.dj()
        pid = datos.pista(a, bpm=127.5)
        assert conn.execute("SELECT bpm FROM pista WHERE id=?", (pid,)).fetchone()[0] == 127.5


class TestCodigoCamelotGenerado:
    @pytest.mark.parametrize("tonalidad, camelot", sorted(CAMELOT.items()))
    def test_las_24_tonalidades(self, datos, conn, tonalidad, camelot):
        a = datos.dj()
        pid = datos.pista(a, tonalidad=tonalidad)
        assert conn.execute("SELECT codigo_camelot FROM pista WHERE id=?", (pid,)).fetchone()[0] == camelot

    def test_correspondencia_biyectiva(self):
        assert len(CAMELOT) == 24 and len(set(CAMELOT.values())) == 24

    def test_se_recalcula_al_cambiar_la_tonalidad(self, datos, conn):
        a = datos.dj()
        pid = datos.pista(a, tonalidad="Am")
        conn.execute("UPDATE pista SET tonalidad='C' WHERE id=?", (pid,))
        assert conn.execute("SELECT codigo_camelot FROM pista WHERE id=?", (pid,)).fetchone()[0] == "8B"

    def test_no_se_puede_escribir_directamente(self, datos, conn):
        a = datos.dj()
        pid = datos.pista(a)
        with pytest.raises(sqlite3.OperationalError):
            conn.execute("UPDATE pista SET codigo_camelot='1A' WHERE id=?", (pid,))
        with pytest.raises(sqlite3.OperationalError):
            conn.execute("INSERT INTO pista (dj_id, ruta_local, tamano_bytes, fecha_modificacion_archivo, estado,"
                         " duracion_seg, bpm, tonalidad, motor_mir, fecha_analisis, codigo_camelot)"
                         " VALUES (?, '/x', 1, 1, 'disponible', 1, 1, 'Am', 'm', 'f', '1A')", (a,))


# ---------------------------------------------------------------------------------------
# Setlist y setlist_pista
# ---------------------------------------------------------------------------------------
class TestSetlist:
    @pytest.mark.parametrize("over", [
        {"semilla": -1}, {"duracion_objetivo_seg": 0}, {"bpm_min": 0},
        {"bpm_min": 120.0, "bpm_max": 100.0}, {"tolerancia_pct": 100}, {"tolerancia_pct": -1},
        {"preset_camelot": "otra"},
        {"fecha_creacion": AHORA, "fecha_modificacion": ANTES},
    ])
    def test_valores_invalidos_rechazados(self, datos, over):
        a = datos.dj()
        with pytest.raises(sqlite3.IntegrityError):
            datos.setlist(a, **over)

    def test_tolerancia_por_defecto_5(self, datos, conn):
        a = datos.dj()
        sid = conn.execute(
            "INSERT INTO setlist (dj_id, nombre, fecha_creacion, fecha_modificacion, duracion_objetivo_seg,"
            " bpm_min, bpm_max, preset_camelot, semilla) VALUES (?, 'S', ?, ?, 3600, 80, 120, 'energetica', 7)",
            (a, AHORA, AHORA)).lastrowid
        assert conn.execute("SELECT tolerancia_pct FROM setlist WHERE id=?", (sid,)).fetchone()[0] == 5

    def test_semilla_de_64_bits_maxima_aceptada(self, datos):
        a = datos.dj()
        assert datos.setlist(a, semilla=2**63 - 1) > 0

    def test_nombre_unico_por_dj_pero_repetible_entre_dj(self, datos):
        a, b = datos.dj("a"), datos.dj("b")
        datos.setlist(a, "Sesion")
        with pytest.raises(sqlite3.IntegrityError):
            datos.setlist(a, "Sesion")
        datos.setlist(b, "Sesion")

    def test_presets_validos(self, datos):
        a = datos.dj()
        datos.setlist(a, "e", preset_camelot="estricta")
        datos.setlist(a, "n", preset_camelot="energetica")


class TestSetlistPista:
    def test_orden_minimo_uno(self, datos):
        a = datos.dj()
        p, s = datos.pista(a), datos.setlist(a)
        with pytest.raises(sqlite3.IntegrityError):
            datos.anadir(s, p, 0)

    def test_orden_unico_en_el_setlist(self, datos):
        a = datos.dj()
        p1, p2 = datos.pista(a, "/m/1.mp3"), datos.pista(a, "/m/2.mp3")
        s = datos.setlist(a)
        datos.anadir(s, p1, 1)
        with pytest.raises(sqlite3.IntegrityError):
            datos.anadir(s, p2, 1)

    def test_pista_no_se_repite_en_el_setlist(self, datos):
        a = datos.dj()
        p = datos.pista(a)
        s = datos.setlist(a)
        datos.anadir(s, p, 1)
        with pytest.raises(sqlite3.IntegrityError):
            datos.anadir(s, p, 2)

    def test_una_pista_puede_estar_en_varios_setlists(self, datos):
        a = datos.dj()
        p = datos.pista(a)
        datos.anadir(datos.setlist(a, "uno"), p, 1)
        datos.anadir(datos.setlist(a, "dos"), p, 1)

    def test_una_pista_puede_estar_en_varias_bibliotecas_sin_duplicarse(self, datos, conn):
        a = datos.dj()
        p = datos.pista(a)
        datos.vincular(datos.biblioteca(a, "/m1"), p)
        datos.vincular(datos.biblioteca(a, "/m2"), p)
        assert n(conn, "pista") == 1 and n(conn, "biblioteca_pista") == 2

    def test_vinculo_biblioteca_pista_unico(self, datos):
        a = datos.dj()
        b, p = datos.biblioteca(a), datos.pista(a)
        datos.vincular(b, p)
        with pytest.raises(sqlite3.IntegrityError):
            datos.vincular(b, p)


# ---------------------------------------------------------------------------------------
# Claves foráneas: CASCADE y RESTRICT
# ---------------------------------------------------------------------------------------
class TestClavesForaneas:
    def test_pista_con_dj_inexistente_rechazada(self, datos):
        with pytest.raises(sqlite3.IntegrityError):
            datos.pista(9999)

    def test_vinculos_con_filas_inexistentes_rechazados(self, datos):
        a = datos.dj()
        p, s = datos.pista(a), datos.setlist(a)
        with pytest.raises(sqlite3.IntegrityError):
            datos.vincular(9999, p)
        with pytest.raises(sqlite3.IntegrityError):
            datos.anadir(s, 9999, 1)

    def test_borrar_setlist_elimina_sus_entradas_pero_no_las_pistas(self, datos, conn):
        a = datos.dj()
        p, s = datos.pista(a), datos.setlist(a)
        datos.anadir(s, p, 1)
        conn.execute("DELETE FROM setlist WHERE id=?", (s,))
        assert n(conn, "setlist_pista") == 0 and n(conn, "pista") == 1

    def test_borrar_biblioteca_elimina_vinculos_pero_no_las_pistas(self, datos, conn):
        a = datos.dj()
        b, p = datos.biblioteca(a), datos.pista(a)
        datos.vincular(b, p)
        conn.execute("DELETE FROM biblioteca WHERE id=?", (b,))
        assert n(conn, "biblioteca_pista") == 0 and n(conn, "pista") == 1

    def test_restrict_impide_borrar_una_pista_usada_en_un_setlist(self, datos, conn):
        a = datos.dj()
        p, s = datos.pista(a), datos.setlist(a)
        datos.anadir(s, p, 1)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("DELETE FROM pista WHERE id=?", (p,))
        assert n(conn, "pista") == 1

    def test_pista_no_usada_se_puede_borrar_y_arrastra_sus_vinculos(self, datos, conn):
        a = datos.dj()
        b, p = datos.biblioteca(a), datos.pista(a)
        datos.vincular(b, p)
        conn.execute("DELETE FROM pista WHERE id=?", (p,))
        assert n(conn, "pista") == 0 and n(conn, "biblioteca_pista") == 0

    def test_borrar_un_dj_elimina_todo_su_arbol_sin_tocar_a_los_demas(self, datos, conn):
        """Comportamiento observado en SQLite 3.45.1: el CASCADE de setlist se resuelve antes
        que el RESTRICT de pista. Si falla en otra versión, hay que tratarlo como P-08."""
        a, b = datos.dj("a"), datos.dj("b")
        pa, pb = datos.pista(a, "/m/a.mp3"), datos.pista(b, "/m/b.mp3")
        datos.anadir(datos.setlist(a), pa, 1)
        datos.vincular(datos.biblioteca(a), pa)
        datos.anadir(datos.setlist(b), pb, 1)
        conn.execute("DELETE FROM dj WHERE id=?", (a,))
        assert n(conn, "dj") == 1 and n(conn, "pista") == 1 and n(conn, "setlist") == 1
        assert n(conn, "setlist_pista") == 1 and n(conn, "biblioteca_pista") == 0
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []


# ---------------------------------------------------------------------------------------
# Triggers de aislamiento entre cuentas (RNF-12) e inmutabilidad de dj_id
# ---------------------------------------------------------------------------------------
class TestTriggersAislamiento:
    def test_biblioteca_y_pista_de_distinto_dj_rechazadas(self, datos, conn):
        a, b = datos.dj("a"), datos.dj("b")
        bib_b, pista_a = datos.biblioteca(b, "/otra"), datos.pista(a)
        with pytest.raises(sqlite3.IntegrityError, match="DJ distintos"):
            datos.vincular(bib_b, pista_a)
        assert n(conn, "biblioteca_pista") == 0

    def test_biblioteca_y_pista_del_mismo_dj_aceptadas(self, datos):
        a = datos.dj()
        datos.vincular(datos.biblioteca(a), datos.pista(a))

    def test_setlist_y_pista_de_distinto_dj_rechazadas(self, datos, conn):
        a, b = datos.dj("a"), datos.dj("b")
        setlist_b, pista_a = datos.setlist(b), datos.pista(a)
        with pytest.raises(sqlite3.IntegrityError, match="DJ distintos"):
            datos.anadir(setlist_b, pista_a, 1)
        assert n(conn, "setlist_pista") == 0

    def test_setlist_y_pista_del_mismo_dj_aceptadas(self, datos):
        a = datos.dj()
        datos.anadir(datos.setlist(a), datos.pista(a), 1)

    def test_el_mismo_fichero_en_dos_cuentas_son_dos_pistas_aisladas(self, datos, conn):
        a, b = datos.dj("a"), datos.dj("b")
        pa, pb = datos.pista(a, "/musica/x.mp3"), datos.pista(b, "/musica/x.mp3")
        assert pa != pb
        setlist_b = datos.setlist(b)
        with pytest.raises(sqlite3.IntegrityError):
            datos.anadir(setlist_b, pa, 1)  # la pista de A no entra en el setlist de B
        datos.anadir(setlist_b, pb, 1)

    @pytest.mark.parametrize("tabla", ["pista", "biblioteca", "setlist"])
    def test_dj_id_inmutable(self, datos, conn, tabla):
        a, b = datos.dj("a"), datos.dj("b")
        fila = {"pista": lambda: datos.pista(a), "biblioteca": lambda: datos.biblioteca(a),
                "setlist": lambda: datos.setlist(a)}[tabla]()
        with pytest.raises(sqlite3.IntegrityError, match="no es modificable"):
            conn.execute(f"UPDATE {tabla} SET dj_id=? WHERE id=?", (b, fila))
        assert conn.execute(f"SELECT dj_id FROM {tabla} WHERE id=?", (fila,)).fetchone()[0] == a

    @pytest.mark.parametrize("tabla", ["pista", "biblioteca", "setlist"])
    def test_reasignar_el_mismo_dj_o_cambiar_otras_columnas_esta_permitido(self, datos, conn, tabla):
        a = datos.dj("a")
        fila = {"pista": lambda: datos.pista(a), "biblioteca": lambda: datos.biblioteca(a),
                "setlist": lambda: datos.setlist(a)}[tabla]()
        conn.execute(f"UPDATE {tabla} SET dj_id=? WHERE id=?", (a, fila))
        columna = {"pista": "titulo", "biblioteca": "nombre", "setlist": "nombre"}[tabla]
        conn.execute(f"UPDATE {tabla} SET {columna}='nuevo' WHERE id=?", (fila,))


# ---------------------------------------------------------------------------------------
# Ciclo de estados de la pista y actualización sin romper setlists
# ---------------------------------------------------------------------------------------
class TestEstadosDePista:
    def estado(self, conn, pid):
        return conn.execute("SELECT estado FROM pista WHERE id=?", (pid,)).fetchone()[0]

    def test_disponible_no_disponible_y_vuelta_conserva_los_descriptores(self, datos, conn):
        a = datos.dj()
        pid = datos.pista(a, bpm=126.5, tonalidad="Dm")
        conn.execute("UPDATE pista SET estado='no_disponible' WHERE id=? AND dj_id=? AND estado='disponible'", (pid, a))
        assert self.estado(conn, pid) == "no_disponible"
        conn.execute("UPDATE pista SET estado='disponible' WHERE id=? AND dj_id=? AND estado='no_disponible'", (pid, a))
        fila = conn.execute("SELECT estado, bpm, codigo_camelot FROM pista WHERE id=?", (pid,)).fetchone()
        assert (fila["estado"], fila["bpm"], fila["codigo_camelot"]) == ("disponible", 126.5, "7A")

    def test_disponible_pasa_a_fallida_si_el_reanalisis_falla(self, datos, conn):
        a = datos.dj()
        pid = datos.pista(a, "/m/x.mp3")
        conn.execute(UPSERT_PISTA, params_pista(a, "/m/x.mp3", estado="fallida", motivo="El motor no devolvió BPM",
                                                bpm=None, tonalidad=None, duracion=None, motor=None, fecha=None, mtime_ns=MTIME + 1))
        fila = conn.execute("SELECT id, estado, motivo_fallo, bpm FROM pista").fetchone()
        assert (fila["id"], fila["estado"], fila["bpm"]) == (pid, "fallida", None)
        assert fila["motivo_fallo"] == "El motor no devolvió BPM"

    def test_fallida_vuelve_a_disponible_solo_limpiando_el_motivo(self, datos, conn):
        a = datos.dj()
        pid = datos.pista_fallida(a, "/m/x.mp3")
        with pytest.raises(sqlite3.IntegrityError):  # quedarse con el motivo viola el CHECK
            conn.execute("UPDATE pista SET estado='disponible' WHERE id=?", (pid,))
        conn.execute(UPSERT_PISTA, params_pista(a, "/m/x.mp3", mtime_ns=MTIME + 5))  # reanálisis correcto
        fila = conn.execute("SELECT estado, motivo_fallo, bpm FROM pista WHERE id=?", (pid,)).fetchone()
        assert (fila["estado"], fila["motivo_fallo"], fila["bpm"]) == ("disponible", None, 124.0)

    def test_una_fallida_sin_descriptores_no_puede_pasar_a_no_disponible(self, datos, conn):
        """Regla de data-model.md sección 6: la fallida cuyo fichero desaparece sigue fallida."""
        a = datos.dj()
        pid = datos.pista_fallida(a)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("UPDATE pista SET estado='no_disponible', motivo_fallo=NULL WHERE id=?", (pid,))
        assert self.estado(conn, pid) == "fallida"

    def test_upsert_actualiza_sin_duplicar_y_conserva_id_y_vinculos(self, datos, conn):
        a = datos.dj()
        bib, pid = datos.biblioteca(a), datos.pista(a, "/m/x.mp3", bpm=120.0)
        sid = datos.setlist(a)
        datos.vincular(bib, pid)
        datos.anadir(sid, pid, 1)
        conn.execute(UPSERT_PISTA, params_pista(a, "/m/x.mp3", bpm=128.25, tamano=2000, mtime_ns=MTIME + 9))
        assert n(conn, "pista") == 1
        fila = conn.execute("SELECT id, bpm, tamano_bytes, fecha_modificacion_archivo FROM pista").fetchone()
        assert (fila["id"], fila["bpm"], fila["tamano_bytes"], fila["fecha_modificacion_archivo"]) == (pid, 128.25, 2000, MTIME + 9)
        assert n(conn, "biblioteca_pista") == 1 and n(conn, "setlist_pista") == 1

    def test_el_setlist_guardado_se_abre_con_el_estado_actual_de_sus_pistas(self, datos, conn):
        a = datos.dj()
        p1, p2 = datos.pista(a, "/m/1.mp3"), datos.pista(a, "/m/2.mp3")
        sid = datos.setlist(a)
        datos.anadir(sid, p1, 1)
        datos.anadir(sid, p2, 2)
        conn.execute("UPDATE pista SET estado='no_disponible' WHERE id=?", (p1,))
        conn.execute(UPSERT_PISTA, params_pista(a, "/m/2.mp3", estado="fallida", motivo="reanálisis fallido",
                                                bpm=None, tonalidad=None, duracion=None, motor=None, fecha=None, mtime_ns=MTIME + 1))
        filas = conn.execute("SELECT sp.orden, p.estado FROM setlist_pista sp JOIN pista p ON p.id = sp.pista_id"
                             " WHERE sp.setlist_id=? ORDER BY sp.orden", (sid,)).fetchall()
        assert [(f["orden"], f["estado"]) for f in filas] == [(1, "no_disponible"), (2, "fallida")]

    def test_insert_or_replace_rompe_el_vinculo_y_esta_prohibido(self, datos, conn):
        """REPLACE borra la fila conflictiva: con la pista en un setlist, RESTRICT lo impide.
        Por eso la aplicación usa siempre INSERT ... ON CONFLICT DO UPDATE."""
        a = datos.dj()
        pid = datos.pista(a, "/m/x.mp3")
        datos.anadir(datos.setlist(a), pid, 1)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT OR REPLACE INTO pista (dj_id, ruta_local, tamano_bytes, fecha_modificacion_archivo,"
                         " estado, duracion_seg, bpm, tonalidad, motor_mir, fecha_analisis)"
                         " VALUES (?, '/m/x.mp3', 1, 1, 'disponible', 100, 120, 'Am', 'm', 'f')", (a,))
        assert conn.execute("SELECT id FROM pista").fetchone()[0] == pid

    def test_insertar_o_ignorar_el_vinculo_no_duplica(self, datos, conn):
        a = datos.dj()
        b, p = datos.biblioteca(a), datos.pista(a)
        for _ in range(3):
            conn.execute("INSERT OR IGNORE INTO biblioteca_pista (biblioteca_id, pista_id) VALUES (?, ?)", (b, p))
        assert n(conn, "biblioteca_pista") == 1

    def test_un_fichero_movido_es_una_pista_nueva_y_la_antigua_queda_no_disponible(self, datos, conn):
        a = datos.dj()
        vieja = datos.pista(a, "/m/vieja.mp3")
        conn.execute("UPDATE pista SET estado='no_disponible' WHERE id=?", (vieja,))
        nueva = datos.pista(a, "/m/nueva.mp3")
        assert vieja != nueva and n(conn, "pista") == 2
        assert self.estado(conn, vieja) == "no_disponible" and self.estado(conn, nueva) == "disponible"


# ---------------------------------------------------------------------------------------
# Atomicidad (RNF-09): guardar un setlist reemplazando su contenido
# ---------------------------------------------------------------------------------------
class TestAtomicidad:
    def test_actualizar_un_setlist_es_todo_o_nada(self, datos, conn):
        a = datos.dj()
        p1, p2, p3 = (datos.pista(a, f"/m/{i}.mp3") for i in range(3))
        sid = datos.setlist(a)
        datos.anadir(sid, p1, 1)
        datos.anadir(sid, p2, 2)
        conn.execute("BEGIN")
        conn.execute("UPDATE setlist SET fecha_modificacion=? WHERE id=?", (DESPUES, sid))
        conn.execute("DELETE FROM setlist_pista WHERE setlist_id=?", (sid,))
        conn.execute("INSERT INTO setlist_pista VALUES (?, ?, 1)", (sid, p3))
        with pytest.raises(sqlite3.IntegrityError):  # orden duplicado a mitad de la transacción
            conn.execute("INSERT INTO setlist_pista VALUES (?, ?, 1)", (sid, p1))
        conn.execute("ROLLBACK")
        filas = conn.execute("SELECT pista_id, orden FROM setlist_pista WHERE setlist_id=? ORDER BY orden", (sid,)).fetchall()
        assert [(f["pista_id"], f["orden"]) for f in filas] == [(p1, 1), (p2, 2)]
        assert conn.execute("SELECT fecha_modificacion FROM setlist WHERE id=?", (sid,)).fetchone()[0] == AHORA

    def test_intercambiar_dos_posiciones_con_update_choca_con_unique_y_se_hace_con_delete_insert(self, datos, conn):
        """Motivo de P-06: el UPDATE fila a fila puede violar UNIQUE (setlist_id, orden)."""
        a = datos.dj()
        p1, p2 = datos.pista(a, "/m/1.mp3"), datos.pista(a, "/m/2.mp3")
        sid = datos.setlist(a)
        datos.anadir(sid, p1, 1)
        datos.anadir(sid, p2, 2)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("UPDATE setlist_pista SET orden = 3 - orden WHERE setlist_id=?", (sid,))
        conn.execute("BEGIN")
        conn.execute("DELETE FROM setlist_pista WHERE setlist_id=?", (sid,))
        conn.execute("INSERT INTO setlist_pista VALUES (?, ?, 1)", (sid, p2))
        conn.execute("INSERT INTO setlist_pista VALUES (?, ?, 2)", (sid, p1))
        conn.execute("COMMIT")
        filas = conn.execute("SELECT pista_id FROM setlist_pista WHERE setlist_id=? ORDER BY orden", (sid,)).fetchall()
        assert [f[0] for f in filas] == [p2, p1]
