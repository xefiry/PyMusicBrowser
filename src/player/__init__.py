import enum
import threading

import pygame

from ..database.song import Song
from ..database.album import Album
from .playlist import Playlist


class Event(enum.IntEnum):
    SONG_END = 1


class State(enum.Enum):
    STOP = 0
    PLAY = 1
    PAUSE = 2


# TODO Handle missing files


class Player:
    def __init__(self) -> None:
        pygame.mixer.init()
        self.playlist = Playlist()
        self.is_playing: bool = False

        pygame.init()
        self.tread_run: bool = True
        self.thread = threading.Thread(target=self.event_handler)
        self.thread.start()

        self.state = State.STOP
        self.cur_pos: int = 0
        self.volume: int = 100

        pygame.mixer.music.set_endevent(Event.SONG_END)

    def load_music(self) -> None:
        """Load a music file and play it"""

        song = self.playlist.get_current()

        if song is not None:
            pygame.mixer.music.load(str(song.file_path))
            self.cur_pos = 0
            if self.state != State.STOP:
                pygame.mixer.music.play()

    def play_pause(self) -> None:
        if self.state == State.STOP:
            self.state = State.PLAY
            self.load_music()

        elif self.state == State.PLAY:
            self.state = State.PAUSE
            pygame.mixer.music.pause()

        elif self.state == State.PAUSE:
            self.state = State.PLAY
            pygame.mixer.music.unpause()

    def previous(self) -> None:
        self.state = State.PLAY

        pygame.mixer.music.unload()

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

    def add_song(self, song_id: int) -> None:
        # TODO don't query data directly, use function from database
        song = Song.select().where(Song.id == song_id).get()  # type: ignore
        self.playlist.add_next(song)

    def add_album(self, album_id: int) -> None:
        # TODO don't query data directly, use function from database
        songs = (
            Song.select()
            .join(Album)
            .where(Album.id == album_id)  # type: ignore
            # order by desc because songs will be added next to the current one
            .order_by(Song.track.desc(), Song.name.desc())
        )

        for song in songs:
            self.playlist.add_next(song)

    def remove_song(self, song_nb: int) -> None:
        if self.playlist.remove(song_nb):
            self.load_music()

    def stop(self) -> None:
        if self.state != State.STOP:
            self.state = State.STOP
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

    def seek(self, time: int) -> None:
        if self.playlist.get_current() is None or self.state == State.STOP:
            return

        v = self.get_volume()

        # reload song (rewind does not work properly)
        pygame.mixer.music.unload()

        # to avoid a sound crack caused by fast play/pause, set volume to 0
        if self.state == State.PAUSE:
            self.set_volume(0)

        self.load_music()
        pygame.mixer.music.set_pos(time)

        # if the state was pause, put it back (with the volume)
        if self.state == State.PAUSE:
            pygame.mixer.music.pause()
            self.set_volume(v)

        self.cur_pos = time

    def quit(self) -> None:
        self.playlist.save()
        self.stop()
        self.tread_run = False
        self.thread.join()
        pygame.mixer.quit()
        pygame.quit()

    def get_current_time(self) -> tuple[int, int]:
        """Get song current/total time of the current playing song.
        If no song is playng, return 0/0"""

        song = self.playlist.get_current()

        if song is None or self.state == State.STOP:
            return (0, 0)

        # get current play position in seconds, 0 if negative
        cur_time = max(pygame.mixer.music.get_pos() // 1000, 0) + self.cur_pos

        # get current song time in seconds
        total_time = int(song.duration)  # type: ignore

        return (cur_time, total_time)

    def get_volume(self) -> int:
        return self.volume

    def set_volume(self, volume: int) -> None:
        self.volume = volume
        pygame.mixer.music.set_volume(volume / 100)

    def get_song_list(self) -> tuple[list[Song], int]:
        """Get the current song list.
        It returns the list of songs and the index of the current playing one"""

        return (
            self.playlist.song_list,
            self.playlist.current_song,
        )

    def event_handler(self) -> None:
        """Function to manage pygame events.
        It does next when the current song ends."""

        while self.tread_run:
            for event in pygame.event.get():
                # if song ends and it was not because we used stop button
                if event.type == Event.SONG_END and self.state != State.STOP:
                    self.next()

            pygame.time.wait(100)
