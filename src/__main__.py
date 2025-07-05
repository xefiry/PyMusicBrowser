import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

if __name__ == "__main__":
    from . import database
    from .gui import GUI

    database.init()

    gui = GUI()
    gui.mainloop()
