# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
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

    lang: FluentManager
    audio: fta.Audio
    storage: FletStorage
