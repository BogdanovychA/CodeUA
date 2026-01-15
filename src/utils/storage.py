# -*- coding: utf-8 -*-

import json

import flet as ft

from utils.config import APP_NAME


async def save(name: str, obj: object) -> None:

    name_obj = f"{APP_NAME}.{name}"
    obj_json = json.dumps(obj)

    await ft.SharedPreferences().set(name_obj, obj_json)


async def load(name: str) -> object:

    name_obj = f"{APP_NAME}.{name}"

    is_contains = await ft.SharedPreferences().contains_key(name_obj)

    if is_contains:
        obj_json = await ft.SharedPreferences().get(name_obj)
        obj = json.loads(obj_json)
        return obj
    else:
        return None


async def clear() -> None:

    # await list_keys()

    await ft.SharedPreferences().clear()

    # await list_keys()


async def list_keys() -> None:
    keys = await ft.SharedPreferences().get_keys("")
    print(keys)
