# -*- coding: utf-8 -*-

import json

import flet as ft

from utils.config import APP_NAME


async def save_dict(name: str, the_dict: dict) -> None:
    name_dict = f"{APP_NAME}.{name}"
    dict_json = json.dumps(the_dict)

    await ft.SharedPreferences().set(name_dict, dict_json)


async def load_dict(name: str) -> dict:

    name_dict = f"{APP_NAME}.{name}"

    is_contains = await ft.SharedPreferences().contains_key(name_dict)

    if is_contains:
        dict_json = await ft.SharedPreferences().get(name_dict)
        the_dict = json.loads(dict_json)
        return the_dict
    else:
        return {}


async def clear() -> None:

    # keys = await ft.SharedPreferences().get_keys("")
    # print(keys)

    await ft.SharedPreferences().clear()

    # keys = await ft.SharedPreferences().get_keys("")
    # print(keys)
