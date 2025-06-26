import peewee

from .base_model import BaseModel


class Genre(BaseModel):
    name = peewee.CharField(unique=True)
    status = peewee.IntegerField()

    def set_active(self) -> None:
        self.status = 1
        self.save()

    @staticmethod
    def upsert(name: str | None) -> "Genre|None":
        if name is None:
            return None

        clause = (Genre.name == name,)
        count = Genre.select().where(*clause).count()

        if count == 0:
            result = Genre.create(
                name=name,
                status=1,
            )
        else:
            result = Genre.get(*clause)
            result.save()

        return result

    def __str__(self) -> str:
        return f"{self.name}"
