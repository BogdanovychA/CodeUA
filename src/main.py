# -*- coding: utf-8 -*-

import asyncio

import flet as ft
import flet_audio as fta

from routes import about, error404, root, settings
from utils import elements, storage, utils
from utils.config import DEFAULT_ALARM_TIME, DEFAULT_TRACK, TEXT_SIZE, playlist
from utils.models import Track

global_task_is_running = False


def build_main_view(page: ft.Page, audio: fta.Audio) -> ft.View:

    async def _play():
        player_control[2] = pause_button
        controller.update()
        await audio.play()

    async def _pause():
        player_control[2] = resume_button
        controller.update()
        await audio.pause()

    async def _resume():
        player_control[2] = pause_button
        controller.update()
        await audio.resume()

    def _set_volume(value: float):
        nonlocal volume_level
        audio.volume = utils.clamp_value(audio.volume + value, 0, 1)
        volume_level = int(audio.volume * 100)
        switcher.label = f"Гучність: {volume_level}%"
        switcher.update()

    async def _switch():
        await _pause()
        page.session.store.set("track_name", switcher.value)
        audio.src = playlist[switcher.value]

    async def _update_timer():

        while True:

            timer.value = page.session.store.get("time_left")
            timer.update()
            await asyncio.sleep(1)

    track_name = page.session.store.get("track_name")

    volume_level = int(audio.volume * 100)

    switcher = ft.Dropdown(
        label=f"Гучність: {volume_level}%",
        label_style=ft.TextStyle(size=TEXT_SIZE),
        value=track_name,
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

    page.update_timer_task = page.run_task(_update_timer)

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
                "До вшанування пам'яті\nзагиблих героїв залишилося:", size=TEXT_SIZE
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

    def route_change():

        if page.update_timer_task:
            page.update_timer_task.cancel()

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

        global global_task_is_running
        global_task_is_running = True

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

    page.update_timer_task = None
    page.time_left = None

    if not global_task_is_running:
        page.run_task(_check_time)

    route_change()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
