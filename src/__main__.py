from . import database
from .gui import GUI

if __name__ == "__main__":
    database.init()

    gui = GUI()
    gui.mainloop()
