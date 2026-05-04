import flet as ft
import random
from db_manager import agregar_actividad_db
from vistas.notis import mostrar_snackbar


def obtener_vista_inicio(page, correo_usuario):
    color_azul = ft.Colors.BLUE_900
    color_naranja = ft.Colors.ORANGE_600

    frases = [
        "\"El secreto de salir adelante es comenzar.\"",
        "\"No cuentes los días, haz que los días cuenten.\"",
        "\"El tiempo que disfrutas perder no es tiempo perdido.\"",
        "\"Pequeños pasos cada día llevan a grandes resultados.\"",
        "\"La disciplina es elegir entre lo que quieres ahora y lo que más quieres.\"",
        "\"Enfócate en el progreso, no en la perfección.\""
    ]

    estado = {
        "categoria": "",
        "fecha": "",
        "hora_inicio": "",
        "hora_fin": "",
    }

    txt_fecha = ft.Text("Seleccionar fecha", color=ft.Colors.GREY_600, size=13)
    txt_hora_inicio = ft.Text("Seleccionar hora", color=ft.Colors.GREY_600, size=13, text_align=ft.TextAlign.CENTER)
    txt_hora_fin = ft.Text("Seleccionar hora", color=ft.Colors.GREY_600, size=13, text_align=ft.TextAlign.CENTER)

    campo_nombre = ft.Container(
        content=ft.TextField(
            label="Nombre de la actividad",
            prefix_icon=ft.Icons.EDIT_NOTE_ROUNDED,
            border=ft.InputBorder.NONE,
            bgcolor=ft.Colors.TRANSPARENT,
            color=ft.Colors.BLACK,
            content_padding=ft.Padding.only(top=10, bottom=10, left=10, right=10),
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        padding=ft.Padding.only(left=10, right=10),
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), offset=ft.Offset(0, 4))
    )

    campo_descripcion = ft.Container(
        content=ft.TextField(
            label="Descripción (opcional)",
            prefix_icon=ft.Icons.NOTES_ROUNDED,
            border=ft.InputBorder.NONE,
            bgcolor=ft.Colors.TRANSPARENT,
            color=ft.Colors.BLACK,
            multiline=True,
            max_lines=3,
            content_padding=ft.Padding.only(top=10, bottom=10, left=10, right=10),
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        padding=ft.Padding.only(left=10, right=10),
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), offset=ft.Offset(0, 4))
    )

    def al_cambiar_fecha(e):
        if e.control.value:
            estado["fecha"] = e.control.value.strftime("%Y-%m-%d")
            txt_fecha.value = e.control.value.strftime("%d/%m/%Y")
            page.update()

    def al_cambiar_hora_inicio(e):
        if e.control.value:
            estado["hora_inicio"] = f"{e.control.value.hour:02d}:{e.control.value.minute:02d}"
            txt_hora_inicio.value = estado["hora_inicio"]
            page.update()

    def al_cambiar_hora_fin(e):
        if e.control.value:
            estado["hora_fin"] = f"{e.control.value.hour:02d}:{e.control.value.minute:02d}"
            txt_hora_fin.value = estado["hora_fin"]
            page.update()

    date_picker = ft.DatePicker(on_change=al_cambiar_fecha)
    time_picker_inicio = ft.TimePicker(on_change=al_cambiar_hora_inicio)
    time_picker_fin = ft.TimePicker(on_change=al_cambiar_hora_fin)

    page.overlay.extend([date_picker, time_picker_inicio, time_picker_fin])
    page.update()

    def abrir_fecha(e):
        date_picker.open = True
        page.update()

    def abrir_hora_inicio(e):
        time_picker_inicio.open = True
        page.update()

    def abrir_hora_fin(e):
        time_picker_fin.open = True
        page.update()

    def crear_boton_picker(icono, texto_ref, on_click):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icono, color=color_azul, size=20),
                texto_ref
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=ft.Padding.only(left=15, right=15, top=15, bottom=15),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), offset=ft.Offset(0, 4)),
            on_click=on_click,
            expand=True,
            alignment=ft.Alignment(0, 0)
        )

    vista_principal = ft.Column(
        controls=[
            ft.Container(height=10),
            ft.Text("Nueva Actividad", size=24, weight="bold", color=color_azul),
            ft.Text("¿Qué registrarás ahora?", size=14, color=ft.Colors.GREY_700),
            ft.Container(height=20),

            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=ft.Colors.BLUE_900, size=35),
                    ft.Column([
                        ft.Text("Académica", weight="bold", size=16, color=color_azul),
                        ft.Text("Tareas, estudio, proyectos...", size=12, color=ft.Colors.GREY_600),
                    ], spacing=2)
                ], alignment=ft.MainAxisAlignment.START),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=15,
                border=ft.Border.all(1, ft.Colors.BLUE_200),
                on_click=lambda _: abrir_formulario("Académica"),
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK_12)
            ),

            ft.Container(height=10),

            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CELEBRATION_ROUNDED, color=color_naranja, size=35),
                    ft.Column([
                        ft.Text("Ocio y Recreación", weight="bold", size=16, color=color_naranja),
                        ft.Text("Gaming, redes sociales, descanso...", size=12, color=ft.Colors.GREY_600),
                    ], spacing=2)
                ], alignment=ft.MainAxisAlignment.START),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=15,
                border=ft.Border.all(1, ft.Colors.ORANGE_200),
                on_click=lambda _: abrir_formulario("Ocio"),
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK_12)
            ),

            ft.Container(height=30),

            ft.Container(
                content=ft.Text(
                    random.choice(frases),
                    italic=True,
                    size=12,
                    color=ft.Colors.BLUE_GREY_400,
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.Alignment(0, 0)
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    titulo_formulario = ft.Text("", size=22, weight="bold", color=color_azul)
    icono_formulario = ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=ft.Colors.BLUE_900, size=28)

    btn_guardar = ft.Container(
        content=ft.Text("Guardar actividad", size=14, weight="bold", color=ft.Colors.WHITE),
        bgcolor=color_azul,
        border_radius=15,
        height=55,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: guardar_actividad(e),
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK), offset=ft.Offset(0, 4))
    )

    vista_formulario = ft.Column(
        controls=[
            # Parte scrollable
            ft.Column(
                controls=[
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                            icon_color=color_azul,
                            on_click=lambda _: volver_principal()
                        )
                    ], alignment=ft.MainAxisAlignment.START),

                    ft.Row([icono_formulario, titulo_formulario], spacing=10),

                    ft.Container(height=5),

                    campo_nombre,
                    campo_descripcion,

                    crear_boton_picker(ft.Icons.CALENDAR_MONTH_ROUNDED, txt_fecha, abrir_fecha),

                    ft.Row([
                        ft.Container(
                            content=crear_boton_picker(ft.Icons.ACCESS_TIME_ROUNDED, txt_hora_inicio, abrir_hora_inicio),
                            expand=True
                        ),
                        ft.Container(width=10),
                        ft.Container(
                            content=crear_boton_picker(ft.Icons.TIMER_OFF_ROUNDED, txt_hora_fin, abrir_hora_fin),
                            expand=True
                        ),
                    ]),
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),

            # Botón siempre visible abajo
            btn_guardar,
            ft.Container(height=10)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        expand=True
    )

    contenedor = ft.Container(
        content=vista_principal,
        expand=True
    )

    def abrir_formulario(categoria):
        estado["categoria"] = categoria
        estado["fecha"] = ""
        estado["hora_inicio"] = ""
        estado["hora_fin"] = ""
        campo_nombre.content.value = ""
        campo_descripcion.content.value = ""
        txt_fecha.value = "Seleccionar fecha"
        txt_hora_inicio.value = "Seleccionar hora"
        txt_hora_fin.value = "Seleccionar hora"

        titulo_formulario.value = categoria
        if categoria == "Académica":
            icono_formulario.icon = ft.Icons.SCHOOL_ROUNDED
            icono_formulario.color = ft.Colors.BLUE_900
            titulo_formulario.color = color_azul
        else:
            icono_formulario.icon = ft.Icons.CELEBRATION_ROUNDED
            icono_formulario.color = color_naranja
            titulo_formulario.color = color_naranja

        contenedor.content = vista_formulario
        page.update()

    def volver_principal():
        contenedor.content = vista_principal
        page.update()

    def guardar_actividad(e):
        nombre = campo_nombre.content.value.strip()
        descripcion = campo_descripcion.content.value.strip()

        if not nombre:
            mostrar_snackbar(page, "⚠️ El nombre de la actividad es obligatorio", ft.Colors.ORANGE_700)
            return
        if not estado["fecha"]:
            mostrar_snackbar(page, "⚠️ Debes seleccionar una fecha", ft.Colors.ORANGE_700)
            return
        if not estado["hora_inicio"] or not estado["hora_fin"]:
            mostrar_snackbar(page, "⚠️ Debes seleccionar hora de inicio y fin", ft.Colors.ORANGE_700)
            return

        exito = agregar_actividad_db(
            correo_usuario,
            estado["categoria"],
            nombre,
            estado["fecha"],
            estado["hora_inicio"],
            estado["hora_fin"],
            descripcion
        )

        if exito:
            mostrar_snackbar(page, "✅ Actividad registrada correctamente", ft.Colors.GREEN_700)
            volver_principal()
        else:
            mostrar_snackbar(page, "❌ Error al guardar la actividad", ft.Colors.RED_700)

    return contenedor


# --- Bloque de prueba ---
if __name__ == "__main__":
    def test_main(page: ft.Page):
        page.window.width = 380
        page.window.height = 720
        page.window.resizable = False
        page.padding = 0
        page.margin = 0
        page.title = "Prueba Inicio"

        celular_test = ft.Container(
            expand=True,
            image=ft.DecorationImage(src="/bg.jpg", fit="cover"),
            content=ft.Container(
                content=obtener_vista_inicio(page, "correo@test.com"),
                expand=True,
                padding=ft.Padding.only(left=20, right=20, top=20, bottom=5)
            )
        )
        page.add(celular_test)

    ft.run(test_main, assets_dir="../images")