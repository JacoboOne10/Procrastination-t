import flet as ft
from vistas.db_manager import validar_usuario_db
from vistas.notis import mostrar_snackbar


def obtener_vista_login(page, on_login, ir_a_registro, ir_a_recuperar):
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
                content_padding=ft.Padding(top=10, bottom=10, left=10, right=10),
            ),
            bgcolor=color_fondo_tf,
            border_radius=15,
            padding=ft.Padding(left=10, right=10),
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 4)
            )
        )

    campo_correo = crear_campo_sombra("Correo electrónico", ft.Icons.PERSON)
    campo_pass = crear_campo_sombra("Contraseña", ft.Icons.LOCK_OUTLINE, is_password=True)

    def intentar_login(e):
        correo = campo_correo.content.value
        contrasena = campo_pass.content.value

        datos_usuario = validar_usuario_db(correo, contrasena)

        if datos_usuario:
            on_login(datos_usuario)
        else:
            mostrar_snackbar(page, "❌ Credenciales incorrectas", ft.Colors.RED_700)

    btn_login = ft.Container(
        content=ft.Text("Iniciar sesión", size=14, weight="bold", color=color_boton_texto),
        bgcolor=color_primario,
        border_radius=15,
        height=55,
        alignment=ft.Alignment(0, 0),
        on_click=intentar_login,
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
                    src="logo.png", width=120, height=120, fit="contain"
                ),

                ft.Text("Procrastination't", size=26, weight="bold", color=color_primario),
                ft.Container(height=15),

                campo_correo,
                campo_pass,
                ft.Container(height=10),

                btn_login,

                ft.Row([
                    ft.Text("¿No tienes una cuenta?", size=12, color=color_texto_oscuro),
                    ft.TextButton(
                        "Regístrate",
                        on_click=ir_a_registro,
                        style=ft.ButtonStyle(color=color_primario)
                    )
                ], alignment="center"),

                ft.TextButton(
                    "¿Olvidaste tu contraseña?",
                    icon=ft.Icons.LOCK_RESET_ROUNDED,
                    on_click=ir_a_recuperar,
                    style=ft.ButtonStyle(color=color_primario)
                ),

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
        page.title = "Previsualización Login"

        def mock_login(datos): print(f"Login exitoso: {datos}")
        def mock_registro(e): print("Navegando a Registro...")
        def mock_recuperar(e): print("Navegando a Recuperar...")

        celular_test = ft.Container(
            expand=True,
            image=ft.DecorationImage(src="/5.jpg", fit="cover"),
            content=obtener_vista_login(page, mock_login, mock_registro, mock_recuperar)
        )

        page.add(celular_test)
        page.update()

    ft.run(test_main, assets_dir="../images")