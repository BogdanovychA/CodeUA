# -*- coding: utf-8 -*-

import asyncio

import flet as ft

from utils import elements
from utils.config import BASE_URL, TEXT_SIZE

TITLE = "Про автора"
ROUTE = BASE_URL + "/about"


def button(page) -> ft.Button:
    return ft.Button(
        TITLE,
        on_click=lambda: asyncio.create_task(page.push_route(ROUTE)),
    )


def build_view(page: ft.Page) -> ft.View:
    page.title = TITLE
    return ft.View(
        route=ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text("Андрій БОГДАНОВИЧ", size=TEXT_SIZE),
            ft.Text(""),
            ft.Image(
                src="/images/bogdanovych.jpg",
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text(
                size=TEXT_SIZE,
                spans=[
                    elements.link("Домашня сторінка", "https://www.bogdanovych.org"),
                    ft.TextSpan("\n"),
                    elements.link("GitHub", "https://github.com/BogdanovychA/CodeUA"),
                ],
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
            elements.back_button(page),
        ],
    )
