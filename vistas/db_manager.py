import sqlite3


def conectar_db():
    # check_same_thread=False permite que Flet use la DB desde distintos hilos
    return sqlite3.connect("procrastination.db", check_same_thread=False)


def crear_tablas():
    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS usuarios
                       (
                           id       INTEGER PRIMARY KEY AUTOINCREMENT,
                           nombre   TEXT,
                           correo   TEXT UNIQUE NOT NULL,
                           password TEXT        NOT NULL
                       )
                       """)
        db.commit()
    finally:
        db.close()


def registrar_usuario_db(nombre, correo, password):
    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, password) VALUES (?, ?, ?)",
            (nombre, correo, password)
        )
        db.commit()
        return True
    except (sqlite3.IntegrityError, sqlite3.OperationalError) as e:
        print(f"Error al registrar: {e}")
        return False
    finally:
        db.close()


def validar_usuario_db(correo, password):
    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT nombre, correo FROM usuarios WHERE correo=? AND password=?", (correo, password))
        usuario = cursor.fetchone()
        return usuario
    finally:
        db.close()


def actualizar_usuario_db(correo_actual, nuevo_nombre=None, nuevo_correo=None, nueva_pass=None):
    db = conectar_db()  # Solo UNA conexión
    try:
        cursor = db.cursor()

        # 1. Actualizar Nombre
        if nuevo_nombre:
            cursor.execute("UPDATE usuarios SET nombre = ? WHERE correo = ?", (nuevo_nombre, correo_actual))

        # 2. Actualizar Correo (Si cambia, actualizamos correo_actual para la siguiente query)
        if nuevo_correo:
            cursor.execute("UPDATE usuarios SET correo = ? WHERE correo = ?", (nuevo_correo, correo_actual))
            correo_actual = nuevo_correo

        # 3. Actualizar Contraseña
        if nueva_pass:
            cursor.execute("UPDATE usuarios SET password = ? WHERE correo = ?", (nueva_pass, correo_actual))

        db.commit()
        return db.total_changes > 0
    except Exception as e:
        print(f"Error al actualizar: {e}")
        return False
    finally:
        # Esto libera el archivo SIEMPRE
        db.close()