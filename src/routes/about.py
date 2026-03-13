# -*- coding: utf-8 -*-

import asyncio

import flet as ft

from config import app, style
from routes import author, root
from utils import elements

TITLE = "Про застосунок"
ROUTE = app.settings.base_url + "/about"


def button(page) -> ft.Button:
    "Кнопка екрану про застосунок"

    return ft.Button(
        TITLE,
        on_click=lambda: asyncio.create_task(page.push_route(ROUTE)),
    )


def build_view(page: ft.Page) -> ft.View:
    """Екран про автора"""

    page.title = TITLE
    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text(root.TITLE, size=style.settings.text_size),
            ft.Text(f"Версія {app.settings.version}"),
            ft.Image(
                src="/images/foundation101-512x512.jpg",
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text(
                "Створено за підтримки\nГО «Фундація.101»",
                size=style.settings.text_size,
            ),
            ft.Text(
                size=style.settings.text_size,
                spans=[
                    elements.link(
                        "Підтримати проєкт", "https://send.monobank.ua/jar/8Qn1woNnC7"
                    ),
                ],
            ),
            ft.Text(""),
            ft.Text(
                size=style.settings.text_size,
                spans=[
                    elements.link("Вебзастосунок", "https://codeua.foundation101.org"),
                    ft.TextSpan("\n"),
                    elements.link(
                        "Android (Google Play)",
                        "https://play.google.com/store/apps/details?id=org.foundation101.codeua",
                    ),
                    ft.TextSpan("\n"),
                    elements.link("GitHub", "https://github.com/BogdanovychA/CodeUA"),
                ],
            ),
            ft.Text(""),
            author.button(page),
            elements.back_button(page),
        ],
    )
