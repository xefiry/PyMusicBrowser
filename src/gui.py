import math
import tkinter as tk
from tkinter import filedialog as dlg
from tkinter import messagebox as msg
from tkinter import ttk

from PIL import Image, ImageTk

from . import database, utils
from .database.setting import Setting
from .player import Player, State

UPDATE_DELAY = 100  # 0.1 s
COVER_SIZE = (300, 300)
VOLUME_STEP = 5

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

        # UI Configuration

        self.title("PyMusicBrowser")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.do_quit)

        _style = ttk.Style()
        _style.theme_use("xpnative")

        # UI Main

        main_left = ttk.Frame(self)
        main_right = ttk.Frame(self)

        main_left.grid(column=0, row=0)
        main_right.grid(column=2, row=0)

        # UI Left

        self.cover = tk.Canvas(main_left, width=COVER_SIZE[0], height=COVER_SIZE[1])
        self.cover.pack()

        self.song_title = ttk.Label(main_left, text="<title>")
        self.song_title.pack()

        self.song_album = ttk.Label(main_left, text="<album>")
        self.song_album.pack()

        self.song_artist = ttk.Label(main_left, text="<artist>")
        self.song_artist.pack()

        self.time_frame = tk.Frame(main_left)
        self.time_frame.pack(pady=5)

        self.time_cur = ttk.Label(self.time_frame, text="0:00")
        self.time_cur.grid(row=0, column=0, padx=5)

        self.time_var = tk.DoubleVar()
        self.time_scale = ttk.Scale(
            self.time_frame,
            from_=0,
            variable=self.time_var,
            length=200,
        )
        self.time_scale.grid(row=0, column=1)
        self.time_scale_pressed = False
        self.time_scale.bind("<ButtonPress-1>", self.do_press_timescale)
        self.time_scale.bind("<ButtonRelease-1>", self.do_release_timescale)

        self.time_tot = ttk.Label(self.time_frame, text="0:00")
        self.time_tot.grid(row=0, column=2, padx=5)

        self.button_frame = tk.Frame(main_left)
        self.button_frame.pack(pady=5)

        self.b_play_pause = ttk.Button(
            self.button_frame,
            text=BUTTON_TEXT["play"],
            command=self.do_play_pause,
            width=5,
        )
        self.b_play_pause.grid(row=0, column=0)

        ttk.Button(
            self.button_frame,
            text=BUTTON_TEXT["prev"],
            command=self.do_previous,
            width=5,
        ).grid(row=0, column=1)

        ttk.Button(
            self.button_frame, text=BUTTON_TEXT["next"], command=self.do_next, width=5
        ).grid(row=0, column=2)

        ttk.Button(
            self.button_frame, text=BUTTON_TEXT["stop"], command=self.do_stop, width=5
        ).grid(row=0, column=3)

        self.volume_var = tk.DoubleVar()
        self.volume_scale = ttk.Scale(
            self.button_frame,
            from_=0,
            to=100,
            variable=self.volume_var,
            command=self.do_change_volume,
            length=80,
        )
        self.volume_scale.grid(row=0, column=4, padx=5)

        self.volume_scale.bind("<MouseWheel>", self.do_scroll_volume)

        self.volume_lvl = ttk.Label(self.button_frame, text="xx%", width=5)
        self.volume_lvl.grid(row=0, column=5)

        # UI Right

        self.songs_scroll = ttk.Scrollbar(main_right)
        self.songs_scroll.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.songs_var = tk.Variable()
        self.songs_list = tk.Listbox(
            main_right, listvariable=self.songs_var, width=50, height=26
        )
        self.songs_list.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.songs_list.config(yscrollcommand=self.songs_scroll.set)
        self.songs_list.bind("<Return>", self.do_activate_list)
        self.songs_list.bind("<Double-Button-1>", self.do_activate_list)
        self.songs_list.bind("<Delete>", self.do_delete_list)

        # UI variables & misc

        self._cur_song_path = ""

        # ToDo: put in function ?
        music_dir = Setting.get_value("music_dir")
        if music_dir == "":
            music_dir = dlg.askdirectory(title="Select a directory to scan for songs")
            if music_dir == "":
                msg.showerror("No music directory", "No directory to scan for music")
                exit(0)

            Setting.upsert("music_dir", music_dir)

            # ToDo: add possibility to cancel
            msg.showinfo(
                "Music scanning",
                f"'{music_dir}' will be scanned for music.\n"
                "The window may appear stuck, please let it scan to the end.",
            )

            database.scan(music_dir)

        self.player = Player()

        # Try to get volume from settings
        _volume = Setting.get_value("volume")
        # if it does not exist, set it to 100
        if _volume == "":
            _volume = "100"
        self.do_change_volume(_volume)

        self.update_ui()

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

    def do_press_timescale(self, event: tk.Event) -> None:
        if self.time_scale["state"] == "enabled":
            self.time_scale_pressed = True

    def do_release_timescale(self, event: tk.Event) -> None:
        if self.time_scale["state"] == "enabled":
            self.time_scale_pressed = False
            self.player.seek(math.ceil(self.time_var.get()))

    def do_change_volume(self, volume: str) -> None:
        vol = math.ceil(float(volume))

        self.volume_var.set(vol)
        self.player.set_volume(vol)
        self.volume_lvl.config(text=f"{vol:3}%")

        Setting.upsert("volume", str(vol))

    def do_scroll_volume(self, event: tk.Event) -> None:
        vol = self.player.get_volume()

        if event.delta > 0:
            while (vol := vol + 1) % VOLUME_STEP != 0:
                pass
        else:
            while (vol := vol - 1) % VOLUME_STEP != 0:
                pass

        # the volume must be between 0 and 100
        vol = min(vol, 100)
        vol = max(vol, 0)

        self.do_change_volume(str(vol))

    def do_activate_list(self, event: tk.Event) -> None:
        widget = event.widget
        selection = widget.curselection()[0]  # type: ignore

        self.player.select_song(selection)
        self.update_ui()

    def do_delete_list(self, event: tk.Event) -> None:
        widget = event.widget
        selection = widget.curselection()[0]  # type: ignore

        self.player.remove_song(selection)
        self.update_ui()

    def update_ui(self) -> None:
        self.update_time_scale()
        self.update_buttons()
        self.update_song_infos()
        self.update_song_list()

        if self.player.state != State.STOP:
            self.after(UPDATE_DELAY, self.update_ui)

    def update_time_scale(self) -> None:
        """Get song current/total time from the player and use it to update the timescale of the UI"""

        # if the player is stopped, disable time scale and set it to 0/0
        if self.player.state == State.STOP:
            self.time_scale["state"] = "disabled"
            t1, t2 = 0, 0
            # to put the cursor on the left
            self.time_var.set(0)
            self.time_scale["to"] = 1
        else:
            self.time_scale["state"] = "enabled"
            t1, t2 = self.player.get_current_time()

            # if the time scale is pressed, we will display the time of the scale
            # instead of the current time of the song
            if self.time_scale_pressed:
                t1 = self.time_var.get()

            self.time_var.set(t1)
            self.time_scale["to"] = t2

        self.time_cur.config(text=utils.s_to_t(t1))
        self.time_tot.config(text=utils.s_to_t(t2))

    def update_buttons(self) -> None:
        """Update text of buttons using player state"""

        state = self.player.state

        if state == State.STOP or state == State.PAUSE:
            self.b_play_pause.config(text=BUTTON_TEXT["play"])
        elif state == State.PLAY:
            self.b_play_pause.config(text=BUTTON_TEXT["pause"])

    def update_song_infos(self) -> None:
        song = self.player.playlist.get_current()

        # If the song file has not changed since last update, do nothing
        if song.file_path == self._cur_song_path:
            return

        pic = utils.get_cover(str(song.file_path))

        if pic is None:
            self.cover_img = Image.new(mode="RGB", size=COVER_SIZE, color="#999090")
        else:
            self.cover_img = Image.open(pic)
            self.cover_img = self.cover_img.resize(COVER_SIZE)

        self.cover_img = ImageTk.PhotoImage(self.cover_img)

        self.cover.create_image(0, 0, anchor="nw", image=self.cover_img)

        self.song_title.config(text=f"{song.track} - {song.name}")
        self.song_album.config(text=str(song.album.name))
        self.song_artist.config(text=str(song.artist.name))

        # update current song
        self._cur_song_path = song.file_path

    def update_song_list(self) -> None:
        songs, cur = self.player.get_song_list()

        songs[cur] = BUTTON_TEXT["play"] + songs[cur]

        self.songs_var.set(songs)

        self.songs_list.see(cur)
