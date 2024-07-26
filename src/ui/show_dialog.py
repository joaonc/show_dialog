from PySide6.QtWidgets import QMainWindow

from src.ui.forms.ui_show_dialog import Ui_ShowDialog


class ShowDialog(QMainWindow, Ui_ShowDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
