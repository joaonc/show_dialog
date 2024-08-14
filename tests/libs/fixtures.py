import pytest
from PySide6.QtCore import QResource

from src.show_dialog.inputs import Inputs
from tests.libs import resources_rc  # noqa: F401  # Needed to initialize resources
from tests.libs.config import TESTS_ROOT, PROJECT_ROOT


@pytest.fixture
def inputs_instance():
    return Inputs(title='Foo', description='Bar')


@pytest.fixture
def testing_resources():
    """
    Register the test resources file at ``tests/libs/resources_rc.py``.

    Normal code uses the resources file ``src/show_dialog/ui/forms/resources_rc.py``.
    """
    test_resource_file = TESTS_ROOT / 'libs/resources_rc.py'
    if not test_resource_file.is_file():
        raise FileNotFoundError(test_resource_file)

    src_resource_file = PROJECT_ROOT / 'src/show_dialog/ui/forms/resources_rc.py'
    if not src_resource_file.is_file():
        raise FileNotFoundError(src_resource_file)

    # When registering resources, they're registered on top of (ie, in addition to) the existing
    # ones. In order to have only the test resources, the src resources need to be unregistered
    # first.

    QResource.unregisterResource(str(src_resource_file))
    QResource.registerResource(str(test_resource_file))
    yield
    QResource.unregisterResource(str(test_resource_file))
    QResource.registerResource(str(src_resource_file))
