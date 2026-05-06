# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import asyncio

    import flet_audio as fta
    from flet_storage import FletStorage
    from fluent_manager import FluentManager


class Track(StrEnum):
    """Назви треків"""

    MOMENT = "moment"
    ANTHEM = "anthem"
    ANTHEM_2 = "anthem_2"


class Bool(StrEnum):
    """Текстове представлення True/False"""

    TRUE = "true"
    FALSE = "false"


@dataclass
class PandorasBox:
    """Контейнер стану застосунку"""

    storage: FletStorage
    lang: FluentManager | None = None
    audio: fta.Audio | None = None

    # State variables
    audio_state: fta.AudioState | None = None
    repeat: bool = False
    track_name: Track = Track.MOMENT
    time_left: str = "23:59:59"
    alarm_on: bool = True
    alarm_time: dict | None = None
    volume: float = 0.5
    client_id: str = ""
    ui_update_task: asyncio.Task | None = None
    global_task_is_running: bool = False
