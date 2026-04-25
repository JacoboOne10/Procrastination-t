import flet as ft
from datetime import datetime, timedelta, date
from vistas.db_manager import obtener_actividades_por_rango_db


def obtener_vista_estadisticas(page, correo_usuario):
    color_azul = ft.Colors.BLUE_900
    color_naranja = ft.Colors.ORANGE_600

    modo = {"actual": "semana"}

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
        fin = inicio + timedelta(days=6)
        return inicio, fin

    def obtener_rango_mes():
        hoy = date.today()
        inicio = hoy.replace(day=1)
        if hoy.month == 12:
            fin = hoy.replace(month=12, day=31)
        else:
            fin = hoy.replace(month=hoy.month + 1, day=1) - timedelta(days=1)
        return inicio, fin

    # ──────────────────────────────────────────
    #  GRÁFICA DE DISTRIBUCIÓN MANUAL
    # ──────────────────────────────────────────

    def construir_pastel(total_academica, total_ocio):
        total = total_academica + total_ocio
        if total == 0:
            return ft.Container(
                content=ft.Text("Sin datos", color=ft.Colors.GREY_500, size=13),
                alignment=ft.Alignment(0, 0),
                height=60
            )

        porc_ac = (total_academica / total) * 100
        porc_oc = (total_ocio / total) * 100

        barra_academica = ft.Container(
            bgcolor=ft.Colors.BLUE_700,
            border_radius=ft.BorderRadius(top_left=8, top_right=0, bottom_left=8, bottom_right=0),
            expand=int(round(porc_ac)) if porc_ac > 0 else 1,
            height=22
        )
        barra_ocio = ft.Container(
            bgcolor=color_naranja,
            border_radius=ft.BorderRadius(top_left=0, top_right=8, bottom_left=0, bottom_right=8),
            expand=int(round(porc_oc)) if porc_oc > 0 else 1,
            height=22
        )

        return ft.Column([
            ft.Row(
                controls=[barra_academica, barra_ocio],
                spacing=2,
                expand=True
            ),
            ft.Row([
                ft.Container(width=12, height=12, bgcolor=ft.Colors.BLUE_700, border_radius=3),
                ft.Text(f"Académica {porc_ac:.0f}%", size=12, color=ft.Colors.GREY_700),
                ft.Container(width=10),
                ft.Container(width=12, height=12, bgcolor=color_naranja, border_radius=3),
                ft.Text(f"Ocio {porc_oc:.0f}%", size=12, color=ft.Colors.GREY_700),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], spacing=8, expand=True)

    # ──────────────────────────────────────────
    #  GRÁFICA DE BARRAS MANUAL
    # ──────────────────────────────────────────

    def construir_barras(datos_barras, etiquetas):
        todos_valores = [
            datos_barras[i]["Académica"] + datos_barras[i]["Ocio"]
            for i in range(len(etiquetas))
        ]
        max_val = max(todos_valores) if todos_valores and max(todos_valores) > 0 else 1
        max_val_ceil = max(1, int(max_val) + (1 if max_val % 1 > 0 else 0))
        altura_max = 100

        num_marcas = min(4, max_val_ceil)
        paso = max(1, max_val_ceil // num_marcas)
        marcas_y = list(range(0, max_val_ceil + 1, paso))

        columnas = []
        for i, etiqueta in enumerate(etiquetas):
            h_ac = datos_barras[i]["Académica"]
            h_oc = datos_barras[i]["Ocio"]
            alt_ac = min(int((h_ac / max_val_ceil) * altura_max), altura_max)
            alt_oc = min(int((h_oc / max_val_ceil) * altura_max), altura_max)

            columnas.append(
                ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Container(expand=True),
                            ft.Container(
                                bgcolor=ft.Colors.BLUE_700,
                                width=12,
                                height=max(alt_ac, 2),
                                border_radius=ft.BorderRadius(
                                    top_left=3, top_right=3,
                                    bottom_left=0, bottom_right=0
                                )
                            )
                        ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Column([
                            ft.Container(expand=True),
                            ft.Container(
                                bgcolor=color_naranja,
                                width=12,
                                height=max(alt_oc, 2),
                                border_radius=ft.BorderRadius(
                                    top_left=3, top_right=3,
                                    bottom_left=0, bottom_right=0
                                )
                            )
                        ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ], height=altura_max, spacing=3, alignment=ft.MainAxisAlignment.END),
                    ft.Text(etiqueta, size=11, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
                ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                    expand=True
                )
            )

        eje_y = ft.Column(
            controls=[
                ft.Text(f"{v}h", size=10, color=ft.Colors.GREY_400)
                for v in reversed(marcas_y)
            ],
            height=altura_max,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.END,
            width=28
        )

        return ft.Row([
            eje_y,
            ft.Container(width=4),
            ft.Container(
                content=ft.Row(columnas, alignment=ft.MainAxisAlignment.SPACE_AROUND),
                expand=True,
                height=altura_max + 20
            )
        ], vertical_alignment=ft.CrossAxisAlignment.START)

    # ──────────────────────────────────────────
    #  CONTENEDOR PRINCIPAL
    # ──────────────────────────────────────────

    contenedor_stats = ft.Column(
        scroll=ft.ScrollMode.HIDDEN,
        expand=True,
        spacing=12
    )

    def construir_vista():
        contenedor_stats.controls.clear()

        if modo["actual"] == "semana":
            inicio, fin = obtener_rango_semana()
        else:
            inicio, fin = obtener_rango_mes()

        actividades = obtener_actividades_por_rango_db(
            correo_usuario,
            inicio.strftime("%Y-%m-%d"),
            fin.strftime("%Y-%m-%d")
        )

        total_academica = 0.0
        total_ocio = 0.0

        if modo["actual"] == "semana":
            datos_barras = {i: {"Académica": 0.0, "Ocio": 0.0} for i in range(7)}
            etiquetas = ["L", "M", "X", "J", "V", "S", "D"]
            for act in actividades:
                horas = calcular_duracion_horas(act[5], act[6])
                fecha_act = datetime.strptime(act[4], "%Y-%m-%d").date()
                dia_idx = (fecha_act - inicio).days
                if 0 <= dia_idx <= 6:
                    datos_barras[dia_idx][act[1]] += horas
                if act[1] == "Académica":
                    total_academica += horas
                else:
                    total_ocio += horas
        else:
            datos_barras = {i: {"Académica": 0.0, "Ocio": 0.0} for i in range(5)}
            etiquetas = [f"S{i + 1}" for i in range(5)]
            for act in actividades:
                horas = calcular_duracion_horas(act[5], act[6])
                fecha_act = datetime.strptime(act[4], "%Y-%m-%d").date()
                semana_idx = (fecha_act - inicio).days // 7
                if 0 <= semana_idx <= 4:
                    datos_barras[semana_idx][act[1]] += horas
                if act[1] == "Académica":
                    total_academica += horas
                else:
                    total_ocio += horas

        # ── TARJETAS RESUMEN ──
        def tarjeta_resumen(titulo, horas, color, icono):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icono, color=color, size=24),
                    ft.Text(formato_tiempo(horas), size=18, weight="bold", color=color),
                    ft.Text(titulo, size=11, color=ft.Colors.GREY_600),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                padding=15,
                expand=True,
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                )
            )

        contenedor_stats.controls.append(
            ft.Row([
                tarjeta_resumen("Académica", total_academica, color_azul, ft.Icons.SCHOOL_ROUNDED),
                ft.Container(width=10),
                tarjeta_resumen("Ocio", total_ocio, color_naranja, ft.Icons.CELEBRATION_ROUNDED),
            ])
        )

        # ── GRÁFICA DE DISTRIBUCIÓN ──
        contenedor_stats.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("Distribución", size=16, weight="bold", color=color_azul),
                    ft.Container(height=5),
                    construir_pastel(total_academica, total_ocio),
                ], expand=True),
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                padding=15,
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                )
            )
        )

        # ── GRÁFICA DE BARRAS ──
        contenedor_stats.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Horas por día" if modo["actual"] == "semana" else "Horas por semana",
                        size=16, weight="bold", color=color_azul
                    ),
                    ft.Container(height=5),
                    construir_barras(datos_barras, etiquetas),
                ]),
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                padding=15,
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                )
            )
        )

        # ── HISTORIAL ──
        contenedor_stats.controls.append(
            ft.Text("Historial de actividades", size=16, weight="bold", color=color_azul)
        )

        if actividades:
            for act in actividades:
                horas = calcular_duracion_horas(act[5], act[6])
                tiempo_str = formato_tiempo(horas)
                fecha_str = datetime.strptime(act[4], "%Y-%m-%d").strftime("%d/%m/%Y")
                color_cat = color_azul if act[1] == "Académica" else color_naranja
                icono_cat = ft.Icons.SCHOOL_ROUNDED if act[1] == "Académica" else ft.Icons.CELEBRATION_ROUNDED

                contenedor_stats.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(icono_cat, color=color_cat, size=22),
                            ft.Column([
                                ft.Text(act[2], size=14, weight="bold", color=ft.Colors.BLACK87),
                                ft.Text(fecha_str, size=11, color=ft.Colors.GREY_500),
                            ], spacing=2, expand=True),
                            ft.Text(tiempo_str, size=13, weight="bold", color=color_cat)
                        ]),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=12,
                        padding=ft.Padding.only(left=15, right=15, top=12, bottom=12),
                        shadow=ft.BoxShadow(
                            blur_radius=8,
                            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                            offset=ft.Offset(0, 3)
                        )
                    )
                )
        else:
            contenedor_stats.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No hay actividades en este período",
                        color=ft.Colors.GREY_500,
                        size=13
                    ),
                    alignment=ft.Alignment(0, 0),
                    padding=20
                )
            )

        page.update()

    # ── TOGGLE SEMANA / MES ──
    btn_semana = ft.Container(
        content=ft.Text("Semana", size=13, weight="bold", color=ft.Colors.WHITE),
        bgcolor=color_azul,
        border_radius=10,
        padding=ft.Padding.only(left=20, right=20, top=8, bottom=8),
        on_click=lambda _: cambiar_modo("semana")
    )

    btn_mes = ft.Container(
        content=ft.Text("Mes", size=13, weight="bold", color=ft.Colors.GREY_600),
        bgcolor=ft.Colors.GREY_200,
        border_radius=10,
        padding=ft.Padding.only(left=20, right=20, top=8, bottom=8),
        on_click=lambda _: cambiar_modo("mes")
    )

    def cambiar_modo(nuevo_modo):
        modo["actual"] = nuevo_modo
        if nuevo_modo == "semana":
            btn_semana.bgcolor = color_azul
            btn_semana.content.color = ft.Colors.WHITE
            btn_mes.bgcolor = ft.Colors.GREY_200
            btn_mes.content.color = ft.Colors.GREY_600
        else:
            btn_mes.bgcolor = color_azul
            btn_mes.content.color = ft.Colors.WHITE
            btn_semana.bgcolor = ft.Colors.GREY_200
            btn_semana.content.color = ft.Colors.GREY_600
        construir_vista()

    construir_vista()

    return ft.Column([
        ft.Container(height=10),
        ft.Text("Estadísticas", size=24, weight="bold", color=color_azul),
        ft.Row([btn_semana, btn_mes], spacing=10),
        ft.Container(height=5),
        contenedor_stats,
    ], expand=True, spacing=10)


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
            image=ft.DecorationImage(src="/5.jpg", fit="cover"),
            content=ft.Container(
                content=obtener_vista_estadisticas(page, "correo@test.com"),
                expand=True,
                padding=ft.Padding.only(left=20, right=20, top=20, bottom=5)
            )
        )
        page.add(celular_test)

    ft.run(test_main, assets_dir="../images")