import enum

import peewee

from .base_model import BaseModel


class Key(enum.StrEnum):
    MUSIC_DIR = "music_dir"
    PLAYLIST = "playlist"
    VOLUME = "volume"


class Setting(BaseModel):
    key = peewee.CharField(unique=True)
    value = peewee.CharField()

    def __str__(self) -> str:
        return f"{self.key} = {self.value}"

    @staticmethod
    def upsert(key: Key, value: str) -> "Setting":
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
        """Get setting with it's key. If not foundreturns default value."""

        try:
            s = Setting.get(Setting.key == key)

            return s.value

        except peewee.DoesNotExist:
            return default_value
