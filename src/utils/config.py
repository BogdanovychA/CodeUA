# -*- coding: utf-8 -*-

import flet as ft

from utils.models import Track

APP_NAME = "CodeUA"
BASE_URL = ""

TITLE_SIZE = 24
TEXT_SIZE = 20

LINK_COLOR = ft.Colors.PRIMARY

FORM_BORDER_COLOR = ft.Colors.PRIMARY
FORM_BG_COLOR = ft.Colors.SURFACE_CONTAINER

DEFAULT_ALARM_TIME = {
    "hours": 9,
    "minutes": 0,
    "seconds": 0,
}

DEFAULT_TRACK = Track.MOMENT.value

DEFAULT_VOLUME = 0.5

playlist = {
    Track.MOMENT.value: "/sounds/moment_of_silence.mp3",
    # Track.ANTHEM.value: "/sounds/anthem_of_Ukraine-1.ogx",
    Track.ANTHEM.value: "/sounds/anthem_of_Ukraine-2.mp3",
}
