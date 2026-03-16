import flet as ft
from vistas.db_manager import registrar_usuario_db

def obtener_vista_registro(page, volver_a_login):
    # --- CONFIGURACIÓN DE ESTILO ---
    color_primario = ft.Colors.BLUE_800
    color_texto_oscuro = ft.Colors.BLACK
    color_boton_texto = ft.Colors.WHITE
    color_borde_tf = ft.Colors.BLUE_100
    color_fondo_tf = ft.Colors.WHITE

    # Campos de texto usando las variables de estilo
    nombre_tf = ft.TextField(
        label="Nombre completo",
        prefix_icon=ft.Icons.FACE,
        border_radius=10,
        bgcolor=color_fondo_tf,
        color=color_texto_oscuro,
        border_color=color_borde_tf
    )
    correo_tf = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.Icons.EMAIL,
        border_radius=10,
        bgcolor=color_fondo_tf,
        color=color_texto_oscuro,
        border_color=color_borde_tf
    )
    pass_tf = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        border_radius=10,
        bgcolor=color_fondo_tf,
        color=color_texto_oscuro,
        border_color=color_borde_tf
    )

    def realizar_registro(e):
        if not nombre_tf.value or not correo_tf.value or not pass_tf.value:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Todos los campos son obligatorios"), bgcolor=ft.Colors.ORANGE_700)
            page.snack_bar.open = True
            page.update()
            return

        exito = registrar_usuario_db(nombre_tf.value, correo_tf.value, pass_tf.value)

        if exito:
            page.snack_bar = ft.SnackBar(
                ft.Text("✅ ¡Usuario registrado! Ya puedes entrar"),
                bgcolor=ft.Colors.GREEN_700
            )
            page.snack_bar.open = True
            page.update()
            volver_a_login(None)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Error: El correo ya existe"), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(expand=True),

                ft.Image(
                    src="/logo.png", width=120, height=120, fit="contain"
                ),

                ft.Text("Crear cuenta", size=22, weight="bold", color=color_primario),
                ft.Container(height=10),

                nombre_tf,
                correo_tf,
                pass_tf,

                ft.FilledButton(
                    content=ft.Text("Registrarse", size=14, weight="bold", color=color_boton_texto),
                    style=ft.ButtonStyle(
                        bgcolor=color_primario,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    width=400, height=45,
                    on_click=realizar_registro
                ),

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
            horizontal_alignment="center",
            spacing=15
        ),
        padding=20,
        expand=True
    )

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
            padding=ft.Padding(top=40, left=15, right=15, bottom=15),
            content=obtener_vista_registro(page, mock_volver)
        )

        page.add(celular_test)
        page.update()

    ft.run(test_main, assets_dir="../images")