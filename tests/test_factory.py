import pytest

from linked_list import (
    CycleDetectedException,
    DoublyLinkedList,
    EmptyValueException,
    LinkedList,
    Node,
    SinglyLinkedList,
    ValueTypeException,
)


def test_public_api_exports_package_objects():
    assert Node(1).value == 1
    assert issubclass(SinglyLinkedList, object)
    assert issubclass(DoublyLinkedList, object)
    assert issubclass(EmptyValueException, ValueError)
    assert issubclass(ValueTypeException, TypeError)
    assert issubclass(CycleDetectedException, RuntimeError)


@pytest.mark.parametrize("list_type", ["s", "single", "singly", "SINGLY"])
def test_factory_creates_singly_linked_list(list_type):
    linked_list = LinkedList.create(list_type)

    assert isinstance(linked_list, SinglyLinkedList)
    assert len(linked_list) == 0


@pytest.mark.parametrize("list_type", ["d", "double", "doubly", "DOUBLY"])
def test_factory_creates_doubly_linked_list(list_type):
    linked_list = LinkedList.create(list_type)

    assert isinstance(linked_list, DoublyLinkedList)
    assert len(linked_list) == 0


def test_factory_create_passes_initial_value_and_configuration():
    linked_list = LinkedList.create(
        "singly",
        1,
        value_type=int,
        sortable=True,
    )

    assert isinstance(linked_list, SinglyLinkedList)
    assert linked_list.to_list() == [1]
    assert linked_list.value_type is int
    assert linked_list.sortable is True


def test_factory_create_allows_none_initial_value():
    linked_list = LinkedList.create("doubly", None)

    assert isinstance(linked_list, DoublyLinkedList)
    assert linked_list.to_list() == [None]


def test_factory_from_values_builds_selected_list_type():
    linked_list = LinkedList.from_values("doubly", [3, 1, 2])

    assert isinstance(linked_list, DoublyLinkedList)
    assert linked_list.to_list() == [3, 1, 2]


def test_factory_from_values_passes_sort_key():
    linked_list = LinkedList.from_values(
        "singly",
        [{"priority": 2}, {"priority": 1}],
        sort_key=lambda item: item["priority"],
    )

    assert linked_list.sort() is True
    assert linked_list.to_list() == [{"priority": 1}, {"priority": 2}]


def test_factory_raises_for_unknown_list_type():
    with pytest.raises(ValueError):
        LinkedList.create("circular")

    with pytest.raises(ValueError):
        LinkedList.from_values("circular", [1, 2, 3])
