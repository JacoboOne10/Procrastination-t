import flet as ft


def obtener_vista_perfil(on_logout):
    # Colores para fondo blanco
    color_titulo = ft.Colors.BLUE_900
    color_texto = ft.Colors.BLACK
    color_iconos = ft.Colors.BLUE_700

    return ft.Column(
        controls=[
            ft.Container(height=40),

            # Avatar
            ft.CircleAvatar(
                content=ft.Icon(ft.Icons.PERSON, size=40, color=color_titulo),
                radius=50,
                bgcolor=ft.Colors.BLUE_100
            ),

            ft.Text("Mi Perfil", size=26, weight="bold", color=color_titulo),
            ft.Container(height=20),

            # SECCIÓN DE DATOS DEL USUARIO
            ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BADGE_ROUNDED, color=color_iconos),
                        title=ft.Text("Nombre", size=12, color=ft.Colors.BLUE_GREY_400),
                        subtitle=ft.Text("Usuario de Prueba", size=16, color=color_texto, weight="w500"),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.EMAIL_ROUNDED, color=color_iconos),
                        title=ft.Text("Correo Electrónico", size=12, color=ft.Colors.BLUE_GREY_400),
                        subtitle=ft.Text("usuario@ejemplo.com", size=16, color=color_texto, weight="w500"),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=color_iconos),
                        title=ft.Text("Institución", size=12, color=ft.Colors.BLUE_GREY_400),
                        subtitle=ft.Text("Universidad de Guadalajara", size=16, color=color_texto, weight="w500"),
                    ),
                ], spacing=0),
                bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLUE_GREY_50),
                border_radius=20,
                padding=10,
                border=ft.border.all(1, ft.Colors.BLUE_GREY_100)
            ),

            ft.Container(height=20),

            # BOTÓN DE CERRAR SESIÓN
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOGOUT_ROUNDED, color=ft.Colors.RED_400),
                    title=ft.Text("Cerrar Sesión", color=ft.Colors.RED_400, weight="bold"),
                    on_click=on_logout
                ),
                bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.RED_50),
                border_radius=20,
                padding=5,
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


# --- BLOQUE DE PRUEBA ---
if __name__ == "__main__":
    def test_main(page: ft.Page):
        page.window.width = 380
        page.window.height = 720
        page.window.resizable = False
        page.padding = 0
        page.title = "Previsualización Perfil Directo"
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"

        def mock_logout(e): print("Cerrando sesión...")

        celular_test = ft.Container(
            expand=True,
            image=ft.DecorationImage(src="/5.jpg", fit="cover"),
            padding=ft.Padding(top=40, left=20, right=20, bottom=20),
            content=obtener_vista_perfil(mock_logout)
        )

        page.add(celular_test)
        page.update()


    ft.run(test_main, assets_dir="../images")