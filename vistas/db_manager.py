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
    db = conectar_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, password) VALUES (?, ?, ?)",
            (nombre, correo, password)
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.OperationalError as e:
        print(f"Error de base de datos bloqueada: {e}")
        return False
    finally:
        # ESTO ES LO MÁS IMPORTANTE:
        # Cerramos la conexión siempre para liberar el archivo .db
        db.close()


def validar_usuario_db(correo, password):
    conn = sqlite3.connect("procrastination.db")
    cursor = conn.cursor()
    # Buscamos el nombre y el correo
    cursor.execute("SELECT nombre, correo FROM usuarios WHERE correo=? AND password=?", (correo, password))
    usuario = cursor.fetchone()
    conn.close()

    # Si existe, devuelve una tupla (Nombre, Correo), si no, devuelve None
    return usuario