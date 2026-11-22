import enum

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

from .. import database
from ..database.album import Album
from ..database.song import Song
from .playlist import Playlist


class State(enum.StrEnum):
    STOP = "Stopped"
    PLAY = "Playing"
    PAUSE = "Paused"


# TODO Handle missing files


class Player:
    def __init__(self) -> None:
        self.playlist = Playlist()
        self.is_playing: bool = False

        self.state = State.STOP
        self.cur_pos: int = 0
        self.volume: int = 100

        # TODO: suppress qt.multimedia.ffmpeg logs (with ["QT_LOGGING_RULES"] = "qt.multimedia.ffmpeg*=false" ?)
        self.audio_output = QAudioOutput()
        self.audio_engine = QMediaPlayer()
        self.audio_engine.setAudioOutput(self.audio_output)

        # TODO: WIP
        # self.audio_engine.positionChanged.connect(lambda x: print(f"positionChanged {x}"))
        # self.audio_engine.durationChanged.connect(lambda x: print(f"durationChanged {x}"))
        # self.audio_engine.sourceChanged.connect(lambda x: print(f"sourceChanged {x}"))
        self.audio_engine.mediaStatusChanged.connect(self.on_status_changed)

    def load_music(self) -> None:
        """Load a music file and play it"""

        song = self.playlist.get_current()

        if song is not None:
            self.audio_engine.setSource(QUrl.fromLocalFile(song.file_path))
            self.cur_pos = 0
            if self.state != State.STOP:
                self.audio_engine.play()

    def play_pause(self) -> None:
        if self.state == State.STOP:
            self.state = State.PLAY
            self.load_music()

        elif self.state == State.PLAY:
            self.state = State.PAUSE
            self.audio_engine.pause()

        elif self.state == State.PAUSE:
            self.state = State.PLAY
            self.audio_engine.play()

    def previous(self) -> None:
        self.state = State.PLAY

        if self.playlist.previous():
            self.load_music()
        else:
            self.stop()

    def next(self) -> None:
        self.state = State.PLAY
        self.playlist.next()
        self.load_music()

    def select_song(self, song_nb: int) -> None:
        self.state = State.PLAY
        self.playlist.select(song_nb)
        self.load_music()

    def add_song(self, song: Song) -> None:
        self.playlist.add_next(song)

    def add_album(self, album: Album) -> None:
        for song in database.get_songs(album, reverse=True):
            self.playlist.add_next(song)

    def remove_song(self, song_nb: int) -> None:
        if self.playlist.remove(song_nb):
            self.load_music()

    def stop(self) -> None:
        if self.state != State.STOP:
            self.state = State.STOP
            self.audio_engine.stop()

    def seek(self, time: int) -> None:
        if self.playlist.get_current() is None or self.state == State.STOP:
            return

        self.audio_engine.setPosition(time * 1000)
        self.cur_pos = time

    def quit(self) -> None:
        self.playlist.save()
        self.stop()

    def get_current_time(self) -> tuple[int, int]:
        """Get song current/total time of the current playing song.
        If no song is playng, return 0/0"""

        song = self.playlist.get_current()

        if song is None or self.state == State.STOP:
            return (0, 0)

        # get current play position in seconds, 0 if negative
        cur_time = max(self.audio_engine.position() // 1000, 0)

        # get current song time in seconds
        total_time = int(song.duration)

        return (cur_time, total_time)

    def get_volume(self) -> int:
        return self.volume

    def set_volume(self, volume: int) -> None:
        self.volume = volume
        self.audio_output.setVolume(volume / 100)

    def get_song_list(self) -> tuple[list[Song], int]:
        """Get the current song list.
        It returns the list of songs and the index of the current playing one"""

        return (
            self.playlist.song_list,
            self.playlist.current_song,
        )

    def on_status_changed(self, status: QMediaPlayer.MediaStatus) -> None:
        match status:
            case QMediaPlayer.MediaStatus.EndOfMedia:
                self.next()
