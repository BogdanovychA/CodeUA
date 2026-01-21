# -*- coding: utf-8 -*-

import asyncio

import flet as ft

from routes import about
from utils import elements
from utils.config import BASE_URL, TEXT_SIZE

TITLE = "Про автора"
ROUTE = BASE_URL + "/author"


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
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text(""),
            ft.Image(
                src="/images/bogdanovych-950x950.jpg",
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text("Андрій БОГДАНОВИЧ", size=TEXT_SIZE),
            ft.Text(
                size=TEXT_SIZE,
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
