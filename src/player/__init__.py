import enum
import threading
import time

import pygame

from .playlist import Playlist

from collections.abc import Callable


class Event(enum.IntEnum):
    QUIT = 0
    SONG_END = 1


class State(enum.Enum):
    STOP = 0
    PLAY = 1
    PAUSE = 2


class Player:
    def __init__(self, time_callback: Callable) -> None:
        # function used to send back to UI time changes for the current song
        self.time_callback: Callable | None = time_callback

        pygame.mixer.init()
        self.playlist = Playlist()
        self.song = self.playlist.get_current()
        self.is_playing: bool = False

        pygame.init()
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
        # set callback to None to avoid calling it when it has been "removed"
        self.time_callback = None
        self.stop()
        pygame.event.post(pygame.event.Event(Event.QUIT))
        self.thread.join()
        pygame.mixer.quit()
        pygame.quit()

    def event_handler(self) -> None:
        is_running = True

        while is_running:
            if self.time_callback is not None:
                # get current play position in seconds, 0 if negative
                cur_time = max(pygame.mixer.music.get_pos() / 1000, 0)

                # get current song time in seconds, 0 no current song
                if self.song is None:
                    total_time = 0
                else:
                    total_time = self.song.duration

                self.time_callback(cur_time, total_time)

            for event in pygame.event.get():
                if event.type == Event.QUIT:
                    is_running = False

                elif event.type == Event.SONG_END and self.state != State.STOP:
                    self.next()

            time.sleep(0.1)
