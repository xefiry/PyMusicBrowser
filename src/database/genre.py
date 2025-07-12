import peewee

from .base_model import BaseModel


class Genre(BaseModel):
    name = peewee.CharField(unique=True)
    status = peewee.IntegerField()

    def __str__(self) -> str:
        return f"{self.name}"

    def set_active(self) -> None:
        self.status = 1
        self.save()

    @staticmethod
    def upsert(name: str | None) -> "Genre|None":
        if name is None:
            return None

        genre = Genre.select().where(Genre.name == name)

        if genre.exists():
            result = genre.get()
        else:
            result = Genre.create(name=name, status=1)

        return result
