from unittest.mock import patch

import pytest
from PySide6 import QtCore
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from src.inputs import Inputs
from src.ui.show_dialog import ShowDialog


@pytest.fixture(scope='session')
def app():
    _app = QApplication([])
    yield _app


@pytest.fixture
def show_dialog(request, app, qtbot):
    inputs = getattr(request, 'param', Inputs())
    dialog = ShowDialog(app, inputs)
    qtbot.addWidget(dialog)

    yield dialog


@pytest.mark.parametrize('show_dialog', [Inputs(dialog_title='foo bar')], indirect=True)
def test_dialog_title(show_dialog: ShowDialog):
    assert show_dialog.windowTitle() == 'foo bar'


@pytest.mark.parametrize('show_dialog', [Inputs(title='foo bar')], indirect=True)
def test_title(show_dialog: ShowDialog):
    assert show_dialog.title_label.text() == 'foo bar'


@pytest.mark.parametrize('show_dialog', [Inputs(description='foo bar')], indirect=True)
def test_description(show_dialog: ShowDialog):
    assert show_dialog.description_label.text() == 'foo bar'


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
