# -*- coding: utf-8 -*-

import asyncio

import flet as ft
import flet_audio as fta

from routes import about, error404, root, settings
from utils import elements
from utils.config import TEXT_SIZE

playlist = {
    "anthem": "/sounds/anthem_of_Ukraine.ogx",
    "moment": "/sounds/moment_of_silence.mp3",
}


def build_main_view(page: ft.Page) -> ft.View:

    async def _play():
        player_control[2] = pause_button
        await audio.play()

    async def _pause():
        player_control[2] = resume_button
        await audio.pause()

    async def _resume():
        player_control[2] = pause_button
        await audio.resume()

    def _set_volume(value: float):
        audio.volume += value

    async def _switch(event: ft.Event):
        await _pause()
        audio.src = playlist[switcher.value]
        event.page.update()

    switcher = ft.Dropdown(
        label="Композиція",
        label_style=ft.TextStyle(size=TEXT_SIZE),
        value="moment",
        options=[
            ft.DropdownOption(key="moment", text="Хвилина мовчання"),
            ft.DropdownOption(key="anthem", text="Гімн України"),
        ],
        on_select=_switch,
    )

    play_button = ft.IconButton(ft.Icons.PLAY_ARROW_ROUNDED, on_click=_play)
    pause_button = ft.IconButton(ft.Icons.STOP_ROUNDED, on_click=_pause)
    resume_button = ft.IconButton(ft.Icons.PLAY_CIRCLE_OUTLINED, on_click=_resume)
    volume_plus_button = ft.IconButton(
        ft.Icons.VOLUME_DOWN_ROUNDED, on_click=lambda _: _set_volume(-0.1)
    )
    volume_minus_button = ft.IconButton(
        ft.Icons.VOLUME_UP_ROUNDED, on_click=lambda _: _set_volume(0.1)
    )

    player_control = [
        volume_plus_button,
        play_button,
        resume_button,
        volume_minus_button,
    ]

    audio = fta.Audio(
        src=playlist[switcher.value],
        autoplay=False,
        volume=1,
        balance=0,
        # on_loaded=lambda _: print("Loaded"),
        # on_duration_change=lambda e: print("Duration changed:", e.duration),
        # on_position_change=lambda e: print("Position changed:", e.position),
        # on_state_change=lambda e: print("State changed:", e.state),
        # on_seek_complete=lambda _: print("Seek complete"),
    )

    page.title = root.TITLE
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
            ft.Text("", size=TEXT_SIZE),
            switcher,
            ft.Text(""),
            ft.Row(
                controls=player_control,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(""),
            ft.Button(
                settings.TITLE,
                on_click=lambda: asyncio.create_task(page.push_route(settings.ROUTE)),
            ),
            ft.Text(""),
            about.button(page),
        ],
    )


def main(page: ft.Page):
    page.title = root.TITLE
    page.theme_mode = ft.ThemeMode.DARK
    page.route = root.ROUTE

    def route_change():
        page.views.clear()
        page.views.append(build_main_view(page))
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

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
