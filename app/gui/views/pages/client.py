import flet as ft
import json
from chat_client.chatcli import ChatClient
import os

TARGET_IP = os.getenv("SERVER_IP") or "127.0.0.1"
TARGET_PORT = os.getenv("SERVER_PORT") or "8889"
ON_WEB = os.getenv("ONWEB") or "1"

class ChatRoom:
    def __init__(self, page, cc, from_user, to_user):
        self.send_to_field = ft.TextField(
            label="Send to",
            value=to_user,
            expand=True,
        )
        self.chat = ft.TextField(
            label="Write a message...",
            autofocus=True,
            expand=True,
            on_submit=self.send_click,
        )
        self.lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self.send = ft.IconButton(
            icon=ft.icons.SEND_ROUNDED,
            tooltip="Send message",
            on_click=self.send_click,
        )
        self.get_massage = ft.ElevatedButton(
            "Get Message",
            on_click=self.read_inbox,
        )
        self.file_picker = ft.FilePicker(on_result=self.upload_files, on_upload=self.upload_server)
        self.file_pick = ft.IconButton(
            icon=ft.icons.UPLOAD_FILE_ROUNDED,
            tooltip="Send file",
            on_click=self.on_pick_file,
        )
        self.page = page
        self.cc = cc
        self.from_user = from_user
        self.to_user = to_user
        self.page.pubsub.subscribe(self.on_chat)

    def on_pick_file(self, __e__):
        self.page.overlay.append(self.file_picker)
        self.page.update()
        self.file_picker.pick_files(allow_multiple=True)
    
    def update_send_to(self, to_user):
        self.send_to_field.value = to_user
        self.to_user = to_user

    def send_click(self, __e__):
        self.update_send_to(self.send_to_field.value)
        if not self.chat.value:
            self.chat.error_text = "Please enter message"
            self.page.update()
        else:
            print(self.from_user)
            print(self.to_user)
            print(self.chat.value)
            command = f"send {self.to_user} {self.chat.value}"
            server_call = self.cc.proses(command)
            # self.lv.controls.append(ft.Text("To {}: {}".format(self.to_user, self.chat.value)))

            if "sent" in server_call:
                self.page.pubsub.send_all(self.chat.value)

            self.chat.value = ""
            self.chat.focus()
            self.page.update()
    
    def on_chat(self, message):
        check_inbox = json.loads(self.cc.inbox())
        # self.lv.controls.append(ft.Text("From {}: {}".format(check_inbox[self.to_user][0]['msg_from'], check_inbox[self.to_user][0]['msg'])))
        self.page.update()
    
    def read_inbox(self, __e__):
        output = json.loads(self.cc.inbox())
        print("Print Inbox", output)
        self.page.update()

    # file picker and uploads
    def upload_files(self, e:ft.FilePickerResultEvent):
        upload_list = []
        if self.file_picker.result != None and self.file_picker.result.files != None:
            for f in self.file_picker.result.files:
                # print(self.page.get_upload_url(f.name, 600),)
                upload_list.append(
                    ft.FilePickerUploadFile(
                        f.name,
                        upload_url=self.page.get_upload_url(f.name, 600),
                    )
                )
            self.file_picker.upload(upload_list)
    
    def upload_server(self, e:ft.FilePickerUploadEvent):
        if(e.progress == 1):
            command = f"sendfile {self.to_user} app\\client\\upload\\{e.file_name}"
            print(command)
            server_call = self.cc.proses(command)
            print(server_call)
            self.lv.controls.append(ft.Text("To {}: Berhasil mengirim file {}".format(self.to_user, e.file_name)))

            if "sent" in server_call:
                self.page.pubsub.send_all(self.chat.value)

            self.chat.value = ""
            self.chat.focus()
            self.page.update()

def main(page: ft.Page):
    page.title = "Client"
    is_login = False

    chat_client = ChatClient()

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
                ft.ElevatedButton("Login", on_click= do_login)
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
                ft.ElevatedButton("Login", on_click= do_login)
            ],
            actions_alignment="center",
        )

    def do_login(__e__):
            username = username_field.value
            password = password_field.value
            print(username, password)
            if username == "" or password == "":
                ft.alert("Please fill username and password")
                return
            if chat_client.login(username, password):
                page.dialog.open = False
                is_login = True
                # menu_item_username.text = username
                # menu.open = True
                page.go("/")
            else:
                ft.alert("Username or password is wrong")
    
    username_field = ft.TextField(label="Username", autofocus=True)
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        autofocus=True,
        on_submit=do_login,
    )
    name = ft.TextField(label="Name", autofocus=True)
    country = ft.TextField(label="Country", autofocus=True)
    
    login_dialog()

    target_user = ""

    def route_change(__route__):
        troute = ft.TemplateRoute(page.route)
        chat_room = ChatRoom(page, chat_client, chat_client.username, target_user)

        page.views.clear()

        page.views.append(
            ft.View(
                "/",
                [
                    ft.Tabs(
                        tabs = [
                            ft.Tab(
                                text="                                      Private Chat                                        ",
                                content = ft.Column([
                                    ft.Text(chat_client.info()),
                                    ft.Row([chat_room.send_to_field]),
                                    ft.Row([chat_room.chat, chat_room.send, chat_room.file_pick]),
                                ])
                            ),
                            ft.Tab(
                                text="                                      Inbox                                        ",
                                content = ft.Column([
                                    chat_room.get_massage
                                ])
                            ),
                            ft.Tab(
                                text="                                      Group Chat                                    ",
                                # route="/group",
                                content= ft.Container(
                                    content=ft.Text("Private Chat")
                                )
                            ),
                        ]
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