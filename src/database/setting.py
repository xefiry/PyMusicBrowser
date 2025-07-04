import peewee

from .base_model import BaseModel


class Setting(BaseModel):
    name = peewee.CharField(unique=True)
    value = peewee.CharField(null=True)

    @staticmethod
    def upsert(name: str, value: str | None) -> "Setting":
        clause = (Setting.name == name,)
        count = Setting.select().where(*clause).count()

        if count == 0:
            result = Setting.create(name=name, value=value)
        else:
            result = Setting.get(*clause)
            result.value = value
            result.save()

        return result

    @staticmethod
    def get_value(name: str) -> str:
        try:
            s = Setting.get(Setting.name == name)

            if s.value is not None:
                return s.value
            else:
                return ""

        except peewee.DoesNotExist:
            return ""

    def __str__(self) -> str:
        return f"{self.name} = {self.value}"
