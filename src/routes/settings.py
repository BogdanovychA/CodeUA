# -*- coding: utf-8 -*-


from datetime import time

import flet as ft
from fluent_manager import FluentManager

from config import app, default, style
from routes import about, author
from utils import elements
from utils.models import Bool, PandorasBox

ROUTE = app.settings.base_url + "/settings"


def build_view(
    page: ft.Page,
    box: PandorasBox,
) -> ft.View:
    """Екран налаштувань"""

    async def _clear_cache() -> None:
        """Обробник кнопки очистки кешу"""

        await box.storage.clear()
        await _reset()

    async def _reset() -> None:
        """Обробник кнопки скидання налаштувань"""

        # Скидання часу будильника
        new_alarm_time = default.settings.alarm_time.copy()
        await _set_alarm(new_alarm_time)

        # Скидання вкл/викл будильника
        box.alarm_on = True
        await box.storage.set("alarm_on", True)
        alarm_on_selector.selected[0] = Bool.TRUE
        alarm_on_selector.update()

        # Скидання кольору будильника
        alarm_block.style.color = ft.Colors.PRIMARY
        alarm_block.update()

    async def _set_alarm(new_alarm_time: dict) -> None:
        """Встановлення будильника"""

        box.alarm_time = new_alarm_time
        await box.storage.set("alarm_time", new_alarm_time)

        alarm_block.value = (
            f'{new_alarm_time["hours"]:02}:{new_alarm_time["minutes"]:02}'
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
            box.alarm_on = True
            await box.storage.set("alarm_on", True)
            alarm_block.style.color = ft.Colors.PRIMARY
        else:
            box.alarm_on = False
            await box.storage.set("alarm_on", False)
            alarm_block.style.color = ft.Colors.ON_PRIMARY

        alarm_block.update()

    async def _lang_switch(event: ft.Event) -> None:
        """Обробник перемикача мови"""

        new_locale = lang_switcher.value
        box.lang = FluentManager([new_locale], str(app.settings.locales_dir))

        await box.storage.set("locale", new_locale)

        event.page.views.clear()
        event.page.views.append(build_view(page, box))

    hours, minutes, seconds = (
        box.alarm_time[k] for k in ("hours", "minutes", "seconds")
    )

    alarm_block = ft.Text(
        f"{hours:02}:{minutes:02}",
        style=ft.TextStyle(
            color=(ft.Colors.PRIMARY if box.alarm_on else ft.Colors.ON_PRIMARY),
            weight=ft.FontWeight.BOLD,
        ),
        size=style.settings.text_size,
    )

    time_picker = ft.TimePicker(
        value=time(hour=hours, minute=minutes, second=seconds),
        confirm_text=box.lang.get("settings-time-picker-confirm"),
        error_invalid_text=box.lang.get("settings-time-picker-error"),
        help_text=box.lang.get("settings-time-picker-help"),
        entry_mode=ft.TimePickerEntryMode.DIAL,
        hour_format=ft.TimePickerHourFormat.H24,
        on_change=_change,
    )

    alarm_on_selector = ft.SegmentedButton(
        selected=[Bool.TRUE if box.alarm_on else Bool.FALSE],
        allow_empty_selection=False,
        allow_multiple_selection=False,
        show_selected_icon=False,
        segments=[
            ft.Segment(
                value=Bool.TRUE,
                icon=ft.Icons.NOTIFICATIONS_ACTIVE_ROUNDED,
            ),
            ft.Segment(
                value=Bool.FALSE,
                icon=ft.Icons.NOTIFICATIONS_OFF_ROUNDED,
            ),
        ],
        on_change=_switch,
    )

    def _create_lang_switcher_options() -> list[ft.DropdownOption]:
        options = []
        for language in box.lang.languages:
            options.append(ft.DropdownOption(key=language, text=language.upper()))
        return options

    lang_switcher = ft.Dropdown(
        label=box.lang.get("settings-lang-switch", volume=int(box.audio.volume * 100)),
        label_style=ft.TextStyle(size=style.settings.text_size),
        value=box.lang.locales[0],
        options=_create_lang_switcher_options(),
        on_select=_lang_switch,
    )

    page.title = box.lang.get("settings-title")

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(box.lang.get("settings-title"), page),
            ft.Text(""),
            ft.Text(box.lang.get("settings-title"), size=style.settings.text_size),
            ft.Text(""),
            lang_switcher,
            ft.Text(""),
            alarm_on_selector,
            ft.Text(
                box.lang.get("settings-alarm-time-label"), size=style.settings.text_size
            ),
            alarm_block,
            ft.Row(
                controls=[
                    ft.Button(
                        content=box.lang.get("settings-set-time"),
                        on_click=lambda: page.show_dialog(time_picker),
                    ),
                    ft.IconButton(
                        ft.Icons.UPDATE,
                        on_click=_reset,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(""),
            ft.Row(
                controls=[
                    author.button(page, box),
                    about.button(page, box),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            elements.back_button(page, box),
        ],
    )
