import flet as ft

def registro(page: ft.Page):
    page.bgcolor = ft.Colors.BLACK
    page.title = "Procrastination't - Registro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    #Tarjeta blanca
    registro_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.PERSON_ADD_ALT_1_ROUNDED, color=ft.Colors.BLUE_600, size=60),

                ft.Text("Registro", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),

                ft.Container(height=5),

                ft.TextField(
                    label="Nombre completo",
                    text_size=14,
                    label_style=ft.TextStyle(size=12),
                    prefix_icon=ft.Icons.PERSON_OUTLINE,
                    border_radius=10,
                    height=45,
                    bgcolor=ft.Colors.WHITE
                ),

                ft.TextField(
                    label="Correo electrónico",
                    text_size=14,
                    label_style=ft.TextStyle(size=12),
                    prefix_icon=ft.Icons.EMAIL_OUTLINED,
                    border_radius=10,
                    height=45,
                    bgcolor=ft.Colors.WHITE
                ),

                ft.TextField(
                    label="Contraseña",
                    text_size=14,
                    label_style=ft.TextStyle(size=12),
                    prefix_icon=ft.Icons.LOCK_OUTLINE,
                    password=True,
                    can_reveal_password=True,
                    border_radius=10,
                    height=45,
                    bgcolor=ft.Colors.WHITE
                ),

                ft.Container(height=5),

                ft.FilledButton(
                    content=ft.Text("Registrarse", size=14),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_600,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    width=float("inf"),
                    height=45
                ),

                ft.Container(height=5),

                ft.Row(
                    controls=[
                        ft.Text("¿Ya tienes una cuenta?", size=12),
                        ft.TextButton(
                            content=ft.Text("Inicia sesión", size=12, color=ft.Colors.BLUE_600)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            tight=True
        ),
        bgcolor=ft.Colors.WHITE,
        padding=15,
        width=450,
        border_radius=20,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.BLACK_12,
            spread_radius=1
        )
    )

    celular = ft.Container(
        content=registro_card,
        image=ft.DecorationImage(
            src="2.jpg",
            fit=ft.BoxFit.COVER
        ),
        width=320,
        height=650,
        border_radius=40,
        alignment=ft.Alignment.CENTER,
        padding=20,
        border=ft.Border.all(2, ft.Colors.GREY_900)
    )

    page.add(celular)
    page.window.maximized = True
    page.update()

if __name__ == "__main__":
    ft.run(registro)