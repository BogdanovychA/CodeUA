# -*- coding: utf-8 -*-

import asyncio

import flet as ft

from routes import author
from utils import elements
from utils.config import BASE_URL, TEXT_SIZE

TITLE = "Про застосунок"
ROUTE = BASE_URL + "/about"
VERSION = "1.0.7"


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
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text("CodeUA (код українця)", size=TEXT_SIZE),
            ft.Text(f"Версія {VERSION}"),
            ft.Image(
                src="/images/foundation101-512x512.jpg",
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text(
                "Створено за підтримки\nГО «Фундація.101»",
                size=TEXT_SIZE,
            ),
            ft.Text(
                size=TEXT_SIZE,
                spans=[
                    elements.link(
                        "Підтримати проєкт", "https://send.monobank.ua/jar/8Qn1woNnC7"
                    ),
                ],
            ),
            ft.Text(""),
            ft.Text(
                size=TEXT_SIZE,
                spans=[
                    elements.link("Веб-версія", "https://codeua.foundation101.org"),
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
