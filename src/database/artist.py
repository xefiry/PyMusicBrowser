import peewee

from .base_model import BaseModel


class Artist(BaseModel):
    name = peewee.CharField(unique=True)
    status = peewee.IntegerField()

    def set_active(self) -> None:
        self.status = 1
        self.save()

    @staticmethod
    def upsert(name: str | None) -> "Artist|None":
        if name is None:
            return None

        clause = (Artist.name == name,)
        count = Artist.select().where(*clause).count()

        if count == 0:
            result = Artist.create(
                name=name,
                status=1,
            )
        else:
            result = Artist.get(*clause)
            result.save()

        return result

    def __str__(self) -> str:
        return f"{self.name}"
