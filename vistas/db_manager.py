import sqlite3
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "procrastination.db")

def conectar_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def crear_tablas():
    db = conectar_db()
    try:
        cursor = db.cursor()

        # --- TABLA USUARIOS ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre   TEXT NOT NULL CHECK(LENGTH(nombre) <= 80),
                correo   TEXT UNIQUE NOT NULL CHECK(
                             correo LIKE '%@%.%' AND
                             LENGTH(correo) >= 6
                         ),
                password TEXT NOT NULL
            )
        """)

        # --- TABLA ACTIVIDADES ---
        # fecha:       YYYY-MM-DD
        # hora_inicio: HH:MM (24h)
        # hora_fin:    HH:MM (24h)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS actividades (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_correo TEXT NOT NULL,
                categoria      TEXT NOT NULL CHECK(categoria IN ('Académica', 'Ocio')),
                nombre         TEXT NOT NULL,
                descripcion    TEXT,
                fecha          TEXT NOT NULL,
                hora_inicio    TEXT NOT NULL,
                hora_fin       TEXT NOT NULL,
                FOREIGN KEY (usuario_correo) REFERENCES usuarios(correo)
            )
        """)

        db.commit()
    finally:
        db.close()


# ──────────────────────────────────────────
#  VALIDACIONES
# ──────────────────────────────────────────

def validar_nombre(nombre: str):
    if not (0 < len(nombre.strip()) <= 80):
        return False, "El nombre no puede estar vacío ni superar 80 caracteres."
    if any(c.isdigit() for c in nombre):
        return False, "El nombre no puede contener números."
    return True, ""


def validar_correo(correo: str) -> bool:
    patron = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    return bool(re.match(patron, correo))


# ──────────────────────────────────────────
#  FUNCIONES DE USUARIOS
# ──────────────────────────────────────────

def registrar_usuario_db(nombre, correo, password):
    valido, mensaje = validar_nombre(nombre)
    if not valido:
        return False, mensaje
    if not validar_correo(correo):
        return False, "El correo no tiene un formato válido."

    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, password) VALUES (?, ?, ?)",
            (nombre.strip(), correo.strip(), password)
        )
        db.commit()
        return True, "Registro exitoso."
    except sqlite3.IntegrityError:
        return False, "Este correo ya está registrado."
    except Exception as e:
        print(f"Error al registrar: {e}")
        return False, "Error inesperado al registrar."
    finally:
        db.close()


def validar_usuario_db(correo, password):
    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            "SELECT nombre, correo FROM usuarios WHERE correo=? AND password=?",
            (correo, password)
        )
        return cursor.fetchone()
    finally:
        db.close()


def actualizar_usuario_db(correo_actual, nuevo_nombre=None, nuevo_correo=None, nueva_pass=None):
    if nuevo_nombre:
        valido, mensaje = validar_nombre(nuevo_nombre)
        if not valido:
            return False, mensaje
    if nuevo_correo and not validar_correo(nuevo_correo):
        return False, "El nuevo correo no tiene un formato válido."

    db = conectar_db()
    try:
        cursor = db.cursor()
        if nuevo_nombre:
            cursor.execute(
                "UPDATE usuarios SET nombre = ? WHERE correo = ?",
                (nuevo_nombre.strip(), correo_actual)
            )
        if nuevo_correo:
            cursor.execute(
                "UPDATE usuarios SET correo = ? WHERE correo = ?",
                (nuevo_correo.strip(), correo_actual)
            )
            cursor.execute(
                "UPDATE actividades SET usuario_correo = ? WHERE usuario_correo = ?",
                (nuevo_correo.strip(), correo_actual)
            )
            correo_actual = nuevo_correo
        if nueva_pass:
            cursor.execute(
                "UPDATE usuarios SET password = ? WHERE correo = ?",
                (nueva_pass, correo_actual)
            )
        db.commit()
        return True, "Actualización exitosa."
    except sqlite3.IntegrityError:
        return False, "Ese correo ya está en uso por otra cuenta."
    except Exception as e:
        print(f"Error al actualizar: {e}")
        return False, "Error inesperado al actualizar."
    finally:
        db.close()


# ──────────────────────────────────────────
#  FUNCIONES DE ACTIVIDADES
# ──────────────────────────────────────────

def agregar_actividad_db(usuario_correo, categoria, nombre, fecha, hora_inicio, hora_fin, descripcion=""):
    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO actividades (usuario_correo, categoria, nombre, descripcion, fecha, hora_inicio, hora_fin)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (usuario_correo, categoria, nombre, descripcion, fecha, hora_inicio, hora_fin))
        db.commit()
        return True
    except Exception as e:
        print(f"Error al agregar actividad: {e}")
        return False
    finally:
        db.close()


def obtener_actividades_db(usuario_correo):
    """Todas las actividades del usuario, ordenadas por fecha y hora."""
    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id, categoria, nombre, descripcion, fecha, hora_inicio, hora_fin
            FROM actividades
            WHERE usuario_correo = ?
            ORDER BY fecha DESC, hora_inicio ASC
        """, (usuario_correo,))
        return cursor.fetchall()
    finally:
        db.close()


def obtener_actividades_por_fecha_db(usuario_correo, fecha):
    """Actividades de un día específico (fecha: 'YYYY-MM-DD')."""
    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id, categoria, nombre, descripcion, fecha, hora_inicio, hora_fin
            FROM actividades
            WHERE usuario_correo = ? AND fecha = ?
            ORDER BY hora_inicio ASC
        """, (usuario_correo, fecha))
        return cursor.fetchall()
    finally:
        db.close()

def obtener_actividades_por_rango_db(usuario_correo, fecha_inicio, fecha_fin):
    """Actividades entre dos fechas (formato 'YYYY-MM-DD')."""
    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id, categoria, nombre, descripcion, fecha, hora_inicio, hora_fin
            FROM actividades
            WHERE usuario_correo = ? AND fecha BETWEEN ? AND ?
            ORDER BY fecha DESC, hora_inicio ASC
        """, (usuario_correo, fecha_inicio, fecha_fin))
        return cursor.fetchall()
    finally:
        db.close()

def eliminar_actividad_db(actividad_id):
    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM actividades WHERE id = ?", (actividad_id,))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al eliminar actividad: {e}")
        return False
    finally:
        db.close()


def actualizar_actividad_db(actividad_id, categoria=None, nombre=None, descripcion=None,
                             fecha=None, hora_inicio=None, hora_fin=None):
    db = conectar_db()
    try:
        cursor = db.cursor()
        campos = []
        valores = []
        if categoria:               campos.append("categoria = ?");     valores.append(categoria)
        if nombre:                  campos.append("nombre = ?");         valores.append(nombre)
        if descripcion is not None: campos.append("descripcion = ?");   valores.append(descripcion)
        if fecha:                   campos.append("fecha = ?");          valores.append(fecha)
        if hora_inicio:             campos.append("hora_inicio = ?");    valores.append(hora_inicio)
        if hora_fin:                campos.append("hora_fin = ?");       valores.append(hora_fin)

        if not campos:
            return False

        valores.append(actividad_id)
        cursor.execute(f"UPDATE actividades SET {', '.join(campos)} WHERE id = ?", valores)
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al actualizar actividad: {e}")
        return False
    finally:
        db.close()


def limpiar_datos():
    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM actividades")
        cursor.execute("DELETE FROM usuarios")
        cursor.execute("DELETE FROM sqlite_sequence")  # resetea los IDs autoincrement
        db.commit()
        print("Datos eliminados correctamente.")
    finally:
        db.close()