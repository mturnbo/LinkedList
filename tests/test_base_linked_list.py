from linked_list.base import BaseLinkedList


def test_linked_list():
    linked_list = BaseLinkedList()
    assert len(linked_list) == 0


def test_linked_list_initializes_with_falsy_values():
    for value in (0, False, ""):
        linked_list = BaseLinkedList(value)

        assert len(linked_list) == 1
        assert linked_list.head is linked_list.tail
        assert linked_list.head.value == value
