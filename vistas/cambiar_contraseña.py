import flet as ft
from vistas.db_manager import validar_usuario_db, actualizar_usuario_db
from vistas.notis import mostrar_snackbar
from vistas.enviar_email import generar_codigo, enviar_codigo_verificacion


def obtener_vista_recuperar(page, volver_a_login):
    color_primario = ft.Colors.BLUE_800
    color_texto_oscuro = ft.Colors.BLACK
    color_boton_texto = ft.Colors.WHITE
    color_fondo_tf = ft.Colors.WHITE

    estado = {"codigo": "", "correo": ""}

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

    # ── CAMPOS ──
    campo_correo = crear_campo_sombra("Correo electrónico", ft.Icons.EMAIL)
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
    campo_nueva_pass = crear_campo_sombra("Nueva contraseña", ft.Icons.LOCK_OUTLINE, is_password=True)
    campo_confirmar_pass = crear_campo_sombra("Confirmar contraseña", ft.Icons.LOCK_OUTLINE, is_password=True)

    contenedor = ft.Container(expand=True)

    # ── VISTA 1: INGRESAR CORREO ──
    btn_enviar = ft.Container(
        content=ft.Text("Enviar código", size=14, weight="bold", color=color_boton_texto),
        bgcolor=color_primario,
        border_radius=15,
        height=55,
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
    )

    vista_correo = ft.Container(
        content=ft.Column([
            ft.Container(expand=True),
            ft.Icon(ft.Icons.LOCK_RESET_ROUNDED, size=70, color=color_primario),
            ft.Text("Recuperar contraseña", size=22, weight="bold", color=color_primario),
            ft.Text(
                "Ingresa tu correo y te enviaremos\nun código para restablecer tu contraseña.",
                size=13, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=10),
            campo_correo,
            ft.Container(height=10),
            btn_enviar,
            ft.TextButton(
                "Volver al inicio de sesión",
                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                on_click=volver_a_login,
                style=ft.ButtonStyle(color=ft.Colors.GREY_500)
            ),
            ft.Container(expand=True),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        padding=20,
        expand=True
    )

    # ── VISTA 2: VERIFICAR CÓDIGO ──
    txt_correo_enviado = ft.Text(
        "", size=13, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER
    )

    btn_verificar = ft.Container(
        content=ft.Text("Verificar código", size=14, weight="bold", color=color_boton_texto),
        bgcolor=color_primario,
        border_radius=15,
        height=55,
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
    )

    vista_codigo = ft.Container(
        content=ft.Column([
            ft.Container(expand=True),
            ft.Icon(ft.Icons.MARK_EMAIL_UNREAD_ROUNDED, size=70, color=color_primario),
            ft.Text("Verifica tu correo", size=22, weight="bold", color=color_primario),
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
                "Volver",
                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                on_click=lambda e: ir_a_vista_correo(),
                style=ft.ButtonStyle(color=ft.Colors.GREY_500)
            ),
            ft.Container(expand=True),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        padding=20,
        expand=True
    )

    # ── VISTA 3: NUEVA CONTRASEÑA ──
    btn_cambiar = ft.Container(
        content=ft.Text("Cambiar contraseña", size=14, weight="bold", color=color_boton_texto),
        bgcolor=color_primario,
        border_radius=15,
        height=55,
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
    )

    vista_nueva_pass = ft.Container(
        content=ft.Column([
            ft.Container(expand=True),
            ft.Icon(ft.Icons.LOCK_ROUNDED, size=70, color=color_primario),
            ft.Text("Nueva contraseña", size=22, weight="bold", color=color_primario),
            ft.Text(
                "Elige una nueva contraseña segura.",
                size=13, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=10),
            campo_nueva_pass,
            campo_confirmar_pass,
            ft.Container(height=10),
            btn_cambiar,
            ft.Container(expand=True),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        padding=20,
        expand=True
    )

    # ── FUNCIONES DE NAVEGACIÓN ──
    def ir_a_vista_correo():
        contenedor.content = vista_correo
        page.update()

    def ir_a_vista_codigo():
        contenedor.content = vista_codigo
        page.update()

    def ir_a_vista_nueva_pass():
        contenedor.content = vista_nueva_pass
        page.update()

    # ── LÓGICA ──
    def enviar_codigo(e):
        correo = campo_correo.content.value.strip()
        if not correo:
            mostrar_snackbar(page, "⚠️ Ingresa tu correo", ft.Colors.ORANGE_700)
            return

        # Verificar que el correo existe en la DB
        from vistas.db_manager import conectar_db
        db = conectar_db()
        try:
            cursor = db.cursor()
            cursor.execute("SELECT correo FROM usuarios WHERE correo = ?", (correo,))
            resultado = cursor.fetchone()
        finally:
            db.close()

        if not resultado:
            mostrar_snackbar(page, "❌ No existe una cuenta con ese correo", ft.Colors.RED_700)
            return

        codigo = generar_codigo()
        estado["codigo"] = codigo
        estado["correo"] = correo

        btn_enviar.bgcolor = ft.Colors.GREY_400
        btn_enviar.content.value = "Enviando..."
        page.update()

        exito = enviar_codigo_verificacion(correo, codigo)

        btn_enviar.bgcolor = color_primario
        btn_enviar.content.value = "Enviar código"
        page.update()

        if exito:
            txt_correo_enviado.value = f"Enviamos un código de 6 dígitos a\n{correo}"
            campo_codigo.content.value = ""
            ir_a_vista_codigo()
        else:
            mostrar_snackbar(page, "❌ Error al enviar el correo", ft.Colors.RED_700)

    def verificar_codigo(e):
        codigo_ingresado = campo_codigo.content.value.strip()
        if not codigo_ingresado:
            mostrar_snackbar(page, "⚠️ Ingresa el código", ft.Colors.ORANGE_700)
            return
        if codigo_ingresado != estado["codigo"]:
            mostrar_snackbar(page, "❌ Código incorrecto", ft.Colors.RED_700)
            return
        campo_nueva_pass.content.value = ""
        campo_confirmar_pass.content.value = ""
        ir_a_vista_nueva_pass()

    def reenviar_codigo(e):
        nuevo_codigo = generar_codigo()
        estado["codigo"] = nuevo_codigo
        exito = enviar_codigo_verificacion(estado["correo"], nuevo_codigo)
        if exito:
            mostrar_snackbar(page, "✅ Nuevo código enviado", ft.Colors.GREEN_700)
        else:
            mostrar_snackbar(page, "❌ Error al reenviar", ft.Colors.RED_700)

    def cambiar_password(e):
        nueva = campo_nueva_pass.content.value.strip()
        confirmar = campo_confirmar_pass.content.value.strip()

        if len(nueva) < 8:
            mostrar_snackbar(page, "⚠️ La contraseña debe tener al menos 8 caracteres", ft.Colors.ORANGE_700)
            return

        if not nueva or not confirmar:
            mostrar_snackbar(page, "⚠️ Completa ambos campos", ft.Colors.ORANGE_700)
            return
        if nueva != confirmar:
            mostrar_snackbar(page, "❌ Las contraseñas no coinciden", ft.Colors.RED_700)
            return
        if len(nueva) < 6:
            mostrar_snackbar(page, "⚠️ La contraseña debe tener al menos 6 caracteres", ft.Colors.ORANGE_700)
            return

        exito, mensaje = actualizar_usuario_db(estado["correo"], nueva_pass=nueva)
        if exito:
            mostrar_snackbar(page, "✅ Contraseña actualizada correctamente", ft.Colors.GREEN_700)
            volver_a_login(None)
        else:
            mostrar_snackbar(page, f"❌ {mensaje}", ft.Colors.RED_700)

    btn_enviar.on_click = enviar_codigo
    btn_verificar.on_click = verificar_codigo
    btn_cambiar.on_click = cambiar_password

    contenedor.content = vista_correo
    return contenedor


# --- Bloque de prueba ---
if __name__ == "__main__":
    def test_main(page: ft.Page):
        page.window.width = 380
        page.window.height = 720
        page.window.resizable = False
        page.padding = 0
        page.title = "Prueba Recuperar Contraseña"

        def mock_volver(e): print("Volviendo al login...")

        celular_test = ft.Container(
            expand=True,
            image=ft.DecorationImage(src="/5.jpg", fit="cover"),
            content=obtener_vista_recuperar(page, mock_volver)
        )
        page.add(celular_test)
        page.update()

    ft.run(test_main, assets_dir="../images")