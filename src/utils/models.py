# -*- coding: utf-8 -*-

from enum import Enum


class Track(Enum):
    """Назви треків"""

    MOMENT = "moment"
    ANTHEM = "anthem"


class Bool(Enum):
    """Текстове представлення True/False"""

    TRUE = "true"
    FALSE = "false"
