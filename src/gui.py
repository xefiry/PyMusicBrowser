import tkinter as tk
from tkinter import ttk
from .player import Player, State


class GUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("PyMusicPlayer")
        self.geometry("200x150")

        self.b_play_pause = ttk.Button(self, text="Play", command=self.do_play_pause)
        self.b_play_pause.pack(pady=5)

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
