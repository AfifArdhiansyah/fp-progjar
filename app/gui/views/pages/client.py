import flet as ft
import json
from ... import ChatClient
import os

TARGET_IP = os.getenv("SERVER_IP") or "127.0.0.1"
TARGET_PORT = os.getenv("SERVER_PORT") or "8889"
ON_WEB = os.getenv("ONWEB") or "1"

def main(page: ft.Page):
    page.title = "Client"    

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8550, upload_dir="upload")