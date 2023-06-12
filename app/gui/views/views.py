from flet import *
from pages.onboard import Onboard
from pages.menu import Menu
from pages.group import Group
from pages.chat import Chat

def views_handler(page):
  return {
    '/':View(
        route='/',
        controls=[
          Onboard(page)
        ]
      ),
    '/menu':View(
        route='/menu',
        controls=[
          Menu(page)
        ]
      ),
    '/group':View(
        route='/group',
        controls=[
          Group(page)
        ]
      ),
    '/chat':View(
        route='/chat',
        controls=[
          Chat(page)
        ]
      ),
  }