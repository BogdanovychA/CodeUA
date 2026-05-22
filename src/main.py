# -*- coding: utf-8 -*-

import asyncio
import logging
import uuid
from logging import INFO

import flet as ft
import flet_audio as fta
from flet_storage import FletStorage
from fluent_manager import FluentManager
from measurement_api import MeasurementAPI

from config import app, default, style
from config import google_analytics as ga_config
from config.sound import playlist
from routes import about, author, error404, root, settings
from utils import elements, utils
from utils.models import PandorasBox, Track

logging.basicConfig(
    level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def build_main_view(
    page: ft.Page,
    box: PandorasBox,
) -> ft.View:
    """Головний екран застосунку"""

    async def _play():
        """Обробник натискання кнопки play"""

        match box.audio_state:
            case fta.AudioState.PAUSED:
                await box.audio.resume()
            case fta.AudioState.DISPOSED:  # audio player has been disposed
                pass
            case _:
                await box.audio.play()

    async def _stop():
        """Обробник натискання кнопки stop"""

        await box.audio.pause()
        await box.audio.seek(ft.Duration(0))

    async def _pause():
        """Обробник натискання кнопки pause"""

        await box.audio.pause()

    async def _repeat():
        box.repeat = not box.repeat
        await box.storage.set("repeat", box.repeat)

    async def _set_volume(value: float):
        """Обробник кнопок зміни гучності"""

        new_volume = round(utils.clamp_value(box.audio.volume + value, 0, 1), 1)
        box.audio.volume = new_volume
        box.audio.update()
        await box.storage.set("volume", new_volume)
        switcher.label = box.lang.get("main-volume-label", volume=int(new_volume * 100))
        switcher.update()

    async def _switch():
        """Обробник зміни треків"""

        await _pause()
        box.track_name = switcher.value
        await box.storage.set("track_name", box.track_name)
        box.audio.src = playlist[box.track_name]

    async def _ui_update():
        """Фоновий таск оновлення інтерфейсу"""

        while True:
            try:
                if timer.value != box.time_left:
                    timer.value = box.time_left

            except RuntimeError:
                logger.info("RuntimeError")
                await asyncio.sleep(0.1)
                continue

            if box.alarm_on:
                if timer.style.color != ft.Colors.PRIMARY:
                    timer.style.color = ft.Colors.PRIMARY
            else:
                if timer.style.color != ft.Colors.ON_PRIMARY:
                    timer.style.color = ft.Colors.ON_PRIMARY

            if box.repeat:
                if repeat_button.icon != ft.Icons.REPEAT_ON:
                    repeat_button.icon = ft.Icons.REPEAT_ON
            else:
                if repeat_button.icon != ft.Icons.REPEAT:
                    repeat_button.icon = ft.Icons.REPEAT

            match box.audio_state:
                case fta.AudioState.PLAYING:
                    if player_control[1] != pause_button:
                        player_control[1] = pause_button

                case fta.AudioState.DISPOSED:  # audio player has been disposed
                    pass

                case _:
                    if player_control[1] != play_button:
                        player_control[1] = play_button

            page.update()
            await asyncio.sleep(0.5)

    switcher = ft.Dropdown(
        label=box.lang.get("main-volume-label", volume=int(box.audio.volume * 100)),
        label_style=ft.TextStyle(size=style.settings.text_size),
        value=box.track_name,
        options=[
            ft.DropdownOption(
                key=Track.MOMENT, text=box.lang.get("main-track-silence")
            ),
            ft.DropdownOption(
                key=Track.ANTHEM, text=box.lang.get("main-track-anthem-1")
            ),
            ft.DropdownOption(
                key=Track.ANTHEM_2, text=box.lang.get("main-track-anthem-2")
            ),
        ],
        on_select=_switch,
    )

    timer = ft.Text(
        "",
        size=style.settings.text_size,
        style=ft.TextStyle(
            color=(ft.Colors.PRIMARY if box.alarm_on else ft.Colors.ON_PRIMARY),
            weight=ft.FontWeight.BOLD,
        ),
    )

    play_button = ft.IconButton(ft.Icons.PLAY_ARROW_ROUNDED, on_click=_play)
    repeat_button = ft.IconButton(ft.Icons.REPEAT, on_click=_repeat)
    pause_button = ft.IconButton(ft.Icons.PAUSE_ROUNDED, on_click=_pause)
    stop_button = ft.IconButton(ft.Icons.STOP_ROUNDED, on_click=_stop)
    volume_minus_button = ft.IconButton(
        ft.Icons.VOLUME_DOWN_ROUNDED,
        on_click=lambda _: asyncio.create_task(_set_volume(-0.1)),
    )
    volume_plus_button = ft.IconButton(
        ft.Icons.VOLUME_UP_ROUNDED,
        on_click=lambda _: asyncio.create_task(_set_volume(0.1)),
    )

    player_control = [
        volume_minus_button,
        play_button,
        repeat_button,
        stop_button,
        volume_plus_button,
    ]

    controller = ft.Row(
        controls=player_control,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.title = box.lang.get("main-title")

    box.ui_update_task = page.run_task(_ui_update)

    return ft.View(
        route=root.ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(box.lang.get("main-title"), page),
            ft.Text(""),
            ft.Image(
                src="/favicon.png",
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text(
                box.lang.get("main-memory-title"),
                size=style.settings.text_size,
            ),
            timer,
            ft.Text(""),
            switcher,
            controller,
            ft.Text(""),
            ft.Row(
                controls=[
                    author.button(page, box),
                    about.button(page, box),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
    )


async def main(page: ft.Page):
    """Головна функція запуску застосунку"""

    async def route_change():
        """Обробник перемикання екранів"""

        if box.analytics:
            page.run_task(
                box.analytics.log_event,
                box.client_id,
                "route_change",
                platform=str(page.platform.value),
                page_path=page.route,
            )

        if box.ui_update_task:
            box.ui_update_task.cancel()

        page.views.clear()
        page.views.append(build_main_view(page, box))
        match page.route:
            case settings.ROUTE:
                page.views.append(settings.build_view(page, box))
            case author.ROUTE:
                page.views.append(author.build_view(page, box))
            case about.ROUTE:
                page.views.append(about.build_view(page, box))
            case _:
                if page.route != root.ROUTE:
                    page.views.append(error404.build_view(page, box))

        page.update()

    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    async def _check_time():
        """Головний фоновий обробник автоматичного спрацювання мелодії"""

        box.global_task_is_running = True

        while True:
            hours, minutes, seconds = utils.check_delta(**box.alarm_time)

            if box.alarm_on and hours == minutes == seconds == 0:
                await box.audio.play()

            box.time_left = f"{hours:02}:{minutes:02}:{seconds:02}"

            await asyncio.sleep(1)

    async def _state_change(event: fta.AudioStateChangeEvent | None):
        """Обробник зміни статусу програвання мелодії"""

        box.audio_state = event.state

        match event.state:
            case fta.AudioState.COMPLETED:
                if box.repeat:
                    await box.audio.play()

    def _create_audio() -> fta.Audio:
        """Створення об'єкта плеєра"""

        return fta.Audio(
            src=playlist[box.track_name],
            autoplay=False,
            release_mode=fta.ReleaseMode.STOP,
            volume=box.volume,
            balance=0,
            on_state_change=lambda e: asyncio.create_task(_state_change(e)),
        )

    async def _init() -> None:
        """Стартова ініціалізація змінних"""

        async def __init_obj(name: str, default_value: object):
            """Допоміжна функція ініціалізації об'єктів,
            зчитування налаштувань з кешу"""

            value = await box.storage.get_or_default(name, default_value)
            setattr(box, name, value)

        await __init_obj("alarm_time", default.settings.alarm_time.copy())
        await __init_obj("track_name", default.settings.track)
        await __init_obj("alarm_on", True)
        await __init_obj("volume", default.settings.volume)
        await __init_obj("client_id", str(uuid.uuid4()))
        await __init_obj("repeat", default.settings.repeat)

        box.time_left = "23:59:59"
        box.ui_update_task = None
        box.global_task_is_running = False
        box.audio_state = None

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    box = PandorasBox(
        storage=FletStorage(app.settings.name),
        analytics=MeasurementAPI(
            **ga_config.settings.model_dump(),
        ),
    )

    await _init()

    box.audio = _create_audio()

    locale = await box.storage.get_or_default("locale", default.settings.locale)
    box.lang = FluentManager([locale], str(app.settings.locales_dir))

    if not box.global_task_is_running:
        page.run_task(_check_time)

    page.title = box.lang.get("main-title")

    page.theme_mode = ft.ThemeMode.DARK
    page.route = root.ROUTE

    await route_change()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
