import time

import peewee
from tinytag import TinyTag

SONG_LIST = [
    "D:/Music/Compilations/Good music/Brutal Truth - Blue world.mp3",
    "D:/Music/Compilations/Good music/Iggy Pop & Goran Bregovic - In the death car (Arizona dream).mp3",
    "D:/Music/Dimmu Borgir/1996 - Stormblåst/02 - Broderskapets ring.mp3",
    "D:/Music/Röyksopp/2022 - Profound mysteries I/01 - (Nothing but) ashes….mp3",
    "D:/Music/Röyksopp/2022 - Profound mysteries II/01 - Denimclad baboons.mp3",
    "D:/Music/Röyksopp/2014 - The inevitable end/CD 1/01 - Skulls.mp3",
]

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
    name = peewee.CharField()
    year = peewee.IntegerField()
    status = peewee.IntegerField()

    class Meta:
        database = db

    @staticmethod
    @timeit
    def create_or_update(name: str, year: int) -> "Album":
        count = Album.select().where(Album.name == name).count()

        if count == 0:
            result = Album.create(name=name, year=year, status=1)
        else:
            result = Album.get(Album.name == name)
            result.year = year
            result.status = 1
            result.save()

        return result

    @staticmethod
    def print_all() -> None:
        print("List of Album")
        for album in Album.select():
            print(album.__data__)


class Song(peewee.Model):
    track = peewee.IntegerField()
    name = peewee.CharField(null=True)
    album = peewee.ForeignKeyField(Album, backref="songs", null=True)
    artist = peewee.CharField(null=True)
    filepath = peewee.CharField(unique=True, index=True)
    status = peewee.IntegerField()

    class Meta:
        database = db

    @staticmethod
    @timeit
    def create_or_update(
        track: int, name: str, album: Album, artist: str, filepath: str
    ) -> "Song":
        count = Song.select().where(Song.filepath == filepath).count()

        if count == 0:
            # print(f"Created song : {track} - {name}")
            result = Song.create(
                track=track,
                name=name,
                album=album,
                artist=artist,
                filepath=filepath,
                status=1,
            )
        else:
            # print(f"Updated song : {track} - {name}")
            result = Song.get(Song.filepath == filepath)
            result.track = track
            result.name = name
            result.album = album
            result.artist = artist
            result.status = 1
            result.save()

        return result

    @staticmethod
    def print_all() -> None:
        print("List of Song")
        for song in Song.select():
            print(song.__data__)


@timeit
def do_db_insert():
    with db.transaction():
        for song in SONG_LIST:
            tag = TinyTag.get(song)
            album = Album.create_or_update(tag.album, tag.year)

            Song.create_or_update(tag.track, tag.title, album, tag.artist, song)


def main():
    db.connect()
    # db.drop_tables([Album, Song])  # ToDo: remove this line (here only for tests)
    db.create_tables([Album, Song])

    db.execute_sql("PRAGMA journal_mode = off;")
    db.execute_sql("PRAGMA synchronous = 0;")

    db.execute_sql("UPDATE song  SET status = 0;")
    db.execute_sql("UPDATE album SET status = 0;")

    for pragma in ["journal_mode", "synchronous"]:
        for r in db.execute_sql(f"PRAGMA {pragma};"):
            print(f"{pragma} - {r[0]}")

    do_db_insert()

    Album.print_all()
    Song.print_all()

    db.execute_sql("DELETE FROM song  WHERE status = 0;")
    db.execute_sql("DELETE FROM album WHERE status = 0;")

    Album.print_all()
    Song.print_all()


if __name__ == "__main__":
    main()
