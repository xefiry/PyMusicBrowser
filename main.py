import os
import pathlib
import time

import peewee
from tinytag import TinyTag

DIR_LIST = ["D:/Music/Compilations/", "D:/Music/Röyksopp/"]
DATABASE_FILE = "library.db"

db: peewee.SqliteDatabase = peewee.SqliteDatabase(DATABASE_FILE)


def timeit(func):
    def wrapper(*arg):
        t = time.time()
        res = func(*arg)
        t = round(time.time() - t, 6)
        print(f"{func.__name__} : {t}")
        return res

    return wrapper


class Album(peewee.Model):
    name = peewee.CharField(null=True)
    year = peewee.CharField(null=True)
    status = peewee.IntegerField()

    class Meta:
        database = db

    @staticmethod
    def upsert(name: str | None, year: str | None) -> "Album":
        clause = (Album.name == name, Album.year == year)
        count = Album.select().where(*clause).count()

        if count == 0:
            result = Album.create(name=name, year=year, status=1)
        else:
            result = Album.get(*clause)
            result.status = 1
            result.save()

        return result


class Genre(peewee.Model):
    name = peewee.CharField(unique=True)
    status = peewee.IntegerField()

    class Meta:
        database = db

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
            result.status = 1
            result.save()

        return result


class Song(peewee.Model):
    track = peewee.IntegerField(null=True)
    name = peewee.CharField(null=True)
    genre = peewee.ForeignKeyField(Genre, backref="songs", null=True)
    album = peewee.ForeignKeyField(Album, backref="songs", null=True)
    artist = peewee.CharField(null=True)
    filepath = peewee.CharField(unique=True, index=True)
    status = peewee.IntegerField()

    class Meta:
        database = db

    @staticmethod
    def upsert(
        track: int | None,
        name: str | None,
        genre: Genre | None,
        album: Album | None,
        artist: str | None,
        filepath: str,
    ) -> "Song":
        clause = (Song.filepath == filepath,)
        count = Song.select().where(*clause).count()

        if count == 0:
            result = Song.create(
                track=track,
                name=name,
                genre=genre,
                album=album,
                artist=artist,
                filepath=filepath,
                status=1,
            )
        else:
            result = Song.get(*clause)
            result.track = track
            result.name = name
            result.genre = genre
            result.album = album
            result.artist = artist
            result.status = 1
            result.save()

        return result


@timeit
def scan_dir(path: str):
    print(f"Scanning {path}")
    for root, dirs, files in os.walk(path):
        for file in files:
            if pathlib.Path(file).suffix == ".mp3":
                song_file = os.path.normpath(os.path.join(root, file))
                tag = TinyTag.get(song_file)
                genre = Genre.upsert(tag.genre)
                album = Album.upsert(tag.album, tag.year)
                Song.upsert(tag.track, tag.title, genre, album, tag.artist, song_file)


def main():
    models = [Album, Genre, Song]

    db.connect()
    # db.drop_tables(models)  # ToDo: remove this line (here only for tests)
    db.create_tables(models)

    db.execute_sql("PRAGMA journal_mode = off;")
    db.execute_sql("PRAGMA synchronous = 0;")

    # Set all data satatus to 0
    for model in models:
        model.update(status=0).execute()

    for pragma in ["journal_mode", "synchronous"]:
        for r in db.execute_sql(f"PRAGMA {pragma};"):
            print(f"{pragma} - {r[0]}")

    # Insert/update data
    for dir in DIR_LIST:
        scan_dir(dir)

    # Delete data with status to 0
    for model in models:
        model.delete().where(model.status == 0).execute()
    # ToDo: do a vacuum


if __name__ == "__main__":
    main()
