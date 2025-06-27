import enum
import threading
import time

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

        pygame.mixer.music.set_endevent(Event.SONG_END)

    def play_pause(self) -> None:
        if self.state == State.STOP:
            self.state = State.PLAY
            self.song = self.playlist.get_current()
            pygame.mixer.music.load(str(self.song.file_path))
            pygame.mixer.music.play()

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
            pygame.mixer.music.load(str(self.song.file_path))
            pygame.mixer.music.play()

    def next(self) -> None:
        self.state = State.PLAY

        pygame.mixer.music.unload()
        self.song = self.playlist.next()
        pygame.mixer.music.load(str(self.song.file_path))
        pygame.mixer.music.play()

    def stop(self) -> None:
        if self.state != State.STOP:
            self.state = State.STOP
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

    def quit(self) -> None:
        self.stop()
        self.tread_run = False
        self.thread.join()
        pygame.mixer.quit()
        pygame.quit()

    def get_current_time(self) -> tuple[float, float]:
        if self.song is None:
            return (0, 0)

        # get current play position in seconds, 0 if negative
        cur_time = max(pygame.mixer.music.get_pos() / 1000, 0)

        # get current song time in seconds
        total_time = float(self.song.duration)  # type: ignore

        return (cur_time, total_time)

    def event_handler(self) -> None:
        while self.tread_run:
            for event in pygame.event.get():
                if event.type == Event.SONG_END and self.state != State.STOP:
                    self.next()

            time.sleep(0.1)
