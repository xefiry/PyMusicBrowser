import peewee

from .artist import Artist
from .base_model import BaseModel
from . import utils


class Album(BaseModel):
    name = peewee.CharField(null=True)
    artist = peewee.ForeignKeyField(Artist, backref="albums", null=True)
    year = peewee.IntegerField(null=True)
    status = peewee.IntegerField()

    def __str__(self) -> str:
        return f"{self.name} ({self.year}) {self.artist}"

    def set_active(self) -> None:
        self.status = 1
        self.save()

        if self.artist is not None:
            self.artist.set_active()

    def match(self, input: str) -> bool:
        return (
            input == ""
            or utils.match_str(self.name, input)
            or utils.match_int(self.year, input)
            or (self.artist is not None and self.artist.match(input))
        )

    @staticmethod
    def upsert(
        name: str | None, artist: Artist | None, year: int | None
    ) -> "Album|None":
        if name is None:
            return None

        album = Album.select().where(Album.name == name, Album.artist == artist)

        if album.exists():
            result = album.get()
            if year is not None:
                result.year = min(result.year, year)
            result.save()
        else:
            result = Album.create(name=name, artist=artist, year=year, status=1)

        return result
