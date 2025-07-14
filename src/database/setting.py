import enum

import peewee

from .base_model import BaseModel


class Key(enum.StrEnum):
    MUSIC_DIR = "music_dir"
    PLAYLIST = "playlist"
    VOLUME = "volume"


class Setting(BaseModel):
    key = peewee.CharField(unique=True)
    value = peewee.CharField(null=True)

    def __str__(self) -> str:
        return f"{self.key} = {self.value}"

    @staticmethod
    def upsert(key: Key, value: str | None) -> "Setting":
        setting = Setting.select().where(Setting.key == key)

        if setting.exists():
            result = setting.get()
            result.value = value
            result.save()
        else:
            result = Setting.create(key=key, value=value)

        return result

    @staticmethod
    def get_value(key: Key, default_value: str = "") -> str:
        """Get setting with it's key. If not found or None, returns default value."""

        try:
            s = Setting.get(Setting.key == key)

            if s.value is not None:
                return s.value
            else:
                return default_value

        except peewee.DoesNotExist:
            return default_value
