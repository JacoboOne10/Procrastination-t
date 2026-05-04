from db_manager import conectar_db, crear_tablas, registrar_usuario_db
from datetime import date, timedelta


def correr_seeder():
    crear_tablas()

    # ── USUARIO DE PRUEBA ──
    exito, msg = registrar_usuario_db("Pruebas", "pruebas@123.com", "123")
    if not exito:
        print(f"Usuario ya existe o error: {msg}")
    else:
        print("Usuario creado: pruebas@123.com / 123")

    # ── ACTIVIDADES ──
    actividades = [
        # (categoria, nombre, descripcion, dias_atras, hora_inicio, hora_fin)
        ("Académica", "Estudiar para examen de cálculo", "Repasar integrales y derivadas", 0, "09:00", "11:30"),
        ("Ocio", "Ver Netflix", "Serie Breaking Bad temporada 2", 0, "20:00", "22:00"),
        ("Académica", "Tarea de programación", "Implementar árbol binario en Python", 1, "14:00", "16:30"),
        ("Ocio", "Gaming", "Minecraft", 1, "19:00", "21:00"),
        ("Académica", "Lectura de artículo científico", "Paper sobre redes neuronales", 2, "10:00", "11:00"),
        ("Ocio", "Redes sociales", "Instagram y TikTok", 2, "21:00", "22:30"),
        ("Académica", "Estudiar inglés", "Vocabulario y gramática avanzada", 3, "08:00", "09:30"),
        ("Ocio", "Gaming", "Fortnite", 3, "18:00", "20:30"),
        ("Académica", "Exposición", "Preparar diapositivas", 4, "13:00", "15:00"),
        ("Ocio", "YouTube", "Videos de tecnología", 4, "20:00", "21:30"),
        ("Ocio", "Gaming", "FIFA", 6, "19:30", "21:00"),
        ("Académica", "Tarea de estadística", "Ejercicios de regresión lineal", 8, "14:00", "16:00"),
        ("Ocio", "Ver película", "Interestelar", 8, "21:00", "23:30"),
        ("Académica", "Estudio grupal", "Matemáticas con compañeros", 10, "09:00", "12:00"),
        ("Ocio", "Redes sociales", "Twitter", 10, "22:00", "23:00"),
        ("Académica", "Examen de programación", "Bases de datos", 15, "08:00", "10:00"),
        ("Académica", "Proyecto de base de datos", "Diagrama ER y normalización", 20, "13:00", "16:30"),
        ("Académica", "Estudiar para parcial", "Repaso general de todas las materias", 22, "08:00", "12:00"),
    ]

    hoy = date.today()
    db = conectar_db()
    try:
        cursor = db.cursor()
        for cat, nombre, desc, dias_atras, h_ini, h_fin in actividades:
            fecha = (hoy - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
            cursor.execute("""
                INSERT INTO actividades (usuario_correo, categoria, nombre, descripcion, fecha, hora_inicio, hora_fin)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ("pruebas@123.com", cat, nombre, desc, fecha, h_ini, h_fin))
        db.commit()
        print(f"✅ {len(actividades)} actividades insertadas correctamente.")
    except Exception as e:
        print(f"❌ Error al insertar actividades: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    correr_seeder()