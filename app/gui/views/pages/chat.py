import random
from math import pi

import flet as ft
from flet import *

class Chat(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        return Column(
            controls=[
                Container(
                height=800,width=300,
                bgcolor='red',
                content=Column(
                    controls=[
                    Text('Welcome to the homepage'),
                    Container(
                        content=Text('Goto Login',size=25,color='black')
                    )
                ]
            )
          )
        ]
    )