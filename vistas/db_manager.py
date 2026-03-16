import sqlite3

def conectar_db():
    # Crea el archivo local 'procrastination.db'
    return sqlite3.connect("procrastination.db", check_same_thread=False)

def crear_tablas():
    db = conectar_db()
    cursor = db.cursor()
    # Creamos la tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    db.commit()
    db.close()

def registrar_usuario_db(nombre, correo, password):
    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, password) VALUES (?, ?, ?)",
            (nombre, correo, password)
        )
        db.commit()
        db.close()
        return True
    except sqlite3.IntegrityError:
        return False # El correo ya existe

def validar_usuario_db(correo, password):
    db = conectar_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE correo = ? AND password = ?",
        (correo, password)
    )
    usuario = cursor.fetchone()
    db.close()
    return usuario is not None