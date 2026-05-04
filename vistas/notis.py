import flet as ft

def mostrar_snackbar(page, mensaje, color):
    page.overlay.append(ft.SnackBar(
        content=ft.Text(mensaje),
        bgcolor=color,
        behavior=ft.SnackBarBehavior.FLOATING,
        margin=ft.Padding.only(left=10, right=10, bottom=400)
    ))
    page.overlay[-1].open = True
    page.update()