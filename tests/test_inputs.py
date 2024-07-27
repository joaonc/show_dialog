import json

import pytest

from inputs import Inputs


@pytest.fixture
def inputs_instance():
    return Inputs(title='Foo', description='Bar')


def test_instantiation():
    inputs = Inputs(title='Foo', description='Bar')

    assert inputs.title == 'Foo'
    assert inputs.description == 'Bar'


def test_to_file(tmp_path, inputs_instance):
    file = tmp_path / 'test.json'
    inputs_instance.to_file(file)

    with open(file) as f:
        data = json.load(f)

    inputs_instance_2 = Inputs.from_dict(data)
    assert inputs_instance == inputs_instance_2


def test_from_file(tmp_path, inputs_instance):
    file = tmp_path / 'test.json'
    inputs_instance.to_file(file)

    inputs_instance_2 = Inputs.from_file(file)
    assert inputs_instance == inputs_instance_2
