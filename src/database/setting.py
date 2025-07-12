import peewee

from .base_model import BaseModel


class Setting(BaseModel):
    name = peewee.CharField(unique=True)
    value = peewee.CharField(null=True)

    def __str__(self) -> str:
        return f"{self.name} = {self.value}"

    @staticmethod
    def upsert(name: str, value: str | None) -> "Setting":
        setting = Setting.select().where(Setting.name == name)

        if setting.exists():
            result = setting.get()
            result.value = value
            result.save()
        else:
            result = Setting.create(name=name, value=value)

        return result

    @staticmethod
    def get_value(name: str, default_value: str = "") -> str:
        """Get setting with it's name. If not found or None, returns default value."""

        try:
            s = Setting.get(Setting.name == name)

            if s.value is not None:
                return s.value
            else:
                return default_value

        except peewee.DoesNotExist:
            return default_value
