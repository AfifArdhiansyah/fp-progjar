import flet as ft

def main(page: ft.Page):
    page.title = "Welcome to Realm Chat!"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.update()
    
    page.add(
        ft.Column(
            [
                ft.Image(
                    src=f"https://media.licdn.com/dms/image/C4D03AQHYvfZw44rlDQ/profile-displayphoto-shrink_800_800/0/1662634536773?e=2147483647&v=beta&t=HlzfZg_0102MbM5BuHQEpMhcnpEKgoZ_1rZYpT5F644",
                ),
                ft.Text(
                    "Selamat Datang di Chat Realm Roy",
                    size=50,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.ORANGE_800,
                    weight=ft.FontWeight.NORMAL,
                ),    
            ],
        )
    )

ft.app(target=main, view=ft.WEB_BROWSER, port=8510)