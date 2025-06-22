import os
import pathlib
import time

from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError
from mutagen.mp3 import MP3, HeaderNotFoundError

from .. import utils
from .album import Album
from .artist import Artist
from .base_model import init_db
from .genre import Genre
from .song import Song

DIR_LIST = ["D:/Music/"]
DATABASE_MODELS = [Artist, Album, Genre, Song]


def init() -> None:
    init_db(DATABASE_MODELS)


def scan() -> None:
    # Set all data satatus to 0
    for model in DATABASE_MODELS:
        model.update(status=0).execute()

    # Insert/update data
    for dir in DIR_LIST:
        _scan_dir(dir)

    # Delete data with status to 0
    for model in DATABASE_MODELS:
        model.delete().where(model.status == 0).execute()


def _scan_dir(path: str) -> None:
    print(f"Scanning {path}")

    start_time = time.time()
    nb_file = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            if pathlib.Path(file).suffix == ".mp3":
                nb_file += 1
                song_file = os.path.normpath(os.path.join(root, file))
                file_stats = os.stat(song_file)
                file_mtime = int(file_stats.st_mtime)
                file_size = file_stats.st_size
                stored_mtime = Song.get_file_mtime(song_file)

                if file_mtime != stored_mtime:
                    try:
                        tag = EasyID3(song_file)
                    except ID3NoHeaderError:
                        tag = EasyID3()

                    try:
                        _duration = MP3(song_file).info.length
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
                        song_file,
                        file_mtime,
                        file_size,
                    )

    total_time = round(time.time() - start_time, 2)
    print(f"Successfully scanned {nb_file} files in {total_time} s")
