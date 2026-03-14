# -*- coding: utf-8 -*-

import os

from fluent.runtime import FluentLocalization, FluentResourceLoader

from config import app, default


class LocaleManager:
    default_locale = default.settings.locale
    base_path = app.settings.assets_dir / "locales"
    loader = FluentResourceLoader([base_path / "{locale}"])
    languages = os.listdir(base_path)
    resource_ids = [
        f for f in os.listdir(base_path / default_locale) if f.endswith(".ftl")
    ]

    def __init__(self, locale):
        self.locale = locale

        self.l10n = FluentLocalization(
            [self.locale, self.default_locale], [*self.resource_ids], self.loader
        )

    @classmethod
    def create_manager(cls, locale: str):
        return cls(locale)

    def get(self, key, **kwargs) -> str:
        return self.l10n.format_value(key, kwargs)


if __name__ == "__main__":

    lang_manager = LocaleManager.create_manager("en")

    print(lang_manager.languages)

    test_msg = lang_manager.get(
        "test-message",
        user_name="Andrii",
        tasks_count=1,
    )
    print(test_msg)
