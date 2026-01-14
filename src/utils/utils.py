# -*- coding: utf-8 -*-

from datetime import datetime, timedelta


def check_delta(hours, minutes, seconds) -> tuple[int, int, int]:

    now = datetime.now()
    alarm_time = now.replace(hour=hours, minute=minutes, second=seconds, microsecond=0)

    if alarm_time < now:
        alarm_time += timedelta(days=1)

    delta = alarm_time - now
    total_seconds = int(delta.total_seconds())

    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60

    return h, m, s


def clamp_value(
    value: int | float, min_value: int | float | None, max_value: int | float | None
) -> int | float:
    """Обмеження значення між min та max.
    Якщо щось обмежувати не треба -- передаємо None"""

    if min_value is not None:
        value = max(value, min_value)
    if max_value is not None:
        value = min(value, max_value)
    return value
