# -*- coding: utf-8 -*-

import flet as ft

from utils.models import Track

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

DEFAULT_TRACK = Track.MOMENT

DEFAULT_VOLUME = 0.5

DEFAULT_REPEAT = False

playlist = {
    Track.MOMENT: "/sounds/moment_of_silence.mp3",
    Track.ANTHEM: "/sounds/anthem_of_Ukraine-1.mp3",
    Track.ANTHEM_2: "/sounds/anthem_of_Ukraine-2.mp3",
}
