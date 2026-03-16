import flet as ft


def obtener_vista_inicio(page):
    return ft.Column(
        controls=[
            ft.Container(height=10),
            # Título de la pestaña
            ft.Text("Nueva Actividad", size=24, weight="bold", color=ft.Colors.BLUE_900),
            ft.Text("¿Qué registrarás ahora?", size=14, color=ft.Colors.GREY_700),

            ft.Container(height=20),

            # BOTÓN: ACTIVIDAD ACADÉMICA
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=ft.Colors.BLUE_600, size=35),
                    ft.Column([
                        ft.Text("Académica", weight="bold", size=16, color=ft.Colors.BLUE_900),
                        ft.Text("Tareas, estudio, proyectos...", size=12, color=ft.Colors.GREY_600),
                    ], spacing=2)
                ], alignment=ft.MainAxisAlignment.START),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=15,
                border=ft.Border.all(1, ft.Colors.BLUE_200),
                on_click=lambda _: print("Abrir formulario Académico"),
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK_12)
            ),

            ft.Container(height=10),

            # BOTÓN: ACTIVIDAD DE OCIO
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CELEBRATION_ROUNDED, color=ft.Colors.ORANGE_600, size=35),
                    ft.Column([
                        ft.Text("Ocio y Recreación", weight="bold", size=16, color=ft.Colors.BLUE_900),
                        ft.Text("Gaming, redes sociales, descanso...", size=12, color=ft.Colors.GREY_600),
                    ], spacing=2)
                ], alignment=ft.MainAxisAlignment.START),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=15,
                border=ft.Border.all(1, ft.Colors.ORANGE_200),
                on_click=lambda _: print("Abrir formulario Ocio"),
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK_12)
            ),

            ft.Container(height=30),

            # Recordatorio motivacional
            ft.Container(
                content=ft.Text(
                    "\"El secreto de salir adelante es comenzar.\"",
                    italic=True,
                    size=12,
                    color=ft.Colors.BLUE_GREY_400,
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.Alignment.CENTER
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )