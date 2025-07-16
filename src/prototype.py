import os
import sys
from PySide6 import QtWidgets, QtGui, QtCore

root_path = "D:/Music/Zombie Nation"
dirs = [
    "1999 - Leichenschmaus",
    "2003 - Absorber",
    "2006 - Black toys",
    "2009 - Zombielicious",
    "2012 - RGB",
    "2025 - don't exist",
]


app = QtWidgets.QApplication(sys.argv)

mw = QtWidgets.QMainWindow()

list = QtWidgets.QListWidget()
list.setViewMode(QtWidgets.QListWidget.ViewMode.IconMode)
list.setIconSize(QtCore.QSize(150, 150))
list.setResizeMode(QtWidgets.QListWidget.ResizeMode.Adjust)
mw.setCentralWidget(list)

item_size = QtCore.QSize(150, 150)

for dir in dirs:
    file_path = os.path.join(root_path, dir, "cover.jpg")
    icon = QtGui.QIcon(file_path)

    item = QtWidgets.QListWidgetItem(list)
    item.setSizeHint(QtCore.QSize(160, 200))
    item.setText("Zombie Nation\n" + dir)
    item.setIcon(icon)


mw.show()

rv = app.exec()

sys.exit(rv)
