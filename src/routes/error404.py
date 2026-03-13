# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.locale_manager import LocaleManager
import flet as ft

from config import app, style
from utils import elements

ROUTE = app.settings.base_url + "/404"


def build_view(page: ft.Page, lang: list[LocaleManager]) -> ft.View:
    """Екран 404 помилки"""

    title = lang[0].get("error404-title")

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(title, page),
            ft.Text(""),
            ft.Text(title, size=style.settings.text_size),
            ft.Text(lang[0].get("error404-target-page", route=page.route)),
            ft.Text(""),
            elements.back_button(page),
        ],
    )
