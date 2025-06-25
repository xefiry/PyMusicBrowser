import enum
import threading
import time

import pygame
from peewee import fn

from .database import Song

EVENT_QUIT = 0
EVENT_SONG_END = 1


class State(enum.Enum):
    STOP = 0
    PLAY = 1
    PAUSE = 2


class Player:
    def __init__(self) -> None:
        pygame.mixer.init()
        self.song = Song.select().get()
        self.is_playing: bool = False

        pygame.init()
        self.thread = threading.Thread(target=self.event_handler)
        self.thread.start()

        self.state = State.STOP

        pygame.mixer.music.set_endevent(EVENT_SONG_END)

    def get_state(self) -> State:
        return self.state

    def play_pause(self) -> None:
        if self.state == State.STOP:
            self.state = State.PLAY
            pygame.mixer.music.load(self.song.file_path)
            pygame.mixer.music.play()

        elif self.state == State.PLAY:
            self.state = State.PAUSE
            pygame.mixer.music.pause()

        elif self.state == State.PAUSE:
            self.state = State.PLAY
            pygame.mixer.music.unpause()

    def next(self) -> None:
        self.song = Song.select().order_by(fn.Random()).get()
        pygame.mixer.music.load(self.song.file_path)
        pygame.mixer.music.play()

    def stop(self) -> None:
        self.state = State.STOP
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def quit(self) -> None:
        self.stop()
        pygame.event.post(pygame.event.Event(0))
        self.thread.join()

    def event_handler(self) -> None:
        is_running = True

        while is_running:
            # pygame.mixer.music.get_pos()  # ToDo: use this to update seek bar

            for event in pygame.event.get():
                if event.type == EVENT_QUIT:
                    is_running = False

                elif event.type == EVENT_SONG_END and self.state != State.STOP:
                    self.next()

            time.sleep(0.25)
