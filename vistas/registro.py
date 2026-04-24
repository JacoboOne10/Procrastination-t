import flet as ft
from vistas.db_manager import registrar_usuario_db
from vistas.notis import mostrar_snackbar


def obtener_vista_registro(page, volver_a_login):
    color_primario = ft.Colors.BLUE_800
    color_texto_oscuro = ft.Colors.BLACK
    color_boton_texto = ft.Colors.WHITE
    color_fondo_tf = ft.Colors.WHITE

    def crear_campo_sombra(label, icon, is_password=False):
        return ft.Container(
            content=ft.TextField(
                label=label,
                prefix_icon=icon,
                password=is_password,
                can_reveal_password=is_password,
                border=ft.InputBorder.NONE,
                bgcolor=ft.Colors.TRANSPARENT,
                color=color_texto_oscuro,
                content_padding=ft.Padding.only(top=10, bottom=10, left=10, right=10),
            ),
            bgcolor=color_fondo_tf,
            border_radius=15,
            padding=ft.Padding.only(left=10, right=10),
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 4)
            )
        )

    campo_nombre = crear_campo_sombra("Nombre completo", ft.Icons.FACE)
    campo_correo = crear_campo_sombra("Correo electrónico", ft.Icons.EMAIL)
    campo_pass = crear_campo_sombra("Contraseña", ft.Icons.LOCK_OUTLINE, is_password=True)

    def realizar_registro(e):
        nombre = campo_nombre.content.value
        correo = campo_correo.content.value
        contrasena = campo_pass.content.value

        if not nombre or not correo or not contrasena:
            mostrar_snackbar(page, "⚠️ Todos los campos son obligatorios", ft.Colors.ORANGE_700)
            return

        exito, mensaje = registrar_usuario_db(nombre, correo, contrasena)

        if exito:
            mostrar_snackbar(page, "✅ ¡Usuario registrado! Ya puedes entrar", ft.Colors.GREEN_700)
            volver_a_login(None)
        else:
            mostrar_snackbar(page, f"❌ {mensaje}", ft.Colors.RED_700)

    btn_registro = ft.Container(
        content=ft.Text("Registrarse", size=14, weight="bold", color=color_boton_texto),
        bgcolor=color_primario,
        border_radius=15,
        height=55,
        alignment=ft.Alignment(0, 0),
        on_click=realizar_registro,
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(expand=True),

                ft.Image(
                    src="/logo.png", width=120, height=120, fit="contain"
                ),

                ft.Text("Crear cuenta", size=26, weight="bold", color=color_primario),
                ft.Container(height=10),

                campo_nombre,
                campo_correo,
                campo_pass,
                ft.Container(height=10),

                btn_registro,

                ft.Row([
                    ft.Text("¿Ya tienes una cuenta?", size=12, color=color_texto_oscuro),
                    ft.TextButton(
                        "Iniciar sesión",
                        on_click=volver_a_login,
                        style=ft.ButtonStyle(color=color_primario)
                    ),
                ], alignment="center"),

                ft.Container(expand=True),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=20,
        expand=True
    )


# --- Bloque de prueba ---
if __name__ == "__main__":
    def test_main(page: ft.Page):
        page.window.width = 380
        page.window.height = 720
        page.window.resizable = False
        page.padding = 0
        page.title = "Previsualización Registro"
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"

        def mock_volver(e): print("Cambiando a Login...")

        celular_test = ft.Container(
            expand=True,
            image=ft.DecorationImage(src="/5.jpg", fit="cover"),
            content=obtener_vista_registro(page, mock_volver)
        )

        page.add(celular_test)
        page.update()

    ft.run(test_main, assets_dir="../images")