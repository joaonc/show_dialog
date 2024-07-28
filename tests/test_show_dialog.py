from unittest.mock import patch

import pytest
from PySide6 import QtCore
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


@patch('PySide6.QtWidgets.QApplication.exit')
def test_pass_clicked(exit_mock, show_dialog: ShowDialog):
    QTest.mouseClick(show_dialog.pass_button, QtCore.Qt.MouseButton.LeftButton)
    exit_mock.assert_called_once_with(0)


@patch('PySide6.QtWidgets.QApplication.exit')
def test_fail_clicked(exit_mock, show_dialog: ShowDialog):
    QTest.mouseClick(show_dialog.fail_button, QtCore.Qt.MouseButton.LeftButton)
    exit_mock.assert_called_once_with(1)
