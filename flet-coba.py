import flet as ft

def main(page: ft.Page):
    page.title = "Welcome to Realm Chat!"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 100)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 100)
        page.update()

    page.add(
        ft.Row(
            [
                ft.TextField(value="Kontol", text_align=ft.TextAlign.RIGHT, width=100),
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main, view=ft.WEB_BROWSER, port=8510)