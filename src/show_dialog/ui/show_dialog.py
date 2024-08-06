import logging

import markdown
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QDialog

from ..inputs import Inputs
from .forms.ui_show_dialog import Ui_ShowDialog


class ShowDialog(QDialog, Ui_ShowDialog):
    def __init__(
        self,
        app: QApplication,
        inputs: Inputs,
        stylesheet: str | None = None,
    ):
        super().__init__()
        self.app = app
        self.stylesheet = stylesheet
        self.setupUi(self)
        self.inputs = inputs

        # UI adjustments
        self.title_label.setText(self.inputs.title)
        if self.inputs.description_md:
            description = markdown.markdown(self.inputs.description)
            logging.debug(f'Description converted to HTML:\n{description}')
        else:
            description = self.inputs.description
        self.description_label.setText(description)
        if self.inputs.dialog_title:
            self.setWindowTitle(self.inputs.dialog_title)
        if self.inputs.pass_button_text:
            self.pass_button.setText(self.inputs.pass_button_text)
        if self.inputs.pass_button_icon:
            icon = QIcon(self.inputs.pass_button_icon)
            if not icon:
                logging.warning(
                    f'Icon image for PASS button not found: {self.inputs.pass_button_icon}'
                )
            self.pass_button.setIcon(icon)
        if self.inputs.fail_button_text:
            self.fail_button.setText(self.inputs.fail_button_text)
        if self.inputs.fail_button_icon:
            icon = QIcon(self.inputs.fail_button_icon)
            if not icon:
                logging.warning(
                    f'Icon image for FAIL button not found: {self.inputs.fail_button_icon}'
                )
            self.fail_button.setIcon(icon)

        if self.stylesheet:
            self.app.setStyleSheet(self.stylesheet)

        # UI bindings
        self.pass_button.clicked.connect(self.pass_clicked)
        self.fail_button.clicked.connect(self.fail_clicked)
        self.exit_shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.exit_shortcut.activated.connect(self.fail_clicked)

    def resizeEvent(self, event):
        self.pass_button.setIconSize(self.pass_button.size())
        self.fail_button.setIconSize(self.fail_button.size())

    def closeEvent(self, event):
        """
        When closing the app (``X`` button), mark as fail instead of pass.
        """
        self.fail_clicked()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            # Disable exiting the app when pressing escape.
            # This avoids passing the step unintentionally by accidentally pressing escape.
            pass
        else:
            super().keyPressEvent(event)

    def pass_clicked(self):
        # Equivalent to `self.close()` and `self.done(0)`.
        # Using `QApplication.exit(0)` to enable testing exit code.
        self.app.exit(0)

    def fail_clicked(self):
        self.app.exit(1)
