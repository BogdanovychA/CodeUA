# -*- coding: utf-8 -*-

import asyncio

import flet as ft
import flet_audio as fta

from routes import about, error404, root, settings
from utils import elements, storage, utils
from utils.config import (
    APP_NAME,
    DEFAULT_ALARM_TIME,
    DEFAULT_TRACK,
    DEFAULT_VOLUME,
    TEXT_SIZE,
    playlist,
)
from utils.models import Track


def build_main_view(page: ft.Page, audio: list[fta.Audio]) -> ft.View:
    """Головний екран застосунку"""

    async def _play():
        """Обробник натискання кнопки play"""

        audio_state = page.session.store.get("audio_state")
        match audio_state:
            case fta.AudioState.PAUSED:
                await audio[0].resume()
            case fta.AudioState.DISPOSED:  # audio player has been disposed
                pass
            case _:
                await audio[0].play()

    async def _stop():
        """Обробник натискання кнопки stop"""

        await audio[0].pause()
        await audio[0].seek(ft.Duration(0))

    async def _pause():
        """Обробник натискання кнопки pause"""

        await audio[0].pause()

    # async def _resume():
    #     await audio[0].resume()

    async def _set_volume(value: float):
        """Обробник кнопок зміни гучності"""

        audio[0].volume = utils.clamp_value(audio[0].volume + value, 0, 1)
        await storage.save("volume", audio[0].volume)
        switcher.label = f"Рівень гучності: {int(audio[0].volume * 100)}%"
        switcher.update()

    async def _switch():
        """Обробник зміни треків"""

        await _pause()
        page.session.store.set("track_name", switcher.value)
        await storage.save("track_name", switcher.value)
        audio[0].src = playlist[switcher.value]

    async def _ui_update():
        """Фоновий таск оновлення інтерфейсу"""

        while True:
            time_left = page.session.store.get("time_left")
            if timer.value != time_left:
                timer.value = time_left
                timer.update()

            if page.session.store.get("alarm_on"):
                if timer.style.color != ft.Colors.PRIMARY:
                    timer.style.color = ft.Colors.PRIMARY
                    timer.update()
            else:
                if timer.style.color != ft.Colors.ON_PRIMARY:
                    timer.style.color = ft.Colors.ON_PRIMARY
                    timer.update()

            audio_state = page.session.store.get("audio_state")
            match audio_state:
                case fta.AudioState.PLAYING:
                    if player_control[1] != pause_button:
                        player_control[1] = pause_button
                        controller.update()

                case fta.AudioState.DISPOSED:  # audio player has been disposed
                    pass

                case _:
                    if player_control[1] != play_button:
                        player_control[1] = play_button
                        controller.update()

            await asyncio.sleep(0.5)

    switcher = ft.Dropdown(
        label=f"Рівень гучності: {int(audio[0].volume * 100)}%",
        label_style=ft.TextStyle(size=TEXT_SIZE),
        value=page.session.store.get("track_name"),
        options=[
            ft.DropdownOption(key=Track.MOMENT.value, text="Хвилина мовчання"),
            ft.DropdownOption(key=Track.ANTHEM.value, text="Гімн України"),
        ],
        on_select=_switch,
    )

    timer = ft.Text(
        "",
        size=TEXT_SIZE,
        style=ft.TextStyle(
            color=(
                ft.Colors.PRIMARY
                if page.session.store.get("alarm_on")
                else ft.Colors.ON_PRIMARY
            ),
            weight=ft.FontWeight.BOLD,
        ),
    )

    play_button = ft.IconButton(ft.Icons.PLAY_ARROW_ROUNDED, on_click=_play)
    pause_button = ft.IconButton(ft.Icons.PAUSE_ROUNDED, on_click=_pause)
    stop_button = ft.IconButton(ft.Icons.STOP_ROUNDED, on_click=_stop)
    # resume_button = ft.IconButton(ft.Icons.PLAY_CIRCLE_OUTLINED, on_click=_resume)
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
        stop_button,
        volume_plus_button,
    ]

    controller = ft.Row(
        controls=player_control,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.title = root.TITLE

    _ui_update_task = page.run_task(_ui_update)
    page.session.store.set("_ui_update_task", _ui_update_task)

    return ft.View(
        route=root.ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(root.TITLE, page),
            ft.Text(""),
            ft.Image(
                src="/icon.png",
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text(
                "До вшанування пам'яті загиблих\nГероїв України залишилося:",
                size=TEXT_SIZE,
            ),
            timer,
            ft.Text(""),
            switcher,
            controller,
            ft.Text(""),
            about.button(page),
        ],
    )


async def main(page: ft.Page):
    """Головна функція запуску застосунку"""

    page.title = root.TITLE
    page.theme_mode = ft.ThemeMode.DARK
    page.route = root.ROUTE

    async def route_change():
        """Обробник перемикання екранів"""

        _ui_update_task = page.session.store.get("_ui_update_task")
        if _ui_update_task:
            _ui_update_task.cancel()

        page.views.clear()
        page.views.append(build_main_view(page, audio))
        match page.route:
            case settings.ROUTE:
                page.views.append(settings.build_view(page, audio))
            case about.ROUTE:
                page.views.append(about.build_view(page))
            case _:
                if page.route != root.ROUTE:
                    page.views.append(error404.build_view(page))

        page.update()

    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    async def _check_time():
        """Головний фоновий обробник автоматичного спрацювання мелодії"""

        page.session.store.set("global_task_is_running", True)

        while True:

            alarm_time = page.session.store.get("alarm_time")
            hours, minutes, seconds = utils.check_delta(**alarm_time)

            if page.session.store.get("alarm_on") and hours == minutes == seconds == 0:
                await audio[0].play()

            page.session.store.set("time_left", f"{hours:02}:{minutes:02}:{seconds:02}")

            await asyncio.sleep(1)

    def _state_change(event: fta.AudioStateChangeEvent | None):
        """Обробник зміни статусу програвання мелодії"""

        page.session.store.set("audio_state", event.state)
        # print(page.session.store.get("audio_state"))

        # match event.state:
        #     case fta.AudioState.COMPLETED:
        #         # Якщо трек відіграв, перестворюємо об'єкт
        #         audio[0] = _create_audio()
        #     case fta.AudioState.DISPOSED:
        #         # Перестворюємо об'єкт (для перестраховки :))
        #         audio[0] = _create_audio()
        #     case fta.AudioState.PLAYING:
        #         pass
        #     case fta.AudioState.STOPPED:
        #         pass
        #     case fta.AudioState.PAUSED:
        #         pass
        #     case None:
        #         pass

    def _create_audio() -> fta.Audio:
        """Створення об'єкту плеера"""

        return fta.Audio(
            src=playlist[page.session.store.get("track_name")],
            autoplay=False,
            release_mode=fta.ReleaseMode.STOP,
            volume=page.session.store.get("volume"),
            balance=0,
            # on_state_change=lambda e: asyncio.create_task(_state_change(e)),
            on_state_change=lambda e: _state_change(e),
            # on_loaded=lambda _: print("Loaded"),
            # on_duration_change=lambda e: print("Duration changed:", e.duration),
            # on_position_change=lambda e: print("Position changed:", e.position),
            # on_seek_complete=lambda _: print("Seek complete"),
        )

    async def _init() -> None:
        """Стартова ініціалізація змінних"""

        async def __init_obj(name: str, default_value: object):
            """Допоміжна функція ініціалізації об'єктів,
            зчитування налаштувань з кешу"""

            is_contains = await ft.SharedPreferences().contains_key(
                f"{APP_NAME}.{name}"
            )
            if is_contains:
                value = await storage.load(name)
            else:
                value = default_value
                await storage.save(name, value)

            page.session.store.set(name, value)

        await __init_obj("alarm_time", DEFAULT_ALARM_TIME.copy())
        await __init_obj("track_name", DEFAULT_TRACK)
        await __init_obj("alarm_on", True)
        await __init_obj("volume", DEFAULT_VOLUME)

        page.session.store.set("time_left", "23:59:59")
        page.session.store.set("_ui_update_task", None)
        page.session.store.set("global_task_is_running", False)
        page.session.store.set("audio_state", None)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    await _init()

    # Об'єкт вкладаємо в єдиний елемент списку, щоб мати можливість
    # його перестворювати, не змінюючи посилання на об'єкт
    audio = [_create_audio()]

    global_task_is_running = page.session.store.get("global_task_is_running")
    if not global_task_is_running:
        page.run_task(_check_time)

    await route_change()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
