from PySide6.QtWidgets import QMainWindow, QApplication

from src.ui.forms.ui_show_dialog import Ui_ShowDialog


class ShowDialog(QMainWindow, Ui_ShowDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # UI adjustments
        self.pass_button.setIconSize(self.pass_button.size())
        self.fail_button.setIconSize(self.fail_button.size())

        # UI bindings
        self.pass_button.clicked.connect(self.pass_clicked)
        self.fail_button.clicked.connect(self.fail_clicked)

    def pass_clicked(self):
        self.close()

    # noinspection PyMethodMayBeStatic
    def fail_clicked(self):
        QApplication.exit(1)
