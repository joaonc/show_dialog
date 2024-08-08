import logging

import markdown
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QDialog

from ..inputs import Inputs
from ..utils_qt import set_layout_visibility
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
        self.timer = None

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
        if self.inputs.timeout:
            self.timeout_increase_button.setIconSize(self.timeout_increase_button.size())
            self.timeout_increase_button.clicked.connect(self.timeout_increase_clicked)
            self.timeout_progress_bar.setMinimum(0)
            self.timeout_progress_bar.setMaximum(self.inputs.timeout)
            self.timeout_progress_bar.setValue(self.inputs.timeout)
            self.timer = QTimer()
            self.timer.setInterval(1000)
            self.timer.timeout.connect(self.timer_timeout)
            self.timer.start()
            if self.inputs.timeout_text:
                self.timeout_progress_bar.setFormat(self.inputs.timeout_text)
            else:
                self.timeout_progress_bar.setTextVisible(False)
        else:
            set_layout_visibility(self.timeout_h_layout, False)

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

    def timer_timeout(self):
        new_value = self.timeout_progress_bar.value() - self.timer.interval() / 1000
        self.timeout_progress_bar.setValue(new_value)
        if new_value <= 0:
            logging.debug('Timeout.')
            if self.inputs.timeout_pass:
                self.pass_clicked()
            else:
                self.fail_clicked()

    def timeout_increase_clicked(self):
        timeout_increase = 10
        new_value = self.timeout_progress_bar.value() + timeout_increase
        if new_value > self.timeout_progress_bar.maximum():
            self.timeout_progress_bar.setMaximum(new_value)
        self.timeout_progress_bar.setValue(new_value)

    def pass_clicked(self):
        # Equivalent to `self.close()` and `self.done(0)`.
        # Using `QApplication.exit(0)` to enable testing exit code.
        self.app.exit(0)

    def fail_clicked(self):
        self.app.exit(1)
