import flet as ft
from vistas.db_manager import crear_tablas, conectar_db
from vistas.login import obtener_vista_login
from vistas.registro import obtener_vista_registro
from vistas.inicio import obtener_vista_inicio
from vistas.perfil import obtener_vista_perfil
from vistas.modificar_datos import obtener_vista_modificar
from vistas.estadisticas import obtener_vista_estadisticas
from vistas.cambiar_contraseña  import obtener_vista_recuperar


def main(page: ft.Page):
    crear_tablas()
    sesion_actual = {"nombre": "", "correo": ""}

    # --- CONFIGURACIÓN DE PÁGINA ---
    page.window.width = 380
    page.window.height = 720
    page.window.resizable = False
    page.padding = 0
    page.margin = 0
    page.title = "Procrastination't"

    contenido_celular = ft.Container(expand=True)

    # --- 1. FUNCIONES DE AYUDA ---
    def crear_item_dock(icon_name, selected_icon_name, index, seleccionado=False):
        icono = selected_icon_name if seleccionado else icon_name
        return ft.Container(
            content=ft.Column([
                ft.Icon(icono, color=ft.Colors.BLUE_900, size=28),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            on_click=lambda _: cambiar_pestana_manual(index),
        )

    # --- 2. FUNCIONES DE NAVEGACIÓN ---
    def cerrar_sesion(e):
        ir_a_login()

    def ir_a_login(e=None):
        contenido_celular.content = obtener_vista_login(page, entrar_a_app, ir_a_registro, ir_a_recuperar)
        capa_dock.visible = False
        page.update()

    def ir_a_registro(e=None):
        contenido_celular.content = obtener_vista_registro(page, ir_a_login)
        capa_dock.visible = False
        page.update()

    def ir_a_recuperar(e=None):
        contenido_celular.content = obtener_vista_recuperar(page, ir_a_login)
        capa_dock.visible = False
        page.update()

    def entrar_a_app(datos):
        sesion_actual["nombre"] = datos[0]
        sesion_actual["correo"] = datos[1]
        cambiar_pestana_manual(0)
        capa_dock.visible = True
        page.update()

    def ir_a_modificar_datos(e=None):
        capa_dock.visible = False

        def volver_y_actualizar(nuevo_nombre=None, nuevo_correo=None):
            if nuevo_correo:
                sesion_actual["correo"] = nuevo_correo
            if nuevo_nombre:
                sesion_actual["nombre"] = nuevo_nombre
            capa_dock.visible = True
            cambiar_pestana_manual(2)
            page.update()

        contenido_celular.content = obtener_vista_modificar(
            page,
            sesion_actual["nombre"],
            sesion_actual["correo"],
            al_finalizar=volver_y_actualizar
        )
        page.update()

    def confirmar_borrar_cuenta(e):
        def hacer_borrar(e):
            dialog.open = False
            page.update()
            db = conectar_db()
            try:
                cursor = db.cursor()
                cursor.execute(
                    "DELETE FROM actividades WHERE usuario_correo = ?",
                    (sesion_actual["correo"],)
                )
                cursor.execute(
                    "DELETE FROM usuarios WHERE correo = ?",
                    (sesion_actual["correo"],)
                )
                db.commit()
            finally:
                db.close()
            ir_a_login()

        def cancelar(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            bgcolor=ft.Colors.WHITE,
            title=ft.Text("Borrar cuenta", color=ft.Colors.BLACK),
            content=ft.Text(
                "¿Estás seguro? Se eliminarán tu cuenta y todas tus actividades. "
                "Esta acción no se puede deshacer.",
                color=ft.Colors.BLACK
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar,
                              style=ft.ButtonStyle(color=ft.Colors.BLUE_900)),
                ft.TextButton("Borrar", on_click=hacer_borrar,
                              style=ft.ButtonStyle(color=ft.Colors.RED_700)),
            ]
        )

        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def cambiar_pestana_manual(indice):
        iconos_base = [ft.Icons.HOME_OUTLINED, ft.Icons.INSERT_CHART_OUTLINED, ft.Icons.PERSON_OUTLINE]
        iconos_solid = [ft.Icons.HOME, ft.Icons.INSERT_CHART, ft.Icons.PERSON]

        for i, item in enumerate(capa_dock.content.controls):
            item.content.controls[0].icon = iconos_solid[i] if i == indice else iconos_base[i]

        if indice == 0:
            contenido_celular.content = obtener_vista_inicio(page, sesion_actual["correo"])
        elif indice == 1:
            contenido_celular.content = obtener_vista_estadisticas(page, sesion_actual["correo"])
        elif indice == 2:
            contenido_celular.content = obtener_vista_perfil(
                cerrar_sesion,
                ir_a_modificar_datos,
                confirmar_borrar_cuenta,
                nombre=sesion_actual["nombre"],
                correo=sesion_actual["correo"]
            )
        page.update()

    # --- 3. COMPONENTES ---
    capa_dock = ft.Container(
        content=ft.Row([
            crear_item_dock(ft.Icons.HOME_OUTLINED, ft.Icons.HOME, 0, seleccionado=True),
            crear_item_dock(ft.Icons.INSERT_CHART_OUTLINED, ft.Icons.INSERT_CHART, 1),
            crear_item_dock(ft.Icons.PERSON_OUTLINE, ft.Icons.PERSON, 2),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND, spacing=0),
        bgcolor=ft.Colors.WHITE,
        height=70,
        visible=False,
        border=ft.Border(top=ft.BorderSide(1, ft.Colors.BLUE_GREY_50)),
    )

    celular = ft.Container(
        expand=True,
        image=ft.DecorationImage(src="/5.jpg", fit="cover"),
        content=ft.Column([
            ft.Container(
                content=contenido_celular,
                expand=True,
                padding=ft.Padding(left=20, right=20, top=20, bottom=5)
            ),
            capa_dock
        ], spacing=0)
    )

    page.add(celular)
    ir_a_login()


if __name__ == "__main__":
    ft.run(main, assets_dir="images")