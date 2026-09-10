import pytest

from linked_list.base import BaseLinkedList
from exceptions import ValueTypeException


class ConcreteLinkedList(BaseLinkedList):
    def append(self, value):
        self._validate_value(value)

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


def test_from_values_builds_list():
    linked_list = ConcreteLinkedList.from_values([1, 2, 3])

    assert isinstance(linked_list, ConcreteLinkedList)
    assert linked_list.get_values() == [1, 2, 3]


def test_from_values_passes_configuration():
    linked_list = ConcreteLinkedList.from_values(
        [3, 1, 2],
        value_type=int,
        sortable=True,
    )

    assert linked_list.value_type is int
    assert linked_list.sortable is True
    assert linked_list.to_list() == [3, 1, 2]


def test_from_values_raises_without_partial_return_for_invalid_values():
    with pytest.raises(ValueTypeException):
        ConcreteLinkedList.from_values([1, "2", 3], value_type=int)


def test_to_list_aliases_get_values():
    linked_list = ConcreteLinkedList.from_values([1, 2, 3])

    assert linked_list.to_list() == linked_list.get_values()
    assert linked_list.to_list(2) == [1, 2]


def test_to_nodes_returns_nodes():
    linked_list = ConcreteLinkedList.from_values([1, 2, 3])

    nodes = linked_list.to_nodes()

    assert [node.value for node in nodes] == [1, 2, 3]
    assert nodes[0] is linked_list.head
    assert nodes[-1] is linked_list.tail


def test_to_nodes_honors_count():
    linked_list = ConcreteLinkedList.from_values([1, 2, 3])

    assert [node.value for node in linked_list.to_nodes(2)] == [1, 2]
    assert linked_list.to_nodes(0) == []


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


def test_repr_includes_sortable_when_configured():
    linked_list = ConcreteLinkedList(value_type=int, sortable=True)
    linked_list.append_values([1, 2])

    assert repr(linked_list) == (
        "ConcreteLinkedList(size=2, values=[1, 2], value_type=int, sortable=True)"
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
    except ValueTypeException as error:
        assert "Expected int" in str(error)
    else:
        raise AssertionError("Expected TypeError for mismatched initial value.")


def test_linked_list_rejects_invalid_value_type_config():
    try:
        ConcreteLinkedList(value_type="int")
    except TypeError as error:
        assert "value_type must be" in str(error)
    else:
        raise AssertionError("Expected TypeError for invalid value_type config.")


def test_linked_list_rejects_invalid_sort_key_config():
    with pytest.raises(TypeError):
        ConcreteLinkedList(sort_key="value")


def test_sortable_list_requires_value_type_or_sort_key():
    with pytest.raises(TypeError):
        ConcreteLinkedList(sortable=True)


def test_sortable_list_rejects_unsortable_initial_value():
    with pytest.raises(TypeError):
        ConcreteLinkedList({"key": "value"}, value_type=dict, sortable=True)


def test_append_values_raises_for_mismatched_value_type():
    linked_list = ConcreteLinkedList(value_type=int)

    with pytest.raises(ValueTypeException):
        linked_list.append_values([1, "2", 3])

    assert linked_list.get_values() == []
