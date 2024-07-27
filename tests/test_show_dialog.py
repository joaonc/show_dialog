from src.inputs import Inputs
from src.ui.show_dialog import ShowDialog


def test_dialog_title(qtbot):
    dialog_title = 'foo bar'
    inputs = Inputs(dialog_title=dialog_title)
    dialog = ShowDialog(inputs)
    qtbot.addWidget(dialog)

    assert dialog.windowTitle() == dialog_title
