import flet as ft
from datetime import datetime, timedelta, date
from db_manager import (
    obtener_actividades_por_rango_db,
    obtener_actividades_db,
    actualizar_actividad_db,
    eliminar_actividad_db
)
from vistas.notis import mostrar_snackbar


def obtener_vista_estadisticas(page, correo_usuario):
    color_azul = ft.Colors.BLUE_900
    color_naranja = ft.Colors.ORANGE_600

    modo = {
        "actual": "semana",
    }

    opciones_labels = {
        "dia": "Hoy",
        "semana": "Esta semana",
        "mes": "Este mes",
        "todo": "Todo el tiempo",
    }

    # ──────────────────────────────────────────
    #  UTILIDADES
    # ──────────────────────────────────────────

    def calcular_duracion_horas(hora_inicio, hora_fin):
        fmt = "%H:%M"
        inicio = datetime.strptime(hora_inicio, fmt)
        fin = datetime.strptime(hora_fin, fmt)
        diff = fin - inicio
        if diff.total_seconds() < 0:
            diff += timedelta(days=1)
        return diff.total_seconds() / 3600

    def formato_tiempo(horas):
        horas_int = int(horas)
        minutos = int((horas % 1) * 60)
        if horas_int > 0 and minutos > 0:
            return f"{horas_int}h {minutos}min"
        elif horas_int > 0:
            return f"{horas_int}h"
        else:
            return f"{minutos}min"

    def obtener_rango_semana():
        hoy = date.today()
        inicio = hoy - timedelta(days=hoy.weekday())
        return inicio, inicio + timedelta(days=6)

    def obtener_rango_mes():
        hoy = date.today()
        inicio = hoy.replace(day=1)
        if hoy.month == 12:
            fin = hoy.replace(month=12, day=31)
        else:
            fin = hoy.replace(month=hoy.month + 1, day=1) - timedelta(days=1)
        return inicio, fin

    # ──────────────────────────────────────────
    #  GRÁFICA DE DISTRIBUCIÓN
    # ──────────────────────────────────────────

    def construir_distribucion(total_academica, total_ocio):
        total = total_academica + total_ocio
        if total == 0:
            return ft.Container(
                content=ft.Text("Sin datos", color=ft.Colors.GREY_500, size=13),
                alignment=ft.Alignment(0, 0), height=60
            )
        porc_ac = (total_academica / total) * 100
        porc_oc = (total_ocio / total) * 100
        return ft.Column([
            ft.Row([
                ft.Container(
                    bgcolor=ft.Colors.BLUE_700,
                    border_radius=ft.BorderRadius(top_left=8, top_right=0, bottom_left=8, bottom_right=0),
                    expand=int(round(porc_ac)) if porc_ac > 0 else 1,
                    height=22
                ),
                ft.Container(
                    bgcolor=color_naranja,
                    border_radius=ft.BorderRadius(top_left=0, top_right=8, bottom_left=0, bottom_right=8),
                    expand=int(round(porc_oc)) if porc_oc > 0 else 1,
                    height=22
                ),
            ], spacing=2),
            ft.Row([
                ft.Container(width=12, height=12, bgcolor=ft.Colors.BLUE_700, border_radius=3),
                ft.Text(f"Académica {porc_ac:.0f}%", size=12, color=ft.Colors.GREY_700),
                ft.Container(width=10),
                ft.Container(width=12, height=12, bgcolor=color_naranja, border_radius=3),
                ft.Text(f"Ocio {porc_oc:.0f}%", size=12, color=ft.Colors.GREY_700),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], spacing=8)

    # ──────────────────────────────────────────
    #  CONTENEDORES
    # ──────────────────────────────────────────

    contenedor_stats = ft.Column(scroll=ft.ScrollMode.HIDDEN, expand=True, spacing=12)
    contenedor_principal = ft.Container(expand=True)

    # ──────────────────────────────────────────
    #  CONFIRMACIÓN ELIMINAR
    # ──────────────────────────────────────────

    def confirmar_eliminar(act_id, nombre_act):
        def hacer_eliminar(e):
            dialog.open = False
            page.update()
            exito = eliminar_actividad_db(act_id)
            if exito:
                mostrar_snackbar(page, "✅ Actividad eliminada", ft.Colors.GREEN_700)
                construir_vista()
            else:
                mostrar_snackbar(page, "❌ Error al eliminar", ft.Colors.RED_700)

        def cancelar(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            bgcolor=ft.Colors.WHITE,
            title=ft.Text("Eliminar actividad", color=ft.Colors.BLACK),
            content=ft.Text(f"¿Eliminar \"{nombre_act}\"? Esta acción no se puede deshacer.", color=ft.Colors.BLACK),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar,
                              style=ft.ButtonStyle(color=ft.Colors.BLUE_900)),
                ft.TextButton("Eliminar", on_click=hacer_eliminar,
                              style=ft.ButtonStyle(color=ft.Colors.RED_700)),
            ]
        )

        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # ──────────────────────────────────────────
    #  VISTA EDICIÓN
    # ──────────────────────────────────────────

    def abrir_edicion(act):
        act_id, categoria, nombre, descripcion, fecha, hora_inicio, hora_fin = act

        estado_edit = {"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin}

        txt_fecha_e = ft.Text(
            datetime.strptime(fecha, "%Y-%m-%d").strftime("%d/%m/%Y"),
            color=ft.Colors.GREY_600, size=13
        )
        txt_hora_ini_e = ft.Text(hora_inicio, color=ft.Colors.GREY_600, size=13, text_align=ft.TextAlign.CENTER)
        txt_hora_fin_e = ft.Text(hora_fin, color=ft.Colors.GREY_600, size=13, text_align=ft.TextAlign.CENTER)

        campo_nombre_e = ft.Container(
            content=ft.TextField(
                value=nombre, label="Nombre de la actividad",
                prefix_icon=ft.Icons.EDIT_NOTE_ROUNDED,
                border=ft.InputBorder.NONE, bgcolor=ft.Colors.TRANSPARENT, color=ft.Colors.BLACK,
                content_padding=ft.Padding.only(top=10, bottom=10, left=10, right=10),
            ),
            bgcolor=ft.Colors.WHITE, border_radius=15, padding=ft.Padding.only(left=10, right=10),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), offset=ft.Offset(0, 4))
        )

        campo_desc_e = ft.Container(
            content=ft.TextField(
                value=descripcion or "", label="Descripción (opcional)",
                prefix_icon=ft.Icons.NOTES_ROUNDED,
                border=ft.InputBorder.NONE, bgcolor=ft.Colors.TRANSPARENT, color=ft.Colors.BLACK,
                multiline=True, max_lines=3,
                content_padding=ft.Padding.only(top=10, bottom=10, left=10, right=10),
            ),
            bgcolor=ft.Colors.WHITE, border_radius=15, padding=ft.Padding.only(left=10, right=10),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), offset=ft.Offset(0, 4))
        )

        def al_cambiar_fecha_e(e):
            if e.control.value:
                estado_edit["fecha"] = e.control.value.strftime("%Y-%m-%d")
                txt_fecha_e.value = e.control.value.strftime("%d/%m/%Y")
                page.update()

        def al_cambiar_hora_ini_e(e):
            if e.control.value:
                estado_edit["hora_inicio"] = f"{e.control.value.hour:02d}:{e.control.value.minute:02d}"
                txt_hora_ini_e.value = estado_edit["hora_inicio"]
                page.update()

        def al_cambiar_hora_fin_e(e):
            if e.control.value:
                estado_edit["hora_fin"] = f"{e.control.value.hour:02d}:{e.control.value.minute:02d}"
                txt_hora_fin_e.value = estado_edit["hora_fin"]
                page.update()

        dp_e = ft.DatePicker(on_change=al_cambiar_fecha_e)
        tp_ini_e = ft.TimePicker(on_change=al_cambiar_hora_ini_e)
        tp_fin_e = ft.TimePicker(on_change=al_cambiar_hora_fin_e)
        page.overlay.extend([dp_e, tp_ini_e, tp_fin_e])
        page.update()

        def crear_btn_picker_e(icono, texto_ref, on_click):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icono, color=color_azul, size=20), texto_ref
                ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.WHITE, border_radius=15,
                padding=ft.Padding.only(left=15, right=15, top=15, bottom=15),
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), offset=ft.Offset(0, 4)),
                on_click=on_click, expand=True, alignment=ft.Alignment(0, 0)
            )

        color_cat = color_azul if categoria == "Académica" else color_naranja
        icono_cat = ft.Icons.SCHOOL_ROUNDED if categoria == "Académica" else ft.Icons.CELEBRATION_ROUNDED

        def guardar_edicion(e):
            nuevo_nombre = campo_nombre_e.content.value.strip()
            nueva_desc = campo_desc_e.content.value.strip()
            if not nuevo_nombre:
                mostrar_snackbar(page, "⚠️ El nombre es obligatorio", ft.Colors.ORANGE_700)
                return
            exito = actualizar_actividad_db(
                act_id, nombre=nuevo_nombre, descripcion=nueva_desc,
                fecha=estado_edit["fecha"], hora_inicio=estado_edit["hora_inicio"], hora_fin=estado_edit["hora_fin"]
            )
            if exito:
                mostrar_snackbar(page, "✅ Actividad actualizada", ft.Colors.GREEN_700)
                volver_stats()
                construir_vista()
            else:
                mostrar_snackbar(page, "❌ Error al actualizar", ft.Colors.RED_700)

        vista_edicion = ft.Column([
            ft.Column(
                controls=[
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, icon_color=color_azul, on_click=lambda _: volver_stats())
                    ], alignment=ft.MainAxisAlignment.START),
                    ft.Row([ft.Icon(icono_cat, color=color_cat, size=26),
                            ft.Text(f"Editar — {categoria}", size=20, weight="bold", color=color_cat)], spacing=10),
                    ft.Container(height=5),
                    campo_nombre_e, campo_desc_e,
                    crear_btn_picker_e(ft.Icons.CALENDAR_MONTH_ROUNDED, txt_fecha_e,
                                       lambda e: (setattr(dp_e, "open", True), page.update())),
                    ft.Row([
                        ft.Container(content=crear_btn_picker_e(ft.Icons.ACCESS_TIME_ROUNDED, txt_hora_ini_e,
                                                                 lambda e: (setattr(tp_ini_e, "open", True), page.update())), expand=True),
                        ft.Container(width=10),
                        ft.Container(content=crear_btn_picker_e(ft.Icons.TIMER_OFF_ROUNDED, txt_hora_fin_e,
                                                                 lambda e: (setattr(tp_fin_e, "open", True), page.update())), expand=True),
                    ]),
                ],
                scroll=ft.ScrollMode.AUTO, expand=True, spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(
                content=ft.Text("Guardar cambios", size=14, weight="bold", color=ft.Colors.WHITE),
                bgcolor=color_azul, border_radius=15, height=55, alignment=ft.Alignment(0, 0),
                on_click=guardar_edicion,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK), offset=ft.Offset(0, 4))
            ),
            ft.Container(height=10)
        ], expand=True, spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        contenedor_principal.content = vista_edicion
        page.update()

    def volver_stats():
        contenedor_principal.content = vista_stats
        page.update()


    # ──────────────────────────────────────────
    #  CONSTRUIR VISTA STATS
    # ──────────────────────────────────────────

    def construir_vista():
        contenedor_stats.controls.clear()

        actual = modo["actual"]

        # ── Determinar rango y actividades ──
        if actual == "dia":
            hoy = date.today()
            inicio, fin = hoy, hoy
            actividades_periodo = obtener_actividades_por_rango_db(
                correo_usuario, hoy.strftime("%Y-%m-%d"), hoy.strftime("%Y-%m-%d")
            )
        elif actual == "semana":
            inicio, fin = obtener_rango_semana()
            actividades_periodo = obtener_actividades_por_rango_db(
                correo_usuario, inicio.strftime("%Y-%m-%d"), fin.strftime("%Y-%m-%d")
            )
        elif actual == "mes":
            inicio, fin = obtener_rango_mes()
            actividades_periodo = obtener_actividades_por_rango_db(
                correo_usuario, inicio.strftime("%Y-%m-%d"), fin.strftime("%Y-%m-%d")
            )
        else:  # todo
            actividades_periodo = obtener_actividades_db(correo_usuario)
            inicio = fin = date.today()

        # ── Totales ──
        total_academica = sum(
            calcular_duracion_horas(a[5], a[6]) for a in actividades_periodo if a[1] == "Académica"
        )
        total_ocio = sum(
            calcular_duracion_horas(a[5], a[6]) for a in actividades_periodo if a[1] == "Ocio"
        )

        # ── Datos para barras ──
        if actual == "dia":
            datos_barras = {0: {"Académica": total_academica, "Ocio": total_ocio}}
            etiquetas_barras = ["Hoy"]
            titulo_barras = "Horas de hoy"

        elif actual == "semana":
            datos_barras = {i: {"Académica": 0.0, "Ocio": 0.0} for i in range(7)}
            etiquetas_barras = ["L", "M", "X", "J", "V", "S", "D"]
            titulo_barras = "Horas por día"
            for act in actividades_periodo:
                horas = calcular_duracion_horas(act[5], act[6])
                fecha_act = datetime.strptime(act[4], "%Y-%m-%d").date()
                idx = (fecha_act - inicio).days
                if 0 <= idx <= 6:
                    datos_barras[idx][act[1]] += horas

        elif actual == "mes":
            datos_barras = {i: {"Académica": 0.0, "Ocio": 0.0} for i in range(5)}
            etiquetas_barras = [f"S{i + 1}" for i in range(5)]
            titulo_barras = "Horas por semana"
            for act in actividades_periodo:
                horas = calcular_duracion_horas(act[5], act[6])
                fecha_act = datetime.strptime(act[4], "%Y-%m-%d").date()
                idx = (fecha_act - inicio).days // 7
                if 0 <= idx <= 4:
                    datos_barras[idx][act[1]] += horas

        else:  # todo
            meses = {}
            for act in actividades_periodo:
                mes_key = act[4][:7]
                if mes_key not in meses:
                    meses[mes_key] = {"Académica": 0.0, "Ocio": 0.0}
                horas = calcular_duracion_horas(act[5], act[6])
                meses[mes_key][act[1]] += horas
            meses_ordenados = sorted(meses.keys())
            datos_barras = {i: meses[k] for i, k in enumerate(meses_ordenados)}
            etiquetas_barras = [
                datetime.strptime(k + "-01", "%Y-%m-%d").strftime("%b") for k in meses_ordenados
            ] if meses_ordenados else [""]
            titulo_barras = "Horas por mes"

        # ── TARJETAS RESUMEN ──
        def tarjeta_resumen(titulo, horas, color, icono):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icono, color=color, size=24),
                    ft.Text(formato_tiempo(horas), size=18, weight="bold", color=color),
                    ft.Text(titulo, size=11, color=ft.Colors.GREY_600),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                bgcolor=ft.Colors.WHITE, border_radius=15, padding=15, expand=True,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), offset=ft.Offset(0, 4))
            )

        contenedor_stats.controls.append(
            ft.Row([
                tarjeta_resumen("Académica", total_academica, color_azul, ft.Icons.SCHOOL_ROUNDED),
                ft.Container(width=10),
                tarjeta_resumen("Ocio", total_ocio, color_naranja, ft.Icons.CELEBRATION_ROUNDED),
            ])
        )

        # ── DISTRIBUCIÓN ──
        contenedor_stats.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("Distribución", size=16, weight="bold", color=color_azul),
                    ft.Container(height=5),
                    construir_distribucion(total_academica, total_ocio),
                ]),
                bgcolor=ft.Colors.WHITE, border_radius=15, padding=15,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), offset=ft.Offset(0, 4))
            )
        )

        # ── HISTORIAL ──
        if actual == "todo":
            actividades_historial = obtener_actividades_db(correo_usuario)
        else:
            actividades_historial = actividades_periodo

        contenedor_stats.controls.append(
            ft.Text(
                "Historial completo" if actual == "todo" else "Historial de actividades",
                size=16, weight="bold", color=color_azul
            )
        )

        if actividades_historial:
            for act in actividades_historial:
                act_id = act[0]
                horas = calcular_duracion_horas(act[5], act[6])
                tiempo_str = formato_tiempo(horas)
                fecha_str = datetime.strptime(act[4], "%Y-%m-%d").strftime("%d/%m/%Y")
                color_cat = color_azul if act[1] == "Académica" else color_naranja
                icono_cat = ft.Icons.SCHOOL_ROUNDED if act[1] == "Académica" else ft.Icons.CELEBRATION_ROUNDED
                descripcion = act[3] if act[3] else "Sin descripción"

                detalle = ft.Container(
                    content=ft.Column([
                        ft.Divider(height=1, color=ft.Colors.GREY_200),
                        ft.Row([
                            ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=14, color=ft.Colors.GREY_500),
                            ft.Text(f"{act[5]} → {act[6]}", size=12, color=ft.Colors.GREY_600),
                        ], spacing=5),
                        ft.Row([
                            ft.Icon(ft.Icons.NOTES_ROUNDED, size=14, color=ft.Colors.GREY_500),
                            ft.Text(descripcion, size=12, color=ft.Colors.GREY_600, expand=True),
                        ], spacing=5),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED,
                                icon_color=color_azul,
                                icon_size=20,
                                tooltip="Editar",
                                on_click=lambda e, a=act: abrir_edicion(a)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                icon_color=ft.Colors.RED_400,
                                icon_size=20,
                                tooltip="Eliminar",
                                on_click=lambda e, ai=act_id, an=act[2]: confirmar_eliminar(ai, an)
                            ),
                        ], alignment=ft.MainAxisAlignment.END, spacing=0),
                    ], spacing=6),
                    visible=False,
                    padding=ft.Padding.only(top=8)
                )

                flecha = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED, color=ft.Colors.GREY_400, size=20)

                estado_detalle = {"abierto": None, "flecha": None}

                def hacer_toggle(e, d=detalle, f=flecha):
                    # Cerrar el que estaba abierto
                    if estado_detalle["abierto"] and estado_detalle["abierto"] != d:
                        estado_detalle["abierto"].visible = False
                        estado_detalle["flecha"].name = ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED

                    # Toggle del actual
                    d.visible = not d.visible
                    f.name = ft.Icons.KEYBOARD_ARROW_UP_ROUNDED if d.visible else ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED

                    # Guardar el abierto actual
                    estado_detalle["abierto"] = d if d.visible else None
                    estado_detalle["flecha"] = f if d.visible else None

                    page.update()

                contenedor_stats.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(icono_cat, color=color_cat, size=22),
                                ft.Column([
                                    ft.Text(act[2], size=14, weight="bold", color=ft.Colors.BLACK87),
                                    ft.Text(fecha_str, size=11, color=ft.Colors.GREY_500),
                                ], spacing=2, expand=True),
                                ft.Text(tiempo_str, size=13, weight="bold", color=color_cat),
                                flecha,
                            ]),
                            detalle,
                        ], spacing=0),
                        bgcolor=ft.Colors.WHITE, border_radius=12,
                        padding=ft.Padding.only(left=15, right=15, top=12, bottom=12),
                        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK), offset=ft.Offset(0, 3)),
                        on_click=hacer_toggle
                    )
                )

        else:
            contenedor_stats.controls.append(
                ft.Container(
                    content=ft.Text("No hay actividades en este período", color=ft.Colors.GREY_500, size=13),
                    alignment=ft.Alignment(0, 0), padding=20
                )
            )

        page.update()


    # ── DROPDOWN PERSONALIZADO ──
    dropdown_abierto = {"valor": False}

    def crear_opcion(key, label):
        cont = ft.Container(
            content=ft.Text(label, size=13, color=ft.Colors.GREY_800),
            padding=ft.Padding.only(left=15, right=15, top=12, bottom=12),
            border_radius=8,
            bgcolor=ft.Colors.TRANSPARENT
        )

        def on_hover(e, c=cont):
            c.bgcolor = ft.Colors.BLUE_50 if e.data == "true" else ft.Colors.TRANSPARENT
            page.update()

        def on_click(e, k=key):
            cerrar_dropdown()
            cambiar_modo(k)

        cont.on_hover = on_hover
        cont.on_click = on_click
        return cont

    panel_dropdown = ft.Container(
        content=ft.Column(
            [crear_opcion(k, l) for k, l in opciones_labels.items()],
            spacing=0
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        shadow=ft.BoxShadow(
            blur_radius=15,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        ),
        width=180,
        padding=ft.Padding.only(top=5, bottom=5),
        visible=False
    )

    def abrir_dropdown(e):
        if dropdown_abierto["valor"]:
            cerrar_dropdown()
        else:
            dropdown_abierto["valor"] = True
            panel_dropdown.visible = True
            page.update()

    def cerrar_dropdown():
        dropdown_abierto["valor"] = False
        panel_dropdown.visible = False
        page.update()

    label_btn_periodo = ft.Text("Esta semana", size=13, weight="bold", color=color_azul)

    btn_periodo = ft.Container(
        content=ft.Row([
            label_btn_periodo,
            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED, color=color_azul, size=18)
        ], spacing=5, tight=True),
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        padding=ft.Padding.only(left=15, right=10, top=8, bottom=8),
        shadow=ft.BoxShadow(
            blur_radius=8,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 2)
        ),
        on_click=abrir_dropdown
    )

    def cambiar_modo(nuevo_modo):
        modo["actual"] = nuevo_modo
        label_btn_periodo.value = opciones_labels[nuevo_modo]
        construir_vista()

    construir_vista()

    vista_stats = ft.Stack([
        ft.Column([
            ft.Container(height=10),
            ft.Text("Estadísticas", size=24, weight="bold", color=color_azul),
            ft.Row([btn_periodo], spacing=10),
            ft.Container(height=5),
            contenedor_stats,
        ], expand=True, spacing=10),
        ft.Column([
            ft.Container(height=65),
            panel_dropdown,
        ], spacing=0)
    ], expand=True)

    contenedor_principal.content = vista_stats
    return contenedor_principal


# --- Bloque de prueba ---
if __name__ == "__main__":
    def test_main(page: ft.Page):
        page.window.width = 380
        page.window.height = 720
        page.window.resizable = False
        page.padding = 0
        page.margin = 0
        page.title = "Prueba Estadísticas"

        celular_test = ft.Container(
            expand=True,
            image=ft.DecorationImage(src="/bg.jpg", fit="cover"),
            content=ft.Container(
                content=obtener_vista_estadisticas(page, "correo@test.com"),
                expand=True,
                padding=ft.Padding.only(left=20, right=20, top=20, bottom=5)
            )
        )
        page.add(celular_test)

    ft.run(test_main, assets_dir="../images")