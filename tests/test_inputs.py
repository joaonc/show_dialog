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
