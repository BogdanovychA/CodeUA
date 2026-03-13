# -*- coding: utf-8 -*-

from pydantic_settings import BaseSettings, SettingsConfigDict

from config import app


class Settings(BaseSettings):
    secret_key: str | None = None
    id: str | None = None
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=app.settings.base_dir / ".env",
        env_prefix="GOOGLE_ANALYTICS__",
        extra="ignore",
    )


settings = Settings()
