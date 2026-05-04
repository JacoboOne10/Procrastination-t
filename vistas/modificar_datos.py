import flet as ft
from db_manager import actualizar_usuario_db
from vistas.notis import mostrar_snackbar


def obtener_vista_modificar(page, nombre_actual, correo_actual, al_finalizar):
    color_oficial = ft.Colors.BLUE_800
    color_titulo = ft.Colors.BLUE_900

    def crear_campo(label, valor_inicial, es_password=False):
        return ft.Container(
            content=ft.TextField(
                value=valor_inicial,
                label=label,
                password=es_password,
                can_reveal_password=es_password,
                border=ft.InputBorder.NONE,
                bgcolor=ft.Colors.TRANSPARENT,
                color=ft.Colors.BLACK,
                content_padding=ft.Padding.only(top=10, bottom=10, left=10, right=10),
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=ft.Padding.only(left=10, right=10),
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 4)
            )
        )

    campo_nombre = crear_campo("Nombre", nombre_actual)
    campo_pass = crear_campo("Nueva contraseña (opcional)", "", es_password=True)

    def guardar_cambios(e):
        nuevo_nombre = campo_nombre.content.value.strip()
        nueva_pass = campo_pass.content.value.strip()

        nombre_cambio = nuevo_nombre if nuevo_nombre != nombre_actual else None
        pass_cambio = nueva_pass if nueva_pass else None

        if nueva_pass and len(nueva_pass) < 8:
            mostrar_snackbar(page, "⚠️ La contraseña debe tener al menos 8 caracteres", ft.Colors.ORANGE_700)
            return

        if not nombre_cambio and not pass_cambio:
            mostrar_snackbar(page, "⚠️ No hay cambios que guardar", ft.Colors.ORANGE_700)
            return

        exito, mensaje = actualizar_usuario_db(
            correo_actual,
            nuevo_nombre=nombre_cambio,
            nueva_pass=pass_cambio
        )

        if exito:
            mostrar_snackbar(page, "✅ Datos actualizados correctamente", ft.Colors.GREEN_700)
            al_finalizar(
                nuevo_nombre if nombre_cambio else nombre_actual,
                correo_actual
            )
        else:
            mostrar_snackbar(page, f"❌ {mensaje}", ft.Colors.RED_700)

    btn_finalizar = ft.Container(
        content=ft.Text("Guardar cambios", size=14, weight="bold", color=ft.Colors.WHITE),
        bgcolor=color_oficial,
        border_radius=15,
        height=55,
        alignment=ft.Alignment(0, 0),
        on_click=guardar_cambios,
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
    )

    return ft.Container(
        content=ft.Column([

            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                    icon_color=color_titulo,
                    on_click=lambda _: al_finalizar(nombre_actual, correo_actual)
                )
            ], alignment=ft.MainAxisAlignment.START),

            ft.Container(
                content=ft.Text("Editar Perfil", size=26, weight="bold", color=color_titulo),
                alignment=ft.Alignment(0, 0),
                width=float("inf")
            ),

            ft.Container(height=20),

            campo_nombre,
            campo_pass,

            ft.Container(expand=True),

            btn_finalizar,

            ft.Container(height=10)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        padding=ft.Padding.only(left=5, right=20, top=10, bottom=20),
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
            image=ft.DecorationImage(src="/bg.jpg", fit="cover"),
            content=obtener_vista_modificar(page, "Juan Pérez", "correo@test.com", mock_finalizar)
        )
        page.add(celular_test)

    ft.run(test_main, assets_dir="../images")