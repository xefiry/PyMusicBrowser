import os
import pathlib
import time
from datetime import timedelta

from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError
from mutagen.mp3 import MP3, HeaderNotFoundError
from peewee import ModelSelect, fn

from . import base_model as db
from . import utils
from .album import Album
from .artist import Artist
from .genre import Genre
from .setting import Setting
from .song import Song

DATABASE_MODELS = [Artist, Album, Genre, Song]

# FIXME Fix behaviour when there are no songs in the database


def init() -> None:
    db.init(DATABASE_MODELS + [Setting])


def scan(music_dirs: list[str]) -> None:
    # Set all data satatus to 0
    for model in DATABASE_MODELS:
        model.update(status=0).execute()

    # Insert/update data
    for music_dir in music_dirs:
        _scan_dir(music_dir)

    # Delete data with status to 0
    for model in DATABASE_MODELS:
        model.delete().where(model.status == 0).execute()

    db.vacuum()


def _scan_dir(path: str) -> None:
    print(f"Scanning {path}")

    start_time = time.time()
    nb_file = 0

    for root, _, files in os.walk(path):
        for file in files:
            if pathlib.Path(file).suffix == ".mp3":
                nb_file += 1
                file_path = os.path.normpath(os.path.join(root, file))
                _scan_file(file_path)

    total_time = round(time.time() - start_time, 2)
    print(f"Successfully scanned {nb_file} files in {total_time} s")


def _scan_file(file_path: str):
    file_stats = os.stat(file_path)
    file_mtime = int(file_stats.st_mtime)
    file_size = file_stats.st_size
    stored_mtime = Song.get_file_mtime(file_path)

    if file_mtime != stored_mtime:
        try:
            tag = EasyID3(file_path)
        except ID3NoHeaderError:
            tag = EasyID3()

        try:
            _duration = MP3(file_path).info.length
        except HeaderNotFoundError:
            _duration = 0

        _album = utils.get_str(tag, "album")
        _albumartist = utils.get_str(tag, "albumartist")
        _artist = utils.get_str(tag, "artist")
        _date = utils.get_year(tag, "date")
        _disk, _disk_total = utils.get_numbers(tag, "discnumber")
        _genre = utils.get_str(tag, "genre")
        _title = utils.get_str(tag, "title", "<unknown>")
        _track, _track_total = utils.get_numbers(tag, "tracknumber")

        albumartist = Artist.upsert(_albumartist)
        songartist = Artist.upsert(_artist)
        genre = Genre.upsert(_genre)
        album = Album.upsert(_album, albumartist, _date)

        Song.upsert(
            _track,
            _track_total,
            _title,
            genre,
            album,
            _disk,
            _disk_total,
            songartist,
            _date,
            _duration,
            file_path,
            file_mtime,
            file_size,
        )


def get_artists(has_album: bool = False, has_song: bool = False) -> ModelSelect:
    result = Artist.select().distinct()

    if has_album:
        result = result.join(Album)
    elif has_song:
        result = result.join(Song)

    return result.order_by(Artist.name)


def get_albums(artist: Artist | None = None) -> ModelSelect:
    result = Album.select()

    if artist is not None:
        result = result.where(Album.artist == artist)

    return result.order_by(Album.year, Album.name)


def get_songs(album: Album | None = None) -> ModelSelect:
    result = Song.select()

    if album is not None:
        result = result.where(Song.album == album)

    return result.order_by(Song.disk, Song.track, Song.name)


def get_genres() -> ModelSelect:
    return Genre.select().order_by(Genre.name)


def get_years() -> list[str]:
    years: list[int] = []
    result: list[str] = []

    for song in get_songs():
        years.append(song.year)

    # remove duplicates
    years = list(set(years))

    # convert to strings
    result = list(map(str, years))

    result.sort()

    return result


def print_stats() -> None:
    duration = Song.select(fn.SUM(Song.duration)).scalar()
    duration_days = timedelta(seconds=duration)
    size = Song.select(fn.SUM(Song.file_size)).scalar()
    size_gb = round(size / (1024**3), 2)

    print("Songs :", Song.select().count())
    print("Albums :", Album.select().count())
    print("Artists :", Artist.select().count())
    print("Genres :", Genre.select().count())
    print(f"duration : {duration} - {duration_days}")
    print(f"size : {size} - {size_gb} GB")
