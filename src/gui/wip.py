import sys

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6 import QtWidgets
from PySide6 import QtGui


def start() -> None:
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    rv = app.exec()

    sys.exit(rv)


class MyQtWidgetsV2(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.build_ui()
        self.connect_all()

    def build_ui(self) -> None:
        self.button = QtWidgets.QPushButton("Click me again")
        self.text = QtWidgets.QLabel("Some random label")

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.button)
        self.main_layout.addWidget(self.text)

    def connect_all(self) -> None:
        self.button.clicked.connect(self.clickme)

    @QtCore.Slot()
    def clickme(self):
        print("Click!")
        self.text.setText("You did it!")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.build()

    def build(self) -> None:
        self.setWindowTitle("My beautifull MainWindow")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QtGui.QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()

        # Dock widgets
        self.left_dock = QtWidgets.QDockWidget(self, floating=False)
        self.left_dock.setMinimumWidth(300)
        self.left_dock.setWindowTitle("The Left Dock")
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)

        self.left_widget = MyQtWidgetsV2()
        self.left_dock.setWidget(self.left_widget)

        # Central widget
        self.central = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central)

        self.button = QtWidgets.QPushButton("Click me now !!!")
        self.text = QtWidgets.QLabel("Some random label")

        self.main_layout = QtWidgets.QVBoxLayout(self.central)
        self.main_layout.addWidget(self.button)
        self.main_layout.addWidget(self.text)

        self.button.clicked.connect(self.clickme)

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setFixedSize(int(geometry.width() * 0.8), int(geometry.height() * 0.8))

    @QtCore.Slot()
    def clickme(self):
        print("Clack!")
        self.status.showMessage("Thank you.")

    @QtCore.Slot()
    def choose_directory(self):
        dialog = QFileDialog()
        result = dialog.getExistingDirectory()
        print(result)
