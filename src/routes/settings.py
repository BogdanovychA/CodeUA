# -*- coding: utf-8 -*-

import flet as ft

from utils import elements
from utils.config import BASE_URL, TEXT_SIZE

TITLE = "Налаштування"
ROUTE = BASE_URL + "/settings"


def build_view(page: ft.Page) -> ft.View:

    return ft.View(
        route=ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE),
            ft.Text(""),
            ft.Text(TITLE, size=TEXT_SIZE),
            ft.Text(""),
            ft.Text(""),
            elements.back_button(page),
        ],
    )
