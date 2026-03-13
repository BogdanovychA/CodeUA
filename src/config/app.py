# -*- coding: utf-8 -*-

from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):

    name: str = "CodeUA"
    version: str = "1.2.0"

    base_url: str = ""
    base_dir: Path = Path(__file__).resolve().parent.parent.parent


settings = Settings()
