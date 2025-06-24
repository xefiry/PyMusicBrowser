import peewee

from .artist import Artist
from .base_model import BaseModel


class Album(BaseModel):
    name = peewee.CharField(null=True)
    artist = peewee.ForeignKeyField(Artist, backref="albums", null=True)
    year = peewee.IntegerField(null=True)
    status = peewee.IntegerField()

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

        clause = (Album.name == name, Album.artist == artist)
        count = Album.select().where(*clause).count()

        if count == 0:
            result = Album.create(name=name, artist=artist, year=year, status=1)
        else:
            result = Album.get(*clause)
            if year is not None:
                result.year = min(result.year, year)
            result.save()

        return result

    def __str__(self) -> str:
        return f"[{self.get_id()}] {self.name} ({self.year}) {self.artist}"
