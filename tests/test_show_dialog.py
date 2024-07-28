from unittest.mock import patch

import pytest
from PySide6 import QtCore
from PySide6.QtGui import QColor, QPalette
from PySide6.QtTest import QTest

from src.inputs import Inputs
from src.ui.show_dialog import ShowDialog


@pytest.fixture
def show_dialog(request, qtbot):
    inputs = getattr(request, 'param', Inputs())
    dialog = ShowDialog(inputs)
    qtbot.addWidget(dialog)

    yield dialog


@pytest.mark.parametrize('show_dialog', [Inputs(dialog_title='foo bar')], indirect=True)
def test_dialog_title(show_dialog: ShowDialog):
    assert show_dialog.windowTitle() == 'foo bar'


@pytest.mark.parametrize(
    'show_dialog', [Inputs(title='foo bar', title_color='rgb(255, 0, 0)')], indirect=True
)
def test_title(show_dialog: ShowDialog):
    assert show_dialog.title_label.text() == 'foo bar'
    assert show_dialog.title_label.palette().color(QPalette.ColorRole.Text) == QColor.fromRgb(255,0,0)


@patch('PySide6.QtWidgets.QApplication.exit')
def test_pass_clicked(exit_mock, show_dialog: ShowDialog):
    """Clicking PASS button application exits with code 0."""
    QTest.mouseClick(show_dialog.pass_button, QtCore.Qt.MouseButton.LeftButton)
    exit_mock.assert_called_once_with(0)


@patch('PySide6.QtWidgets.QApplication.exit')
def test_fail_clicked(exit_mock, show_dialog: ShowDialog):
    """Clicking FAIL button application exits with code 1."""
    QTest.mouseClick(show_dialog.fail_button, QtCore.Qt.MouseButton.LeftButton)
    exit_mock.assert_called_once_with(1)
