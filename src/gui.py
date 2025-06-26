import tkinter as tk
from tkinter import ttk
from .player import Player, State


class GUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("PyMusicPlayer")
        self.geometry("200x180")

        self.b_play_pause = ttk.Button(self, text="Play", command=self.do_play_pause)
        self.b_play_pause.pack(pady=5)

        self.b_previous = ttk.Button(self, text="Previous", command=self.do_previous)
        self.b_previous.pack(pady=5)

        self.b_next = ttk.Button(self, text="Next", command=self.do_next)
        self.b_next.pack(pady=5)

        self.b_stop = ttk.Button(self, text="Stop", command=self.do_stop)
        self.b_stop.pack(pady=5)

        self.b_quit = ttk.Button(self, text="Quit", command=self.do_quit)
        self.b_quit.pack(pady=5)

        self.b_play_pause.focus()
        self.protocol("WM_DELETE_WINDOW", self.do_quit)

        self.player = Player()

    def do_play_pause(self) -> None:
        self.player.play_pause()
        self.update_ui()

    def do_previous(self) -> None:
        self.player.previous()
        self.update_ui()

    def do_next(self) -> None:
        self.player.next()
        self.update_ui()

    def do_stop(self) -> None:
        self.player.stop()
        self.update_ui()

    def do_quit(self) -> None:
        self.player.quit()
        self.quit()

    def update_ui(self) -> None:
        state = self.player.get_state()

        if state == State.STOP or state == State.PAUSE:
            self.b_play_pause.config(text="Play")
        elif state == State.PLAY:
            self.b_play_pause.config(text="Pause")

        self.player.playlist.print()
