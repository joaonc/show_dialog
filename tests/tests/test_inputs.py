import json

import pytest
import yaml

from src.show_dialog.inputs import DataFileType, Inputs
from tests.libs.fixtures import inputs_instance  # noqa: F401


class TestDataFileType:
    @pytest.mark.parametrize(
        'file, expected',
        [
            ('foo.json', DataFileType.JSON),
            ('foo.JSON', DataFileType.JSON),
            ('foo.yaml', DataFileType.YAML),
            ('foo.yMl', DataFileType.YAML),
        ],
    )
    def test_from_file(self, file, expected):
        assert DataFileType.from_file(file) is expected


class TestInputs:
    def test_instantiation(self):
        inputs = Inputs(dialog_title='Baz', title='Foo', description='Bar')

        assert inputs.dialog_title == 'Baz'
        assert inputs.title == 'Foo'
        assert inputs.description == 'Bar'

    def test_instantiation_defaults(self):
        inputs = Inputs()

        assert inputs.dialog_title == ''
        assert inputs.title == ''
        assert inputs.description == ''

    @pytest.mark.parametrize(
        'file_name, file_type',
        [
            ('test.json', DataFileType.JSON),
            ('test.yaml', DataFileType.YAML),
            ('test.json', DataFileType.AUTO),
            ('test.yaml', DataFileType.AUTO),
            ('test.yml', DataFileType.AUTO),
        ],
    )
    def test_to_file(self, tmp_path, inputs_instance, file_name, file_type):
        file = tmp_path / file_name
        inputs_instance.to_file(file)

        with open(file) as f:
            open_func = (
                json.load if DataFileType.from_file(file) is DataFileType.JSON else yaml.safe_load
            )
            data = open_func(f)

        inputs_instance_2 = Inputs.from_dict(data)
        assert inputs_instance == inputs_instance_2

    def test_to_file_invalid(self, tmp_path, inputs_instance):
        file = tmp_path / 'foo.bar'
        with pytest.raises(ValueError):
            inputs_instance.to_file(file)

    @pytest.mark.parametrize(
        'file_name',
        [
            'test.json',
            'test.yaml',
            'test.yml',
        ],
    )
    def test_from_file(self, tmp_path, inputs_instance, file_name):
        file = tmp_path / file_name
        inputs_instance.to_file(file)

        inputs_instance_2 = Inputs.from_file(file)
        assert inputs_instance == inputs_instance_2

    def test_from_file_invalid(self, tmp_path, inputs_instance):
        file = tmp_path / 'foo.bar'
        with pytest.raises(ValueError):
            Inputs.from_file(file)
