import tkinter as tk
from tkinter import ttk
from .player import Player, State


UPDATE_DELAY = 100  # 0.1 s

# More at https://en.wikipedia.org/wiki/Media_control_symbols#Symbols
BUTTON_TEXT = {
    "play": "⏵",
    "pause": "⏸",
    "prev": "⏮",
    "next": "⏭",
    "stop": "⏹",
}


class GUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.player = Player()

        self.title("PyMusicBrowser")
        self.geometry("200x230")

        self.b_play_pause = ttk.Button(
            self, text=BUTTON_TEXT["play"], command=self.do_play_pause
        )
        self.b_play_pause.pack(pady=5)

        self.b_previous = ttk.Button(
            self, text=BUTTON_TEXT["prev"], command=self.do_previous
        )
        self.b_previous.pack(pady=5)

        self.b_next = ttk.Button(self, text=BUTTON_TEXT["next"], command=self.do_next)
        self.b_next.pack(pady=5)

        self.b_stop = ttk.Button(self, text=BUTTON_TEXT["stop"], command=self.do_stop)
        self.b_stop.pack(pady=5)

        self.time_var = tk.DoubleVar()
        self.time_scale = ttk.Scale(self, from_=0, variable=self.time_var)
        self.time_scale.pack()
        # self.time_scale.bind("<ButtonPress-1>",lambda evt: print("scale Press")
        # self.time_scale.bind("<ButtonRelease-1>",lambda evt: print("scale Release")

        self.volume_var = tk.DoubleVar()
        self.volume_var.set(self.player.get_volume())
        self.volume_scale = ttk.Scale(
            self, from_=0, to=100, variable=self.volume_var, command=self.change_volume
        )
        self.volume_scale.pack()

        self.b_play_pause.focus()
        self.protocol("WM_DELETE_WINDOW", self.do_quit)

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

    def change_volume(self, volume: str) -> None:
        self.player.set_volume(float(volume))

    def update_time_scale(self) -> None:
        """Get song current/total time from the player and use it to update the timescale of the UI"""

        t1, t2 = self.player.get_current_time()

        self.time_var.set(t1)
        self.time_scale["to"] = t2

        # If we are playing, recall this function after a delay
        if self.player.state == State.PLAY:
            self.after(UPDATE_DELAY, self.update_time_scale)

    def update_ui(self) -> None:
        """Update UI text of buttons using player state"""

        state = self.player.state

        if state == State.STOP or state == State.PAUSE:
            self.b_play_pause.config(text=BUTTON_TEXT["play"])
        elif state == State.PLAY:
            self.b_play_pause.config(text=BUTTON_TEXT["pause"])
            self.update_time_scale()
