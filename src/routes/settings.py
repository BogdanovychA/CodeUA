# -*- coding: utf-8 -*-

from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING

import flet as ft

from config import app, default, style
from routes import about, author
from utils import elements
from utils.models import Bool

if TYPE_CHECKING:
    import flet_audio as fta
    from flet_storage import FletStorage

    from utils.locale_manager import LocaleManager

TITLE = "Налаштування"
ROUTE = app.settings.base_url + "/settings"


def build_view(
    page: ft.Page,
    audio: list[fta.Audio],
    storage: FletStorage,
    lang: list[LocaleManager],
) -> ft.View:
    """Екран налаштувань"""

    async def _clear_cache() -> None:
        """Обробник кнопки очистки кешу"""

        await storage.clear()
        await _reset()

    async def _reset() -> None:
        """Обробник кнопки скидання налаштувань"""

        # Скидання часу будильника
        new_alarm_time = default.settings.alarm_time.copy()
        await _set_alarm(new_alarm_time)

        # Скидання вкл/викл будильника
        page.session.store.set("alarm_on", True)
        await storage.set("alarm_on", True)
        alarm_on_selector.selected[0] = Bool.TRUE
        alarm_on_selector.update()

        # Скидання кольору будильника
        alarm_block.style.color = ft.Colors.PRIMARY
        alarm_block.update()

        # Скидання треку
        # await storage.set("track_name", DEFAULT_TRACK)
        # page.session.store.set("track_name", DEFAULT_TRACK)
        # audio[0].src = playlist[DEFAULT_TRACK]
        # await audio[0].pause()
        # await audio[0].seek(ft.Duration(0))

        # Скидання гучності
        # audio[0].volume = DEFAULT_VOLUME
        # await storage.set("volume", DEFAULT_VOLUME)

        # Скидання повтору треку
        # page.session.store.set("repeat", DEFAULT_REPEAT)
        # await storage.set("repeat", DEFAULT_REPEAT)

    async def _set_alarm(new_alarm_time: dict) -> None:
        """Встановлення будильника"""

        page.session.store.set("alarm_time", new_alarm_time)
        await storage.set("alarm_time", new_alarm_time)

        alarm_block.value = (
            f"{new_alarm_time["hours"]:02}:{new_alarm_time["minutes"]:02}"
        )
        alarm_block.update()

    async def _change() -> None:
        """Обробник зміни часу будильника"""

        new_alarm_time = {
            "hours": time_picker.value.hour,
            "minutes": time_picker.value.minute,
            "seconds": time_picker.value.second,
        }

        await _set_alarm(new_alarm_time)

    async def _switch(event: ft.Event) -> None:
        """Обробник перемикача вкл/викл будильника"""

        if event.control.selected[0] == Bool.TRUE:
            page.session.store.set("alarm_on", True)
            await storage.set("alarm_on", True)
            alarm_block.style.color = ft.Colors.PRIMARY
        else:
            page.session.store.set("alarm_on", False)
            await storage.set("alarm_on", False)
            alarm_block.style.color = ft.Colors.ON_PRIMARY

        alarm_block.update()

    alarm_time = page.session.store.get("alarm_time")
    hours, minutes, seconds = (alarm_time[k] for k in ("hours", "minutes", "seconds"))

    alarm_block = ft.Text(
        f"{hours:02}:{minutes:02}",
        style=ft.TextStyle(
            color=(
                ft.Colors.PRIMARY
                if page.session.store.get("alarm_on")
                else ft.Colors.ON_PRIMARY
            ),
            weight=ft.FontWeight.BOLD,
        ),
        size=style.settings.text_size,
    )

    time_picker = ft.TimePicker(
        value=time(hour=hours, minute=minutes, second=seconds),
        confirm_text="Підтвердити",
        error_invalid_text="Не коректний час",
        help_text="Встанови час",
        entry_mode=ft.TimePickerEntryMode.DIAL,
        hour_format=ft.TimePickerHourFormat.H24,
        on_change=_change,
    )

    alarm_on_selector = ft.SegmentedButton(
        selected=[Bool.TRUE if page.session.store.get("alarm_on") else Bool.FALSE],
        allow_empty_selection=False,
        allow_multiple_selection=False,
        show_selected_icon=False,
        segments=[
            ft.Segment(
                value=Bool.TRUE,
                # label=ft.Text(Bool.TRUE),
                icon=ft.Icons.NOTIFICATIONS_ACTIVE_ROUNDED,
            ),
            ft.Segment(
                value=Bool.FALSE,
                # label=ft.Text(Bool.FALSE),
                icon=ft.Icons.NOTIFICATIONS_OFF_ROUNDED,
            ),
        ],
        on_change=_switch,
    )

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text(""),
            ft.Text(TITLE, size=style.settings.text_size),
            ft.Text(""),
            alarm_on_selector,
            ft.Text("Час запуску:", size=style.settings.text_size),
            alarm_block,
            ft.Row(
                controls=[
                    ft.Button(
                        content="Встановити",
                        on_click=lambda: page.show_dialog(time_picker),
                    ),
                    ft.IconButton(
                        ft.Icons.UPDATE,
                        on_click=_reset,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            # ft.Button(
            #     content="Видалити кеш",
            #     icon=ft.Icons.DELETE_SWEEP,
            #     on_click=_clear_cache,
            # ),
            ft.Text(""),
            ft.Row(
                controls=[
                    author.button(page),
                    about.button(page),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            elements.back_button(page, lang),
        ],
    )
