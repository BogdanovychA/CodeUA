# -*- coding: utf-8 -*-

import os
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):

    @staticmethod
    def get_asset_dir() -> Path:
        default_assets_dir = Path(__file__).resolve().parent.parent / "assets"
        return Path(os.environ.get("FLET_ASSETS_DIR", default_assets_dir)).resolve()

    name: str = "CodeUA"
    version: str = "1.2.0"

    base_url: str = ""
    assets_dir: Path = get_asset_dir()


settings = Settings()
