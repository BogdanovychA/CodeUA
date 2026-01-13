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


def is_int(value) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False
