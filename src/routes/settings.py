# -*- coding: utf-8 -*-

from datetime import time

import flet as ft

from utils import elements, storage
from utils.config import BASE_URL, DEFAULT_ALARM_TIME, TEXT_SIZE

TITLE = "Налаштування"
ROUTE = BASE_URL + "/settings"


def build_view(page: ft.Page) -> ft.View:

    async def _clear_cache() -> None:
        await storage.clear()
        await _reset()

    async def _set_alarm(new_alarm_time: dict) -> None:

        page.session.store.set("alarm_time", new_alarm_time)
        await storage.save_dict("alarm_time", new_alarm_time)

        alarm_block.value = (
            f"{new_alarm_time["hours"]:02}:{new_alarm_time["minutes"]:02}"
        )
        alarm_block.update()

    async def _reset() -> None:
        new_alarm_time = DEFAULT_ALARM_TIME.copy()
        await _set_alarm(new_alarm_time)

    async def _change() -> None:

        new_alarm_time = {
            "hours": time_picker.value.hour,
            "minutes": time_picker.value.minute,
            "seconds": time_picker.value.second,
        }

        await _set_alarm(new_alarm_time)

    alarm_time = page.session.store.get("alarm_time")
    hours, minutes, seconds = (alarm_time[k] for k in ("hours", "minutes", "seconds"))

    alarm_block = ft.Text(f"{hours:02}:{minutes:02}", size=TEXT_SIZE)

    time_picker = ft.TimePicker(
        value=time(hour=hours, minute=minutes, second=seconds),
        confirm_text="Підтвердити",
        error_invalid_text="Не коректний час",
        help_text="Встанови час",
        entry_mode=ft.TimePickerEntryMode.DIAL,
        on_change=_change,
    )

    return ft.View(
        route=ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text(""),
            ft.Text(TITLE, size=TEXT_SIZE),
            ft.Text(""),
            ft.Text("Час запуску:", size=TEXT_SIZE),
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
            ft.Button(
                content="Видалити кеш",
                icon=ft.Icons.DELETE_SWEEP,
                on_click=_clear_cache,
            ),
            ft.Text(""),
            elements.back_button(page),
        ],
    )
