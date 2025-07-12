import peewee

from .artist import Artist
from .base_model import BaseModel


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
