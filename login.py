import flet as ft

def login(page: ft.Page):
    page.bgcolor = ft.Colors.BLACK
    page.title = "Procrastination't - Login"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    #Tarjeta blanca
    login_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.LOCK_PERSON_ROUNDED, color=ft.Colors.BLUE_600, size=60),

                ft.Text("Iniciar sesión", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),

                ft.Container(height=5),

                ft.TextField(
                    label="Correo electrónico",
                    text_size=14,
                    label_style=ft.TextStyle(size=12),
                    prefix_icon=ft.Icons.PERSON,
                    border_radius=10,
                    height=50,
                    bgcolor=ft.Colors.WHITE
                ),

                ft.TextField(
                    label="Contraseña",
                    text_size=14,
                    label_style=ft.TextStyle(size=12),
                    prefix_icon=ft.Icons.LOCK,
                    password=True,
                    can_reveal_password=True,
                    border_radius=10,
                    height=50,
                    bgcolor=ft.Colors.WHITE
                ),

                ft.Container(height=5),

                ft.FilledButton(
                    content=ft.Text("Iniciar sesión",size=14),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_600,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    width=400,
                    height=45
                ),

                ft.Container(height=5),

                ft.Row(
                    controls=[
                        ft.Text("¿No tienes una cuenta?", size=12),
                        ft.TextButton(
                            content=ft.Text("Regístrate", size=12, color=ft.Colors.BLUE_600)
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
        content=login_card,
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
    ft.run(login)