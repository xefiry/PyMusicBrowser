from . import database, gui

# TODO Add logging

if __name__ == "__main__":
    database.init()
    gui.start()
