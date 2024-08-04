from src.show_dialog.utils_qt import list_resources, read_resource_file
from tests.libs.config import TEST_ASSETS_DIR
from tests.libs.fixtures import testing_resources  # noqa: F401


class TestListResources:
    def test_resource_path(self, testing_resources):
        files = list_resources(':/stylesheets')
        assert files == [':/stylesheets/style_01.css']

    def test_absolute_path(self):
        base_path = TEST_ASSETS_DIR / 'stylesheets'
        files = list_resources(base_path)
        assert files == [f'{base_path}/style_01.css']


class TestReadResourceFile:
    def test_read_resource_file(self, testing_resources):
        file_content = read_resource_file(':/stylesheets/style_01.css')
        assert 'Test stylesheet' in file_content

    def test_absolute_path(self):
        file_content = read_resource_file(TEST_ASSETS_DIR / 'stylesheets/style_01.css')
        assert 'Test stylesheet' in file_content
