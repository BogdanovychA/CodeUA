# -*- coding: utf-8 -*-

from enum import StrEnum


class Track(StrEnum):
    """Назви треків"""

    MOMENT = "moment"
    ANTHEM = "anthem"
    ANTHEM_2 = "anthem_2"


class Bool(StrEnum):
    """Текстове представлення True/False"""

    TRUE = "true"
    FALSE = "false"
