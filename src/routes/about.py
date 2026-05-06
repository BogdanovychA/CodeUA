# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.models import PandorasBox

import asyncio

import flet as ft

from config import app, style
from routes import author
from utils import elements

ROUTE = app.settings.base_url + "/about"


def button(page, box: PandorasBox) -> ft.Button:
    "Кнопка екрану про застосунок"

    return ft.Button(
        box.lang.get("about-title"),
        on_click=lambda: asyncio.create_task(page.push_route(ROUTE)),
    )


def build_view(page: ft.Page, box: PandorasBox) -> ft.View:
    """Екран про автора"""

    page.title = box.lang.get("about-title")

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(box.lang.get("about-title"), page),
            ft.Text(box.lang.get("main-title"), size=style.settings.text_size),
            ft.Text(box.lang.get("about-version", version=app.settings.version)),
            ft.Image(
                src="/images/foundation101-512x512.jpg",
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text(
                box.lang.get("about-created-by"),
                size=style.settings.text_size,
            ),
            ft.Text(
                size=style.settings.text_size,
                spans=[
                    elements.link(
                        box.lang.get("about-support"),
                        "https://send.monobank.ua/jar/8Qn1woNnC7",
                    ),
                ],
            ),
            ft.Text(""),
            ft.Text(
                size=style.settings.text_size,
                spans=[
                    elements.link(
                        box.lang.get("about-web-app"),
                        "https://codeua.foundation101.org",
                    ),
                    ft.TextSpan("\n"),
                    elements.link(
                        box.lang.get("about-android"),
                        "https://play.google.com/store/apps/details?id=org.foundation101.codeua",
                    ),
                    ft.TextSpan("\n"),
                    elements.link(
                        box.lang.get("about-github"),
                        "https://github.com/BogdanovychA/CodeUA",
                    ),
                ],
            ),
            ft.Text(""),
            author.button(page, box),
            elements.back_button(page, box),
        ],
    )
