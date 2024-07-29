import json

import pytest
import yaml

from src.inputs import Inputs


@pytest.fixture
def inputs_instance():
    return Inputs(title='Foo', description='Bar')


def test_instantiation():
    inputs = Inputs(title='Foo', description='Bar')

    assert inputs.title == 'Foo'
    assert inputs.description == 'Bar'


def test_to_json_file(tmp_path, inputs_instance):
    file = tmp_path / 'test.json'
    inputs_instance.to_json_file(file)

    with open(file) as f:
        data = json.load(f)

    inputs_instance_2 = Inputs.from_dict(data)
    assert inputs_instance == inputs_instance_2


def test_to_yaml_file(tmp_path, inputs_instance):
    file = tmp_path / 'test.yaml'
    inputs_instance.to_yaml_file(file)

    with open(file) as f:
        data = yaml.safe_load(f)

    inputs_instance_2 = Inputs.from_dict(data)
    assert inputs_instance == inputs_instance_2


def test_from_json_file(tmp_path, inputs_instance):
    file = tmp_path / 'test.json'
    inputs_instance.to_json_file(file)

    inputs_instance_2 = Inputs.from_json_file(file)
    assert inputs_instance == inputs_instance_2


def test_from_yaml_file(tmp_path, inputs_instance):
    file = tmp_path / 'test.yaml'
    inputs_instance.to_yaml_file(file)

    inputs_instance_2 = Inputs.from_yaml_file(file)
    assert inputs_instance == inputs_instance_2
