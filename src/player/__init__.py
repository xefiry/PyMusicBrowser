import enum
import threading

import pygame

from .playlist import Playlist


class Event(enum.IntEnum):
    SONG_END = 1


class State(enum.Enum):
    STOP = 0
    PLAY = 1
    PAUSE = 2


class Player:
    def __init__(self) -> None:
        pygame.mixer.init()
        self.playlist = Playlist()
        self.song = self.playlist.get_current()
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

        if self.song is not None:
            pygame.mixer.music.load(str(self.song.file_path))
            self.cur_pos = 0
            pygame.mixer.music.play()

    def play_pause(self) -> None:
        if self.state == State.STOP:
            self.state = State.PLAY
            self.song = self.playlist.get_current()
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
        self.song = self.playlist.previous()

        if self.song is None:
            self.stop()
        else:
            self.load_music()

    def next(self) -> None:
        self.state = State.PLAY

        self.song = self.playlist.next()
        self.load_music()

    def stop(self) -> None:
        if self.state != State.STOP:
            self.state = State.STOP
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

    def seek(self, time: int) -> None:
        if self.song is None:
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
        self.stop()
        self.tread_run = False
        self.thread.join()
        pygame.mixer.quit()
        pygame.quit()

    def get_current_time(self) -> tuple[float, float]:
        """Get song current/total time of the current playing song.
        If no song is playng, return 0/0"""

        if self.song is None:
            return (0, 0)

        # get current play position in seconds, 0 if negative
        cur_time = max(pygame.mixer.music.get_pos() / 1000, 0) + self.cur_pos

        # get current song time in seconds
        total_time = float(self.song.duration)  # type: ignore

        return (cur_time, total_time)

    def get_volume(self) -> int:
        return self.volume

    def set_volume(self, volume: int) -> None:
        self.volume = volume
        pygame.mixer.music.set_volume(volume / 100)

    def event_handler(self) -> None:
        """Function to manage pygame events.
        It does next when the current song ends."""

        while self.tread_run:
            for event in pygame.event.get():
                # if song ends and it was not because we used stop button
                if event.type == Event.SONG_END and self.state != State.STOP:
                    self.next()

            pygame.time.wait(100)
