import peewee

from . import utils
from .base_model import BaseModel


class Artist(BaseModel):
    name = peewee.CharField(unique=True)
    status = peewee.IntegerField()

    def __str__(self) -> str:
        return f"{self.name}"

    def set_active(self) -> None:
        self.status = 1
        self.save()

    def match(self, input: str) -> bool:
        return input == "" or utils.match_str(self.name, input)

    @staticmethod
    def upsert(name: str | None) -> "Artist|None":
        if name is None:
            return None

        artist = Artist.select().where(Artist.name == name)

        if artist.exists():
            result = artist.get()
        else:
            result = Artist.create(name=name, status=1)

        return result
