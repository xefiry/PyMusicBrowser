from . import database, gui

# TODO Add logging


def main() -> None:
    database.init()
    gui.start()
