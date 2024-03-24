import pytest
from src.simple_class import SimpleClass


@pytest.fixture
def example_simple_class():
    return SimpleClass("some-attribute")

def test_always_passes():
    assert True

# def test_always_fails():
#     assert False

def test_with_class(example_simple_class):
    assert example_simple_class.getAttribute() == "some-attribute"

def test_class_fails_with_error(example_simple_class):
    with pytest.raises(Exception) as e_info:
        example_simple_class.kaboom()
    assert str(e_info.value) == "kaboom"