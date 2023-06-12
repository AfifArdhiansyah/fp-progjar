import flet as ft

def main(page: ft.Page):
    page.title = "Welcome to Realm Chat!"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


ft.app(target=main, view=ft.WEB_BROWSER, port=8510)