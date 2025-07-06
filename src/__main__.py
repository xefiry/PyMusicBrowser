from . import database

# from gui.old import GUI
from . import gui

if __name__ == "__main__":
    database.init()

    gui.start()
    # gui = GUI()
    # gui.mainloop()
