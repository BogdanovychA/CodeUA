# -*- coding: utf-8 -*-

import os
from importlib.metadata import metadata
from pathlib import Path

from pydantic import BaseModel

meta = metadata("codeua")


class Settings(BaseModel):

    @staticmethod
    def get_asset_dir() -> Path:
        default_assets_dir = Path(__file__).resolve().parent.parent / "assets"
        return Path(os.environ.get("FLET_ASSETS_DIR", default_assets_dir)).resolve()

    name: str = meta["name"]
    version: str = meta["version"]

    base_url: str = ""
    assets_dir: Path = get_asset_dir()
    locales_dir: Path = assets_dir / "locales"


settings = Settings()
