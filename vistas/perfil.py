import flet as ft

def obtener_vista_perfil(on_logout, ir_a_modificar, on_borrar, nombre="Usuario", correo="correo@ejemplo.com"):
    # --- 1. DEFINIR COLORES ---
    color_titulo = ft.Colors.BLUE_900
    color_texto = ft.Colors.BLACK
    color_iconos = ft.Colors.BLUE_700
    color_labels = ft.Colors.BLUE_GREY_400
    color_logout = ft.Colors.RED_600

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=10),
                ft.CircleAvatar(
                    content=ft.Icon(ft.Icons.PERSON, size=40, color=color_titulo),
                    radius=45,
                    bgcolor=ft.Colors.BLUE_100
                ),
                ft.Text("Mi Perfil", size=24, weight="bold", color=color_titulo),

                ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.BADGE_ROUNDED, color=color_iconos),
                            title=ft.Text("Nombre", size=11, color=color_labels),
                            subtitle=ft.Text(nombre, size=15, color=color_texto, weight="w500"),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.EMAIL_ROUNDED, color=color_iconos),
                            title=ft.Text("Correo Electrónico", size=11, color=color_labels),
                            subtitle=ft.Text(correo, size=15, color=color_texto, weight="w500"),
                        ),
                    ], spacing=0),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    padding=5,
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
                ),

                ft.Container(expand=True),

                # --- BOTÓN MODIFICAR DATOS (AHORA CON CLICK) ---
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.EDIT_ROUNDED, color=color_iconos),
                        title=ft.Text("Modificar Datos", color=color_iconos, weight="bold"),
                        on_click=ir_a_modificar # <--- Acción conectada
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    height=55,
                    shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK))
                ),

                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.DELETE_FOREVER_ROUNDED, color=color_logout),
                        title=ft.Text("Borrar Cuenta", color=color_logout, weight="bold"),
                        on_click=on_borrar
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    height=55,
                    shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK))
                ),

                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOGOUT_ROUNDED, color=color_logout),
                        title=ft.Text("Cerrar Sesión", color=color_logout, weight="bold"),
                        on_click=on_logout
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    height=55,
                    shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK))
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True
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
            # Pasamos datos de prueba para ver cómo se ve
            content=obtener_vista_perfil(mock_logout, lambda e: None, lambda e: None, "Prueba","prueba@prueba.com")        )

        page.add(celular_test)
        page.update()


    ft.run(test_main, assets_dir="../images")