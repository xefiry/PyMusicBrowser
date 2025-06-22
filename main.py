import os
import pathlib
import time
from datetime import datetime

import peewee
from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError

# DIR_LIST = ["D:/Music/Compilations/", "D:/Music/Röyksopp/", "D:/Music/Black Sabbath/", "D:/Music/musicForProgramming/"]
DIR_LIST = ["D:/Music/"]
DATABASE_FILE = "library.db"

db: peewee.SqliteDatabase = peewee.SqliteDatabase(DATABASE_FILE)


def timeit(func):
    def wrapper(*arg):
        t = time.time()
        res = func(*arg)
        t = round(time.time() - t, 5)
        print(f"{func.__name__} : {t}s")
        return res

    return wrapper


def get_str(data: EasyID3, key: str, value_if_none: str | None = None) -> str | None:
    value = data.get(key)

    if value is None:
        return value_if_none
    else:
        return value[0]


def get_numbers(data: EasyID3, key: str) -> tuple[int | None, int | None]:
    value = data.get(key)

    if value is None:
        return (None, None)

    split = value[0].split("/")

    if len(split) == 1:
        return (split[0], None)
    else:
        return (split[0], split[1])


def get_year(data: EasyID3, key: str) -> int | None:
    value = data.get(key)

    if value is None:
        return None

    value = value[0]

    if value.isnumeric():
        return int(value)

    try:
        date = datetime.strptime(value, "%Y-%m-%d")
        return date.year
    except ValueError:
        return None


class Album(peewee.Model):
    name = peewee.CharField(null=True)
    year = peewee.IntegerField(null=True)
    status = peewee.IntegerField()

    class Meta:
        database = db

    @staticmethod
    def upsert(name: str | None, year: int | None) -> "Album|None":
        if name is None:
            return None

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
    status = peewee.IntegerField()
    file_path = peewee.CharField(unique=True, index=True)
    file_mtime = peewee.IntegerField()

    class Meta:
        database = db

    @staticmethod
    def upsert(
        track: int | None,
        name: str | None,
        genre: Genre | None,
        album: Album | None,
        artist: str | None,
        file_path: str,
        file_mtime: int,
    ) -> "Song":
        clause = (Song.file_path == file_path,)
        count = Song.select().where(*clause).count()

        if count == 0:
            result = Song.create(
                track=track,
                name=name,
                genre=genre,
                album=album,
                artist=artist,
                status=1,
                file_path=file_path,
                file_mtime=file_mtime,
            )
        else:
            result = Song.get(*clause)
            result.track = track
            result.name = name
            result.genre = genre
            result.album = album
            result.artist = artist
            result.status = 1
            result.file_mtime = file_mtime
            result.save()

        return result

    @staticmethod
    def get_file_mtime(file_path: str) -> int:
        try:
            s = Song.get(Song.file_path == file_path)
            s.status = 1
            s.save()
        except peewee.DoesNotExist:
            return -1

        return s.file_mtime


@timeit
def scan_dir(path: str):
    print(f"Scanning {path}")
    for root, dirs, files in os.walk(path):
        for file in files:
            if pathlib.Path(file).suffix == ".mp3":
                song_file = os.path.normpath(os.path.join(root, file))
                file_mtime = int(os.stat(song_file).st_mtime)
                stored_mtime = Song.get_file_mtime(song_file)

                if file_mtime != stored_mtime:
                    try:
                        tag = EasyID3(song_file)
                    except ID3NoHeaderError:
                        tag = EasyID3()

                    _track, _track_total = get_numbers(tag, "tracknumber")
                    _albumartist = get_str(tag, "albumartist")
                    _disk, _disk_total = get_numbers(tag, "discnumber")

                    genre = Genre.upsert(get_str(tag, "genre"))
                    album = Album.upsert(get_str(tag, "album"), get_year(tag, "date"))

                    Song.upsert(
                        _track,
                        get_str(tag, "title", "<unknown>"),
                        genre,
                        album,
                        get_str(tag, "artist"),
                        song_file,
                        file_mtime,
                    )


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

    db.execute_sql("VACUUM;")


if __name__ == "__main__":
    main()
