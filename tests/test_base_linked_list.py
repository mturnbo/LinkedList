import pytest

from linked_list.base import BaseLinkedList


class ConcreteLinkedList(BaseLinkedList):
    def append(self, value):
        return False


def test_linked_list():
    linked_list = ConcreteLinkedList()
    assert len(linked_list) == 0


def test_base_linked_list_is_abstract():
    with pytest.raises(TypeError):
        BaseLinkedList()


def test_linked_list_initializes_with_falsy_values():
    for value in (0, False, "", None):
        linked_list = ConcreteLinkedList(value)

        assert len(linked_list) == 1
        assert linked_list.head is linked_list.tail
        assert linked_list.head.value == value


def test_linked_list_enforces_initial_value_type():
    linked_list = ConcreteLinkedList(1, value_type=int)

    assert linked_list.value_type is int
    assert linked_list.head.value == 1


def test_linked_list_rejects_invalid_initial_value_type():
    try:
        ConcreteLinkedList("1", value_type=int)
    except TypeError as error:
        assert "Initial node value" in str(error)
    else:
        raise AssertionError("Expected TypeError for mismatched initial value.")


def test_linked_list_rejects_invalid_value_type_config():
    try:
        ConcreteLinkedList(value_type="int")
    except TypeError as error:
        assert "value_type must be" in str(error)
    else:
        raise AssertionError("Expected TypeError for invalid value_type config.")
