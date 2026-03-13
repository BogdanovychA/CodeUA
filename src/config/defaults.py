# -*- coding: utf-8 -*-

from pydantic import BaseModel

from utils.models import Track


class BotSettings(BaseModel):
    alarm_time: dict[str, int] = {
        "hours": 9,
        "minutes": 0,
        "seconds": 0,
    }

    track: Track = Track.MOMENT
    volume: float = 0.5
    repeat: bool = False


settings = BotSettings()
