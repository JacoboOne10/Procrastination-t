import flet as ft
from db_manager import registrar_usuario_db
from vistas.notis import mostrar_snackbar
from enviar_email import generar_codigo, enviar_codigo_verificacion


def obtener_vista_registro(page, volver_a_login):
    color_primario = ft.Colors.BLUE_800
    color_texto_oscuro = ft.Colors.BLACK
    color_boton_texto = ft.Colors.WHITE
    color_fondo_tf = ft.Colors.WHITE

    # Estado temporal del registro
    datos_pendientes = {
        "nombre": "",
        "correo": "",
        "password": "",
        "codigo": ""
    }

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

    # ── CAMPO DE CÓDIGO ──
    campo_codigo = ft.Container(
        content=ft.TextField(
            label="Código de verificación",
            prefix_icon=ft.Icons.VERIFIED_ROUNDED,
            border=ft.InputBorder.NONE,
            bgcolor=ft.Colors.TRANSPARENT,
            color=color_texto_oscuro,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=6,
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

    contenedor = ft.Container(expand=True)

    # ── VISTA FORMULARIO ──
    btn_registro = ft.Container(
        content=ft.Text("Registrarse", size=14, weight="bold", color=color_boton_texto),
        bgcolor=color_primario,
        border_radius=15,
        height=55,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: realizar_registro(e),
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
    )

    vista_formulario = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(expand=True),
                ft.Image(src="/logo.png", width=120, height=120, fit="contain"),
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

    # ── VISTA VERIFICACIÓN ──
    txt_correo_enviado = ft.Text(
        "",
        size=13,
        color=ft.Colors.GREY_600,
        text_align=ft.TextAlign.CENTER
    )

    btn_verificar = ft.Container(
        content=ft.Text("Verificar código", size=14, weight="bold", color=color_boton_texto),
        bgcolor=color_primario,
        border_radius=15,
        height=55,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: verificar_codigo(e),
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
    )

    vista_verificacion = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(expand=True),

                ft.Icon(ft.Icons.MARK_EMAIL_UNREAD_ROUNDED, size=70, color=color_primario),
                ft.Text("Verifica tu correo", size=24, weight="bold", color=color_primario),
                ft.Container(height=5),
                txt_correo_enviado,
                ft.Container(height=10),

                campo_codigo,
                ft.Container(height=10),

                btn_verificar,

                ft.TextButton(
                    "Reenviar código",
                    icon=ft.Icons.REFRESH_ROUNDED,
                    on_click=lambda e: reenviar_codigo(e),
                    style=ft.ButtonStyle(color=color_primario)
                ),

                ft.TextButton(
                    "Volver al registro",
                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                    on_click=lambda e: ir_a_formulario(),
                    style=ft.ButtonStyle(color=ft.Colors.GREY_500)
                ),

                ft.Container(expand=True),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=20,
        expand=True
    )

    # ── FUNCIONES ──
    def ir_a_formulario():
        contenedor.content = vista_formulario
        page.update()

    def ir_a_verificacion():
        contenedor.content = vista_verificacion
        page.update()

    def realizar_registro(e):
        nombre = campo_nombre.content.value.strip()
        correo = campo_correo.content.value.strip()
        contrasena = campo_pass.content.value

        if not nombre or not correo or not contrasena:
            mostrar_snackbar(page, "⚠️ Todos los campos son obligatorios", ft.Colors.ORANGE_700)
            return

        # Validaciones previas antes de enviar el correo
        from db_manager import validar_nombre, validar_correo
        valido, mensaje = validar_nombre(nombre)
        if not valido:
            mostrar_snackbar(page, f"❌ {mensaje}", ft.Colors.RED_700)
            return
        if not validar_correo(correo):
            mostrar_snackbar(page, "❌ El correo no tiene un formato válido.", ft.Colors.RED_700)
            return

        if len(contrasena) < 8:
            mostrar_snackbar(page, "⚠️ La contraseña debe tener al menos 8 caracteres", ft.Colors.ORANGE_700)
            return

        # Generar y enviar código
        codigo = generar_codigo()
        datos_pendientes["nombre"] = nombre
        datos_pendientes["correo"] = correo
        datos_pendientes["password"] = contrasena
        datos_pendientes["codigo"] = codigo

        btn_registro.bgcolor = ft.Colors.GREY_400
        btn_registro.content.value = "Enviando..."
        page.update()

        exito = enviar_codigo_verificacion(correo, codigo)

        btn_registro.bgcolor = color_primario
        btn_registro.content.value = "Registrarse"
        page.update()

        if exito:
            txt_correo_enviado.value = f"Enviamos un código de 6 dígitos a\n{correo}"
            campo_codigo.content.value = ""
            ir_a_verificacion()
        else:
            mostrar_snackbar(page, "❌ No se pudo enviar el correo. Verifica que sea válido.", ft.Colors.RED_700)

    def verificar_codigo(e):
        codigo_ingresado = campo_codigo.content.value.strip()

        if not codigo_ingresado:
            mostrar_snackbar(page, "⚠️ Ingresa el código de verificación", ft.Colors.ORANGE_700)
            return

        if codigo_ingresado != datos_pendientes["codigo"]:
            mostrar_snackbar(page, "❌ Código incorrecto, intenta de nuevo", ft.Colors.RED_700)
            return

        # Código correcto — registrar usuario
        exito, mensaje = registrar_usuario_db(
            datos_pendientes["nombre"],
            datos_pendientes["correo"],
            datos_pendientes["password"]
        )

        if exito:
            mostrar_snackbar(page, "✅ ¡Cuenta verificada! Ya puedes iniciar sesión", ft.Colors.GREEN_700)
            volver_a_login(None)
        else:
            mostrar_snackbar(page, f"❌ {mensaje}", ft.Colors.RED_700)
            ir_a_formulario()

    def reenviar_codigo(e):
        nuevo_codigo = generar_codigo()
        datos_pendientes["codigo"] = nuevo_codigo
        exito = enviar_codigo_verificacion(datos_pendientes["correo"], nuevo_codigo)
        if exito:
            mostrar_snackbar(page, "✅ Nuevo código enviado", ft.Colors.GREEN_700)
        else:
            mostrar_snackbar(page, "❌ Error al reenviar el código", ft.Colors.RED_700)

    # Iniciar con el formulario
    contenedor.content = vista_formulario
    return contenedor


# --- Bloque de prueba ---
if __name__ == "__main__":
    def test_main(page: ft.Page):
        page.window.width = 380
        page.window.height = 720
        page.window.resizable = False
        page.padding = 0
        page.title = "Previsualización Registro"

        def mock_volver(e): print("Cambiando a Login...")

        celular_test = ft.Container(
            expand=True,
            image=ft.DecorationImage(src="/bg.jpg", fit="cover"),
            content=obtener_vista_registro(page, mock_volver)
        )
        page.add(celular_test)
        page.update()

    ft.run(test_main, assets_dir="../images")