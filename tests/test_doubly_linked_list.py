import pytest
from linked_list.doubly import DoublyLinkedList

@pytest.fixture(autouse=True)
def dll():
    return DoublyLinkedList()


@pytest.fixture(autouse=True)
def dll_123():
    dll = DoublyLinkedList()
    dll.append_values([1,2,3])
    return dll


def test_empty_list_initialization(dll):
    assert dll.size == 0
    assert dll.head is None
    assert dll.tail is None


def test_nonempty_list_initialization():
    initial_value = 123
    ll = DoublyLinkedList(initial_value)
    assert ll.size == 1
    assert ll.head.value == initial_value
    assert ll.tail.value == initial_value
    assert ll.head.next is None
    assert ll.tail.next is None


def test_list_append(dll):
    dll.append(1)
    assert dll.size == 1
    assert dll.head.value == 1
    assert dll.tail.value == 1

    dll.append(2)
    assert dll.size == 2
    assert dll.head.value == 1
    assert dll.tail.value == 2


def test_contains_returns_false_for_empty_list():
    linked_list = DoublyLinkedList()

    assert linked_list.contains("missing") is False


def test_contains_accepts_any_value_for_unconstrained_list():
    linked_list = DoublyLinkedList()
    value = {"key": ["nested", "value"]}
    linked_list.append("head")
    linked_list.append(value)
    linked_list.append(None)

    assert linked_list.contains({"key": ["nested", "value"]}) is True
    assert linked_list.contains(None) is True
    assert linked_list.contains({"key": ["other"]}) is False


def test_contains_rejects_mismatched_value_type_for_homogeneous_list():
    linked_list = DoublyLinkedList(value_type=int)
    linked_list.append(1)

    assert linked_list.contains(1) is True
    assert linked_list.contains(False) is False
    assert linked_list.contains("1") is False


def test_contains_checks_middle_value_once_for_odd_length_list():
    linked_list = DoublyLinkedList()
    linked_list.append("a")
    linked_list.append("b")
    linked_list.append("c")

    assert linked_list.contains("b") is True
    
    
def test_pop_head(dll_123):
    assert dll_123.size == 3

    dll_123.pop_head()
    assert dll_123.size == 2
    assert dll_123.head.value == 2


def test_pop_tail(dll_123):
    assert dll_123.size == 3

    dll_123.pop_tail()
    assert dll_123.size == 2
    assert dll_123.tail.value == 2
