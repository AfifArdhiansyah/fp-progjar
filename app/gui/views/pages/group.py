import random
from math import pi

import flet as ft
from flet import *

class Group(UserControl):
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
                        on_click= lambda _: self.page.go('/chat') ,
                        content=Text('Goto Login',size=25,color='black')
                    )
                ]
            )
          )
        ]
    )