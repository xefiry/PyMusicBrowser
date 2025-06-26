import tkinter as tk
from tkinter import ttk
from .player import Player, State


class GUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("PyMusicPlayer")
        self.geometry("200x220")

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

        self.time_var = tk.DoubleVar()
        self.time_scale = ttk.Scale(self, from_=0, variable=self.time_var)
        self.time_scale.pack()
        # self.time_scale.bind("<ButtonPress-1>",lambda evt: print("scale Press")
        # self.time_scale.bind("<ButtonRelease-1>",lambda evt: print("scale Release")

        self.b_play_pause.focus()
        self.protocol("WM_DELETE_WINDOW", self.do_quit)

        self.player = Player(self.update_time_scale)

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

    def update_time_scale(self, cur_time: float, max_time: float) -> None:
        self.time_var.set(cur_time)
        self.time_scale["to"] = max_time

    def update_ui(self) -> None:
        state = self.player.state

        if state == State.STOP or state == State.PAUSE:
            self.b_play_pause.config(text="Play")
        elif state == State.PLAY:
            self.b_play_pause.config(text="Pause")

        self.player.playlist.print()
