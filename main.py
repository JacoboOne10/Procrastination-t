import flet as ft
from vistas.db_manager import crear_tablas
from vistas.login import obtener_vista_login
from vistas.registro import obtener_vista_registro
from vistas.inicio import obtener_vista_inicio
from vistas.perfil import obtener_vista_perfil


def main(page: ft.Page):
    crear_tablas()

    # --- AJUSTES DE VENTANA (Tamaño Celular) ---
    page.window.width = 380  # Un poco más ancho que el contenedor del celular
    page.window.height = 720  # Un poco más alto que el contenedor del celular
    page.window.resizable = False  # Evita que se deforme el diseño
    page.padding = 0  # Quitamos márgenes para que el celular llene la ventana
    page.title = "Procrastination't"

    # Centrado
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    contenido_celular = ft.Container(expand=True)

    # --- FUNCIONES DE NAVEGACIÓN ---
    def ir_a_login(e=None):
        contenido_celular.content = obtener_vista_login(page, entrar_a_app, ir_a_registro)
        capa_dock.visible = False
        page.update()

    def ir_a_registro(e=None):
        contenido_celular.content = obtener_vista_registro(page, ir_a_login)
        capa_dock.visible = False
        page.update()

    def entrar_a_app(e):
        contenido_celular.content = obtener_vista_inicio(page)
        capa_dock.visible = True
        page.update()

    def cerrar_sesion(e):
        ir_a_login()

    def cambiar_pestana(ev):
        indice = ev.control.selected_index
        if indice == 0:
            contenido_celular.content = obtener_vista_inicio(page)
        elif indice == 1:
            contenido_celular.content = obtener_vista_perfil(cerrar_sesion)
        page.update()

    # --- COMPONENTES ---
    dock = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_ROUNDED),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_ROUNDED),
        ],
        on_change=cambiar_pestana,
        bgcolor=ft.Colors.WHITE,
        height=70,
    )

    capa_dock = ft.Container(content=dock, border_radius=20, clip_behavior=ft.ClipBehavior.HARD_EDGE, visible=False)

    # --- EL MARCO DEL CELULAR (Ahora ajustado a la ventana) ---
    celular = ft.Container(
        expand=True,
        image=ft.DecorationImage(src="/5.jpg", fit="cover"),
        padding=ft.Padding(top=40, left=15, right=15, bottom=15),
        content=ft.Column(
            controls=[
                ft.Container(content=contenido_celular, expand=True),
                capa_dock
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    page.add(celular)
    ir_a_login()


if __name__ == "__main__":
    ft.run(main, assets_dir="images")