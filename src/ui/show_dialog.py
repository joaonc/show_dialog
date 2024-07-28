from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow

from src.inputs import Inputs
from src.ui.forms.ui_show_dialog import Ui_ShowDialog


class ShowDialog(QMainWindow, Ui_ShowDialog):
    def __init__(self, inputs: Inputs):
        super().__init__()
        self.setupUi(self)
        self.inputs = inputs

        # UI adjustments
        self.pass_button.setIconSize(self.pass_button.size())
        self.fail_button.setIconSize(self.fail_button.size())
        self.title_label.setText(self.inputs.title)
        self.description_label.setText(self.inputs.description)
        if self.inputs.dialog_title:
            self.setWindowTitle(self.inputs.dialog_title)
        if self.inputs.title_color:
            self.title_label.setStyleSheet(f'color: {self.inputs.title_color};')
        if self.inputs.description_color:
            self.description_label.setStyleSheet(f'color: {self.inputs.description_color};')

        # UI bindings
        self.pass_button.clicked.connect(self.pass_clicked)
        self.fail_button.clicked.connect(self.fail_clicked)
        self.exit_shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.exit_shortcut.activated.connect(self.fail_clicked)

    # noinspection PyMethodMayBeStatic
    def pass_clicked(self):
        # Equivalent to `self.close()`.
        # Using `QApplication.exit(0)` to enable testing exit code.
        QApplication.exit(0)

    # noinspection PyMethodMayBeStatic
    def fail_clicked(self):
        QApplication.exit(1)
