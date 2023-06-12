import random
from math import pi

import flet as ft
from flet import Container, ElevatedButton, Page, Stack, colors


def main(page: Page):

    size = 36
    gap = 6
    duration = 2000

    c1 = colors.PINK_500
    c2 = colors.AMBER_500
    c3 = colors.LIGHT_GREEN_500
    c4 = colors.DEEP_PURPLE_500
    c5 = colors.INDIGO_600

    all_colors = [
        colors.AMBER_400,
        colors.AMBER_ACCENT_400,
        colors.BLUE_400,
        colors.BROWN_400,
        colors.CYAN_700,
        colors.DEEP_ORANGE_500,
        colors.CYAN_500,
        colors.INDIGO_600,
        colors.ORANGE_ACCENT_100,
        colors.PINK,
        colors.RED_600,
        colors.GREEN_400,
        colors.GREEN_ACCENT_200,
        colors.TEAL_ACCENT_200,
        colors.LIGHT_BLUE_500,
    ]

    parts = [
        # R
        (0, 0, c2),
        (0, 1, c2),
        (0, 2, c2),
        (0, 3, c2),
        (0, 4, c2),
        (1, 0, c2),
        (2, 0, c2),

        # O
        (4, 0, c2),
        (4, 1, c2),
        (4, 2, c2),
        (4, 3, c2),
        (4, 4, c2),
        (5, 0, c2),
        (5, 4, c2),
        (6, 0, c2),
        (6, 1, c2),
        (6, 2, c2),
        (6, 3, c2),
        (6, 4, c2),

        # Y
        (8, 0, c2),
        (8, 1, c2),
        (8, 2, c2),
        (8, 4, c2),
        (9, 2, c2),
        (9, 4, c2),
        (10, 0, c2), 
        (10, 1, c2),
        (10, 2, c2),
        (10, 3, c2),
        (10, 4, c2),

        # C
        (12, 0, c2),
        (12, 1, c2),
        (12, 2, c2),
        (12, 3, c2),
        (12, 4, c2),
        (13, 0, c2),
        (13, 4, c2),
        (14, 0, c2),
        (14, 4, c2),

        # H
        (16, 0, c2),
        (16, 1, c2),
        (16, 2, c2),
        (16, 3, c2),
        (16, 4, c2),
        (17, 2, c2),
        (18, 0, c2),
        (18, 1, c2),
        (18, 2, c2),
        (18, 3, c2),
        (18, 4, c2),

        # A
        (20, 0, c2),
        (20, 1, c2),
        (20, 2, c2),
        (20, 3, c2),
        (20, 4, c2),
        (21, 0, c2),
        (21, 2, c2),
        (22, 0, c2),
        (22, 1, c2),
        (22, 2, c2),
        (22, 3, c2),
        (22, 4, c2),

        # T
        (24, 0, c2),
        (25, 0, c2),
        (25, 1, c2),
        (25, 2, c2),
        (25, 3, c2),
        (25, 4, c2),
        (26, 0, c2),

    ]

    width = 27 * (size + gap)
    height = 5 * (size + gap)

    canvas = Stack(
        width=width,
        height=height,
        animate_scale=duration,
        animate_opacity=duration,
    )

    # spread parts randomly
    for i in range(len(parts)):
        canvas.controls.append(
            Container(
                animate=duration,
                animate_position=duration,
                animate_rotation=duration,
            )
        )

    def randomize(e):
        random.seed()
        for i in range(len(parts)):
            c = canvas.controls[i]
            part_size = random.randrange(int(size / 2), int(size * 3))
            c.left = random.randrange(0, width)
            c.top = random.randrange(0, height)
            c.bgcolor = all_colors[random.randrange(0, len(all_colors))]
            c.width = part_size
            c.height = part_size
            c.border_radius = random.randrange(0, int(size / 2))
            c.rotate = random.randrange(0, 90) * 2 * pi / 360
        canvas.scale = 5
        canvas.opacity = 0.3
        go_button.visible = True
        again_button.visible = False
        page.update()

    def assemble(e):
        i = 0
        for left, top, bgcolor in parts:
            c = canvas.controls[i]
            c.left = left * (size + gap)
            c.top = top * (size + gap)
            c.bgcolor = bgcolor
            c.width = size
            c.height = size
            c.border_radius = 5
            c.rotate = 0
            i += 1
        canvas.scale = 1
        canvas.opacity = 1
        go_button.visible = False
        again_button.visible = True
        page.update()


    go_button = ElevatedButton("Go!", on_click=assemble)
    again_button = ElevatedButton("Go to chat!", on_click=lambda _: page.go('/group-screen'))

    randomize(None)

    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.spacing = 30
    page.add(canvas, go_button, again_button)


ft.app(main)