from src.show_dialog.utils_qt import list_resources
from tests.libs.fixtures import testing_resources  # noqa: F401


class TestListResources:
    def test_non_recursive(self, testing_resources):
        files = list_resources(':/stylesheets')
        assert files == [':/stylesheets/style_01.css']
