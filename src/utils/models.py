# -*- coding: utf-8 -*-

from enum import Enum


class Track(Enum):
    """Назви треків"""

    MOMENT = "moment"
    ANTHEM = "anthem"
    ANTHEM_2 = "anthem_2"


class Bool(Enum):
    """Текстове представлення True/False"""

    TRUE = "true"
    FALSE = "false"
