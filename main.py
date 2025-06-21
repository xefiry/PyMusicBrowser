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

    @timeit
    @staticmethod
    def upsert(name: str, year: int) -> "Album":
        clause = (Album.name == name, Album.year == year)
        count = Album.select().where(*clause).count()

        if count == 0:
            result = Album.create(name=name, year=year, status=1)
        else:
            result = Album.get(*clause)
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

    @timeit
    @staticmethod
    def upsert(
        track: int, name: str, album: Album, artist: str, filepath: str
    ) -> "Song":
        clause = (Song.filepath == filepath,)
        count = Song.select().where(*clause).count()

        if count == 0:
            result = Song.create(
                track=track,
                name=name,
                album=album,
                artist=artist,
                filepath=filepath,
                status=1,
            )
        else:
            result = Song.get(*clause)
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
            album = Album.upsert(tag.album, tag.year)
            Song.upsert(tag.track, tag.title, album, tag.artist, song)


def main():
    db.connect()
    # db.drop_tables([Album, Song])  # ToDo: remove this line (here only for tests)
    db.create_tables([Album, Song])

    db.execute_sql("PRAGMA journal_mode = off;")
    db.execute_sql("PRAGMA synchronous = 0;")

    # Set all data satatus to 0
    Song.update(status=0).execute()
    Album.update(status=0).execute()

    for pragma in ["journal_mode", "synchronous"]:
        for r in db.execute_sql(f"PRAGMA {pragma};"):
            print(f"{pragma} - {r[0]}")

    # Insert/update data
    do_db_insert()

    # Delete data with status to 0
    Song.delete().where(Song.status == 0).execute()
    Album.delete().where(Album.status == 0).execute()

    Album.print_all()
    Song.print_all()


if __name__ == "__main__":
    main()
