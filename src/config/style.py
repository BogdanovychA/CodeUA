# -*- coding: utf-8 -*-

import flet as ft
from pydantic import BaseModel


class Settings(BaseModel):

    title_size: int = 24
    text_size: int = 20

    link_color: ft.Colors = ft.Colors.PRIMARY
    form_border_color: ft.Colors = ft.Colors.PRIMARY
    form_bg_color: ft.Colors = ft.Colors.SURFACE_CONTAINER


settings = Settings()
