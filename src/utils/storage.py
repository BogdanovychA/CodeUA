# -*- coding: utf-8 -*-

import json

import flet as ft


async def save(name: str, app_name: str, obj: object) -> None:
    """Зберегти налаштування в кеш"""

    name_obj = f"{app_name}.{name}"
    obj_json = json.dumps(obj)

    await ft.SharedPreferences().set(name_obj, obj_json)


async def load(name: str, app_name: str) -> object:
    """Зчитати налаштування з кешу"""

    obj_json = await ft.SharedPreferences().get(f"{app_name}.{name}")
    obj = json.loads(obj_json)

    return obj


async def clear() -> None:
    """Очистка кешу"""

    await list_keys()
    await ft.SharedPreferences().clear()
    await list_keys()


async def list_keys() -> None:
    """Лістинг всіх збережених даних в кеші"""

    keys = await ft.SharedPreferences().get_keys("")
    print(keys)
