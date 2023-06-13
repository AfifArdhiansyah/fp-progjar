import flet as ft
import json
# from ... import ChatClient
import os

TARGET_IP = os.getenv("SERVER_IP") or "127.0.0.1"
TARGET_PORT = os.getenv("SERVER_PORT") or "8889"
ON_WEB = os.getenv("ONWEB") or "1"

def main(page: ft.Page):
    page.title = "Client"
    is_login = True

    # login
    global login_dialog
    def login_dialog():
        nonlocal is_login
        global login_form
        global logouttologin
        global changeto_logout

        def changeto_register(e):
            page.dialog.title=ft.Text(
                "REGISTER", style=ft.TextThemeStyle.TITLE_MEDIUM
            )
            page.dialog.actions=[
                ft.ElevatedButton("Login?", on_click=login_form),
                # ft.ElevatedButton("Register", on_click=register_click)
                ft.ElevatedButton("Register")
            ]
            page.dialog.content=ft.Column([username_field, password_field, name,country], tight=True)
            # page.dialog.content=ft.Column(["username", "password", "name", "country"], tight=True)
            page.update()
        
        def login_form(e):
            page.dialog.title=ft.Text(
                "LOGIN", style=ft.TextThemeStyle.TITLE_MEDIUM
            )
            page.dialog.actions=[
                ft.ElevatedButton("Register?", on_click=changeto_register),
                # ft.ElevatedButton("Login", on_click=login_click)
                ft.ElevatedButton("Login")
            ]
            page.dialog.content=ft.Column([username_field, password_field], tight=True)
            # page.dialog.content=ft.Column(["username", "password"], tight=True)

            page.update()


        page.dialog = ft.AlertDialog(
            open= not is_login,
            modal=True,
            title=ft.Text(
                "LOGIN", style=ft.TextThemeStyle.TITLE_MEDIUM
            ),
            content=ft.Column([username_field, password_field], tight=True),
            # content=ft.Column(["username", "password"], tight=True),
            actions=[
                ft.ElevatedButton("Register", on_click=changeto_register),
                # ft.ElevatedButton("Login", on_click=login_click)
                ft.ElevatedButton("Login")
            ],
            actions_alignment="center",
        )
    
    username_field = ft.TextField(label="Username", autofocus=True)
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        autofocus=True,
        # on_submit=login_click,
    )
    name = ft.TextField(label="Name", autofocus=True)
    country = ft.TextField(label="Country", autofocus=True)
    
    login_dialog()

    # menu
    # global menu_item_username
    # menu_item_username = ft.PopupMenuItem(text="")
    # menu = ft.PopupMenuButton(
    #     items=[
    #         menu_item_username,
    #         ft.PopupMenuItem(
    #             # icon=ft.icons.LOGOUT, text="Logout", on_click=logout_click
    #             icon=ft.icons.LOGOUT, text="Logout"
    #         ),
    #     ]
    # )


    def route_change(__route__):
        troute = ft.TemplateRoute(page.route)
        page.views.clear()

        page.views.append(
            ft.View(
                "/",
                [
                    # ft.Card(
                    #     content=ft.Container(
                    #         content=ft.Column(
                    #             [
                    #                 ft.ListTile(
                    #                     leading=ft.Icon(ft.icons.PERSON),
                    #                     title=ft.Text("Private Chat"),
                    #                     on_click=lambda _: page.go("/private"),
                    #                 ),
                    #                 ft.ListTile(
                    #                     leading=ft.Icon(ft.icons.GROUP),
                    #                     title=ft.Text("Group Chat"),
                    #                     on_click=lambda _: page.go("/group"),
                    #                 ),
                    #             ],
                    #         ),
                    #         padding=ft.padding.symmetric(vertical=10),
                    #     )
                    # ),
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Tabs(
                            tabs = [
                                ft.Tab(
                                    text="                                      Private Chat                                        ",
                                    icon=ft.Icon(ft.icons.PERSON),
                                    # route="/private",
                                ),
                                ft.Tab(
                                    text="                                      Group Chat                                    ",
                                    icon=ft.Icon(ft.icons.GROUP),
                                    # route="/group",
                                ),
                            ]
                        )
                    )               
                ],
            )
        )

        page.update()

    def view_pop(__view__):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8550, upload_dir="upload")