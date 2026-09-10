import pytest

from linked_list.base import BaseLinkedList


class ConcreteLinkedList(BaseLinkedList):
    def append(self, value):
        if not self._accepts_value(value):
            return False

        from linked_list.node import Node

        new_node = Node(value)
        if self.head:
            self.tail.next = new_node
        else:
            self.head = new_node
        self.tail = new_node
        self.size += 1
        return True


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


def test_get_node_raises_index_error_for_empty_list():
    linked_list = ConcreteLinkedList()

    with pytest.raises(IndexError):
        linked_list.get_node(0)


def test_get_node_raises_index_error_for_out_of_bounds_index():
    linked_list = ConcreteLinkedList("head")

    with pytest.raises(IndexError):
        linked_list.get_node(-1)

    with pytest.raises(IndexError):
        linked_list.get_node(1)


def test_iter_yields_values():
    linked_list = ConcreteLinkedList()
    linked_list.append_values([1, 2, 3])

    assert list(linked_list) == [1, 2, 3]


def test_repr_includes_class_name_size_and_values():
    linked_list = ConcreteLinkedList()
    linked_list.append_values([1, "two", None])

    assert repr(linked_list) == (
        "ConcreteLinkedList(size=3, values=[1, 'two', None])"
    )


def test_repr_includes_value_type_when_configured():
    linked_list = ConcreteLinkedList(value_type=int)
    linked_list.append_values([1, 2])

    assert repr(linked_list) == (
        "ConcreteLinkedList(size=2, values=[1, 2], value_type=int)"
    )


def test_repr_shows_twenty_values_without_ellipsis():
    linked_list = ConcreteLinkedList()
    linked_list.append_values(list(range(20)))

    assert repr(linked_list) == (
        "ConcreteLinkedList(size=20, "
        "values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "
        "10, 11, 12, 13, 14, 15, 16, 17, 18, 19])"
    )


def test_repr_limits_values_to_twenty_with_ellipsis():
    linked_list = ConcreteLinkedList()
    linked_list.append_values(list(range(21)))

    assert repr(linked_list) == (
        "ConcreteLinkedList(size=21, "
        "values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "
        "10, 11, 12, 13, 14, 15, 16, 17, 18, 19, '...'])"
    )


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
