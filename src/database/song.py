import peewee

from .album import Album
from .artist import Artist
from .base_model import BaseModel
from .genre import Genre


class Song(BaseModel):
    track = peewee.IntegerField(null=True)
    track_total = peewee.IntegerField(null=True)
    name = peewee.CharField(null=True)
    genre = peewee.ForeignKeyField(Genre, backref="songs", null=True)
    album = peewee.ForeignKeyField(Album, backref="songs", null=True)
    disk = peewee.IntegerField(null=True)
    disk_total = peewee.IntegerField(null=True)
    artist = peewee.ForeignKeyField(Artist, backref="songs", null=True)
    year = peewee.IntegerField(null=True)
    duration = peewee.IntegerField()
    status = peewee.IntegerField()
    file_path = peewee.CharField(unique=True, index=True)
    file_mtime = peewee.IntegerField()
    file_size = peewee.IntegerField()

    def set_active(self) -> None:
        self.status = 1
        self.save()

        if self.artist is not None:
            self.artist.set_active()

        if self.album is not None:
            self.album.set_active()

        if self.genre is not None:
            self.genre.set_active()

    @staticmethod
    def upsert(
        track: int | None,
        track_total: int | None,
        name: str | None,
        genre: Genre | None,
        album: Album | None,
        disk: int | None,
        disk_total: int | None,
        artist: Artist | None,
        year: int | None,
        duration: int,
        file_path: str,
        file_mtime: int,
        file_size: int,
    ) -> "Song":
        clause = (Song.file_path == file_path,)
        count = Song.select().where(*clause).count()

        if count == 0:
            result = Song.create(
                track=track,
                track_total=track_total,
                name=name,
                genre=genre,
                album=album,
                disk=disk,
                disk_total=disk_total,
                artist=artist,
                year=year,
                duration=duration,
                status=1,
                file_path=file_path,
                file_mtime=file_mtime,
                file_size=file_size,
            )
        else:
            result = Song.get(*clause)
            result.track = track
            result.track_total = track
            result.name = name
            result.genre = genre
            result.album = album
            result.disk = disk
            result.disk_total = disk_total
            result.year = year
            result.duration = duration
            result.artist = artist
            result.file_mtime = file_mtime
            result.file_size = file_size
            result.save()

        return result

    @staticmethod
    def get_file_mtime(file_path: str) -> int:
        try:
            s = Song.get(Song.file_path == file_path)

            # if we find a song, we set it (and its liks) active
            s.set_active()
        except peewee.DoesNotExist:
            return -1

        return s.file_mtime

    def __str__(self) -> str:
        return f"{self.track:3} - {self.name} | {self.artist}"
