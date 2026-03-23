import flet as ft
from vistas.db_manager import actualizar_usuario_db


def obtener_vista_modificar(page, nombre_actual, correo_actual, al_finalizar):
    color_oficial = ft.Colors.BLUE_800
    color_titulo = ft.Colors.BLUE_900

    # Diccionario "Escudo": Guarda lo que REALMENTE está en la DB
    # Esto evita que el perfil se actualice con datos que dieron error (ej. correo duplicado)
    datos_reales = {
        "nombre": nombre_actual,
        "correo": correo_actual
    }

    def crear_fila_editable(label, valor_inicial, es_password=False):
        tf = ft.TextField(
            value=valor_inicial,
            label=label,
            password=es_password,
            can_reveal_password=es_password,
            read_only=True,
            border=ft.InputBorder.UNDERLINE,
            border_color=color_titulo,
            color=ft.Colors.BLACK,
            expand=True
        )

        btn = ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, icon_color=color_oficial)

        def click_editar(e):
            if btn.icon == ft.Icons.EDIT_OUTLINED:
                # Cambiar a modo edición
                tf.read_only = False
                tf.focused_border_color = color_oficial
                btn.icon = ft.Icons.CHECK_ROUNDED
                btn.icon_color = ft.Colors.GREEN_700
                tf.focus()
            else:
                # Intentar guardar en Base de Datos
                nuevo_val = tf.value.strip()
                exito = False

                # Siempre usamos datos_reales["correo"] como ID para la DB
                if label == "Nombre":
                    exito = actualizar_usuario_db(datos_reales["correo"], nuevo_nombre=nuevo_val)
                    if exito: datos_reales["nombre"] = nuevo_val
                elif label == "Correo":
                    exito = actualizar_usuario_db(datos_reales["correo"], nuevo_correo=nuevo_val)
                    if exito: datos_reales["correo"] = nuevo_val
                elif label == "Contraseña":
                    exito = actualizar_usuario_db(datos_reales["correo"], nueva_pass=nuevo_val)

                if exito:
                    tf.read_only = True
                    btn.icon = ft.Icons.EDIT_OUTLINED
                    btn.icon_color = color_oficial
                    page.overlay.append(ft.SnackBar(ft.Text(f"✅ {label} actualizado correctamente")))
                else:
                    # Si falló (ej. correo duplicado), revertimos el texto al valor real de la DB
                    tf.value = datos_reales["nombre"] if label == "Nombre" else datos_reales["correo"]
                    if label == "Contraseña": tf.value = ""

                    page.overlay.append(ft.SnackBar(ft.Text(f"❌ Error: No se pudo actualizar el {label}")))

                page.overlay[-1].open = True
            page.update()

        btn.on_click = click_editar
        return ft.Row([tf, btn], alignment=ft.MainAxisAlignment.CENTER)

    # Creamos las filas
    fila_nombre = crear_fila_editable("Nombre", nombre_actual)
    fila_correo = crear_fila_editable("Correo", correo_actual)
    fila_pass = crear_fila_editable("Contraseña", "", es_password=True)

    return ft.Container(
        content=ft.Column([
            ft.Container(height=10),

            # Título centrado
            ft.Container(
                content=ft.Text("Editar Perfil", size=26, weight="bold", color=color_titulo),
                alignment=ft.Alignment(0, 0),
                width=float("inf")
            ),

            ft.Container(height=30),

            fila_nombre,
            fila_correo,
            fila_pass,

            ft.Container(expand=True),

            # Botón Finalizar
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.DONE_ALL, color=color_oficial),
                    title=ft.Text("Finalizar", color=color_oficial, weight="bold"),
                    # MANDAMOS LOS DATOS REALES (los que pasaron la validación de la DB)
                    on_click=lambda _: al_finalizar(datos_reales["nombre"], datos_reales["correo"])
                ),
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                height=55,
                shadow=ft.BoxShadow(
                    blur_radius=5,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
                )
            ),
            ft.Container(height=10)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        expand=True,
        bgcolor=ft.Colors.TRANSPARENT
    )


# --- Bloque de prueba ---
if __name__ == "__main__":
    def test_main(page: ft.Page):
        page.window.width = 380
        page.window.height = 720
        page.window.resizable = False
        page.padding = 0
        page.margin = 0
        page.title = "Prueba Modificar"

        def mock_finalizar(n, c):
            print(f"Regresando con: {n}, {c}")

        celular_test = ft.Container(
            expand=True,
            image=ft.DecorationImage(src="/5.jpg", fit="cover"),
            content=obtener_vista_modificar(page, "Prueba", "correo@test.com", mock_finalizar)
        )
        page.add(celular_test)


    ft.run(test_main, assets_dir="../images")