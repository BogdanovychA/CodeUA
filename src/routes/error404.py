# -*- coding: utf-8 -*-

import flet as ft

from config import app, style
from utils import elements

TITLE = "Сторінка не знайдена"
ROUTE = app.settings.base_url + "/404"


def build_view(page: ft.Page) -> ft.View:
    """Екран 404 помилки"""

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text(""),
            ft.Text(TITLE, size=style.settings.text_size),
            ft.Text(f"Цільова сторінка: {page.route}"),
            ft.Text(""),
            elements.back_button(page),
        ],
    )
