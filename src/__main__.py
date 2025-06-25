from . import database
from .gui import GUI

if __name__ == "__main__":
    database.init()
    # database.scan()

    gui = GUI()
    gui.mainloop()
