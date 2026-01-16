# -*- coding: utf-8 -*-

import asyncio

import flet as ft

from routes import root
from utils.config import LINK_COLOR, TITLE_SIZE


def back_button(page) -> ft.Button:
    """Кнопка 'назад'"""

    return ft.Button(
        "На головну",
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda: asyncio.create_task(page.push_route(root.ROUTE)),
    )


def app_bar(title, page) -> ft.AppBar:
    """Верхня панель застосунку"""

    from routes import settings

    return ft.AppBar(
        title=ft.Text(title, size=TITLE_SIZE, weight=ft.FontWeight.BOLD),
        center_title=True,
        actions=[
            ft.IconButton(
                ft.Icons.MENU,
                on_click=lambda: asyncio.create_task(page.push_route(settings.ROUTE)),
            ),
        ],
        bgcolor=ft.Colors.SURFACE_CONTAINER,
    )


def link(text: str, url: str) -> ft.TextSpan:
    """Функція створення посилань та обробки наведення на них курсору"""

    style_normal = ft.TextStyle(decoration=ft.TextDecoration.NONE, color=LINK_COLOR)
    style_hover = ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, color=LINK_COLOR)

    def _handler(event: ft.Event) -> None:
        span.style = style_hover if event.name == "enter" else style_normal
        span.update()

    span = ft.TextSpan(
        text,
        url=url,
        style=style_normal,
        on_enter=_handler,
        on_exit=_handler,
    )

    return span
