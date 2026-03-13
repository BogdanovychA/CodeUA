# -*- coding: utf-8 -*-

import asyncio

import flet as ft

from config import app, style
from routes import about
from utils import elements

TITLE = "Про автора"
ROUTE = app.settings.base_url + "/author"


def button(page) -> ft.Button:
    "Кнопка екрану про автора"

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
            ft.Text(""),
            ft.Image(
                src="/images/bogdanovych-900x900.jpg",
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text("Андрій БОГДАНОВИЧ", size=style.settings.text_size),
            ft.Text(
                size=style.settings.text_size,
                spans=[
                    elements.link("Домашня сторінка", "https://www.bogdanovych.org"),
                    ft.TextSpan("\n"),
                    elements.link("Інші застосунки", "https://apps.bogdanovych.org"),
                ],
            ),
            ft.Text(""),
            about.button(page),
            elements.back_button(page),
        ],
    )
