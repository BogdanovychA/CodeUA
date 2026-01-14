# -*- coding: utf-8 -*-

import asyncio

import flet as ft
import flet_audio as fta

from routes import about, error404, root, settings
from utils import elements, storage, utils
from utils.config import DEFAULT_ALARM_TIME, DEFAULT_TRACK, TEXT_SIZE, playlist
from utils.models import Track


def build_main_view(page: ft.Page, audio: fta.Audio) -> ft.View:

    async def _play():
        page.session.store.set("track_is_playing", True)
        await audio.play()

    async def _pause():
        page.session.store.set("track_is_playing", False)
        await audio.pause()

    async def _resume():
        page.session.store.set("track_is_playing", True)
        await audio.resume()

    def _set_volume(value: float):

        audio.volume = utils.clamp_value(audio.volume + value, 0, 1)
        switcher.label = f"Рівень гучності: {int(audio.volume * 100)}%"
        switcher.update()

    async def _switch():
        await _pause()
        page.session.store.set("track_name", switcher.value)
        audio.src = playlist[switcher.value]

    async def _ui_update():

        while True:
            if timer.value != page.session.store.get("time_left"):
                timer.value = page.session.store.get("time_left")
                timer.update()

            if page.session.store.get("track_is_playing"):
                if player_control[2] != pause_button:
                    player_control[2] = pause_button
                    controller.update()
            else:
                if player_control[2] != resume_button:
                    player_control[2] = resume_button
                    controller.update()

            duration1 = await audio.get_current_position()

            await asyncio.sleep(0.1)

            duration2 = await audio.get_current_position()

            if duration1 and duration2:
                if (
                    duration1.microseconds != duration2.microseconds
                    or duration1.milliseconds != duration2.milliseconds
                    or duration1.seconds != duration2.seconds
                    or duration1.minutes != duration2.minutes
                ):
                    page.session.store.set("track_is_playing", True)
                    # print("playing")
                else:
                    page.session.store.set("track_is_playing", False)
                    # print("stopped")
            else:
                page.session.store.set("track_is_playing", False)
                # print("stopped")

    switcher = ft.Dropdown(
        label=f"Рівень гучності: {int(audio.volume * 100)}%",
        label_style=ft.TextStyle(size=TEXT_SIZE),
        value=page.session.store.get("track_name"),
        options=[
            ft.DropdownOption(key=Track.MOMENT.value, text="Хвилина мовчання"),
            ft.DropdownOption(key=Track.ANTHEM.value, text="Гімн України"),
        ],
        on_select=_switch,
    )

    timer = ft.Text("", size=TEXT_SIZE)

    play_button = ft.IconButton(ft.Icons.PLAY_ARROW_ROUNDED, on_click=_play)
    pause_button = ft.IconButton(ft.Icons.STOP_ROUNDED, on_click=_pause)
    resume_button = ft.IconButton(ft.Icons.PLAY_CIRCLE_OUTLINED, on_click=_resume)
    volume_minus_button = ft.IconButton(
        ft.Icons.VOLUME_DOWN_ROUNDED, on_click=lambda _: _set_volume(-0.1)
    )
    volume_plus_button = ft.IconButton(
        ft.Icons.VOLUME_UP_ROUNDED, on_click=lambda _: _set_volume(0.1)
    )

    player_control = [
        volume_minus_button,
        play_button,
        resume_button,
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
            elements.app_bar(root.TITLE),
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
            ft.Button(
                settings.TITLE,
                on_click=lambda: asyncio.create_task(page.push_route(settings.ROUTE)),
            ),
            ft.Text(""),
            about.button(page),
        ],
    )


async def main(page: ft.Page):
    page.title = root.TITLE
    page.theme_mode = ft.ThemeMode.DARK
    page.route = root.ROUTE

    async def route_change():

        _ui_update_task = page.session.store.get("_ui_update_task")
        if _ui_update_task:
            _ui_update_task.cancel()

        page.views.clear()
        page.views.append(build_main_view(page, audio))
        match page.route:
            case settings.ROUTE:
                page.views.append(settings.build_view(page))
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

        page.session.store.set("global_task_is_running", True)

        while True:

            alarm_time = page.session.store.get("alarm_time")
            hours, minutes, seconds = utils.check_delta(**alarm_time)

            if hours == minutes == seconds == 0:
                await audio.play()

            page.session.store.set("time_left", f"{hours:02}:{minutes:02}:{seconds:02}")

            await asyncio.sleep(1)

    async def _init() -> None:

        alarm_time = await storage.load_dict("alarm_time")
        if not alarm_time:
            await storage.save_dict("alarm_time", DEFAULT_ALARM_TIME)
            alarm_time = await storage.load_dict("alarm_time")

        page.session.store.set("alarm_time", alarm_time)
        page.session.store.set("track_name", DEFAULT_TRACK)
        page.session.store.set("time_left", "23:59:59")
        page.session.store.set("_ui_update_task", None)
        page.session.store.set("global_task_is_running", False)
        page.session.store.set("track_is_playing", False)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    await _init()

    audio = fta.Audio(
        src=playlist[Track.MOMENT.value],
        autoplay=False,
        volume=0.5,
        balance=0,
        # on_loaded=lambda _: print("Loaded"),
        # on_duration_change=lambda e: print("Duration changed:", e.duration),
        # on_position_change=lambda e: print("Position changed:", e.position),
        # on_state_change=lambda e: print("State changed:", e.state),
        # on_seek_complete=lambda _: print("Seek complete"),
    )

    global_task_is_running = page.session.store.get("global_task_is_running")

    if not global_task_is_running:
        page.run_task(_check_time)

    await route_change()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
