# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.models import PandorasBox

import asyncio

import flet as ft

from config import app, style
from routes import about
from utils import elements

ROUTE = app.settings.base_url + "/author"


def button(page, box: PandorasBox) -> ft.Button:
    "Кнопка екрану про автора"

    return ft.Button(
        box.lang.get("author-title"),
        on_click=lambda: asyncio.create_task(page.push_route(ROUTE)),
    )


def build_view(page: ft.Page, box: PandorasBox) -> ft.View:
    """Екран про автора"""

    page.title = box.lang.get("author-title")

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(box.lang.get("author-title"), page),
            ft.Text(""),
            ft.Image(
                src="/images/bogdanovych-900x900.jpg",
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text(box.lang.get("author-name"), size=style.settings.text_size),
            ft.Text(
                size=style.settings.text_size,
                spans=[
                    elements.link(
                        box.lang.get("author-homepage"), "https://www.bogdanovych.org"
                    ),
                    ft.TextSpan("\n"),
                    elements.link(
                        box.lang.get("author-other-apps"),
                        "https://apps.bogdanovych.org",
                    ),
                ],
            ),
            ft.Text(""),
            about.button(page, box),
            elements.back_button(page, box),
        ],
    )
