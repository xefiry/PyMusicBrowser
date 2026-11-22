from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QWidget,
)

from .utils import get_child, load_widget_from_file


class DirectoryPicker:
    def __init__(self, parent: QWidget, dir_list: list[str]) -> None:
        # Load UI
        self.dialog = load_widget_from_file(
            "src/pymusicbrowser/gui/directory_picker.ui", QDialog, parent
        )
        self.dir_list = get_child(self.dialog, QListWidget, "dir_list")
        self.add_button = get_child(self.dialog, QPushButton, "add_button")
        self.modify_button = get_child(self.dialog, QPushButton, "modify_button")
        self.remove_button = get_child(self.dialog, QPushButton, "remove_button")
        self.buttonBox = get_child(self.dialog, QDialogButtonBox, "buttonBox")

        # Connect UI
        self.dir_list.itemClicked.connect(self.do_enable_buttons)
        self.add_button.clicked.connect(self.do_add_dir)
        self.modify_button.clicked.connect(self.do_modify_dir)
        self.remove_button.clicked.connect(self.do_remove_dir)
        self.buttonBox.accepted.connect(self.dialog.accept)
        self.buttonBox.rejected.connect(self.dialog.reject)

        # Function calls
        self.set_dir_list(dir_list)

    def exec(self) -> int:
        return self.dialog.exec()

    def do_add_dir(self) -> None:
        dialog = QFileDialog()

        if directory := dialog.getExistingDirectory():
            item = QListWidgetItem(self.dir_list)
            item.setText(directory)

    def do_modify_dir(self) -> None:
        dialog = QFileDialog()
        index = self.dir_list.currentRow()
        selected = self.dir_list.item(index)

        if directory := dialog.getExistingDirectory(dir=selected.text()):
            selected.setText(directory)

    def do_remove_dir(self) -> None:
        index = self.dir_list.currentRow()
        self.dir_list.takeItem(index)

    def do_enable_buttons(self) -> None:
        self.modify_button.setEnabled(True)
        self.remove_button.setEnabled(True)

    def set_dir_list(self, dir_list: list[str]) -> None:
        for dir in dir_list:
            item = QListWidgetItem(self.dir_list)
            item.setText(dir)

    def get_dir_list(self) -> list[str]:
        dir_list = []

        for i in range(self.dir_list.count()):
            dir_list.append(self.dir_list.item(i).text())

        return dir_list
