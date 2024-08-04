import pytest
from PySide6.QtCore import QResource

from src.show_dialog.inputs import Inputs
from tests.libs import resources_rc  # noqa: F401  # Needed to initialize resources
from tests.libs.config import TESTS_ROOT


@pytest.fixture
def inputs_instance():
    return Inputs(title='Foo', description='Bar')


@pytest.fixture
def testing_resources():
    """
    Register the test resources file at ``tests/libs/resources_rc.py``.

    Normal code uses the resources file ``src/show_dialog/ui/forms/resources_rc.py``.
    """
    resources_file = TESTS_ROOT / 'libs/resources_rc.py'
    if not resources_file.is_file():
        raise FileNotFoundError(resources_file)

    QResource.registerResource(str(resources_file))
    yield
    QResource.unregisterResource(str(resources_file))
