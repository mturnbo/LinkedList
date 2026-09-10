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


def assert_doubly_links(linked_list):
    current = linked_list.head
    previous = None
    count = 0

    while current:
        assert current.prev is previous
        previous = current
        current = current.next
        count += 1

    assert previous is linked_list.tail
    assert count == linked_list.size


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
    assert_doubly_links(dll)


def test_prepend(dll):
    assert dll.prepend(2) is True
    assert dll.prepend(1) is True

    assert dll.get_values() == [1, 2]
    assert dll.head.prev is None
    assert dll.tail.next is None
    assert_doubly_links(dll)


def test_prepend_values_preserves_order(dll):
    assert dll.prepend_values([1, 2, 3]) == 3

    assert dll.get_values() == [1, 2, 3]
    assert_doubly_links(dll)


def test_insert_at_head_middle_and_tail(dll):
    assert dll.insert(0, "b") is True
    assert dll.insert(0, "a") is True
    assert dll.insert(2, "d") is True
    assert dll.insert(2, "c") is True

    assert dll.get_values() == ["a", "b", "c", "d"]
    assert_doubly_links(dll)


def test_insert_rejects_mismatched_value_type():
    dll = DoublyLinkedList(value_type=int)

    assert dll.insert(0, 1) is True
    assert dll.insert(1, "2") is False
    assert dll.get_values() == [1]
    assert_doubly_links(dll)


def test_replace(dll_123):
    assert dll_123.replace(1, 4) is True
    assert dll_123.get_values() == [1, 4, 3]
    assert_doubly_links(dll_123)


def test_replace_returns_false_for_invalid_index_and_type():
    dll = DoublyLinkedList(value_type=int)
    dll.append_values([1, 2])

    assert dll.replace(-1, 3) is False
    assert dll.replace(2, 3) is False
    assert dll.replace(1, "3") is False
    assert dll.get_values() == [1, 2]
    assert_doubly_links(dll)


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

    popped_node = dll_123.pop_head()
    assert popped_node.value == 1
    assert popped_node.prev is None
    assert popped_node.next is None
    assert dll_123.size == 2
    assert dll_123.head.value == 2
    assert dll_123.head.prev is None
    assert_doubly_links(dll_123)


def test_pop_tail(dll_123):
    assert dll_123.size == 3

    popped_node = dll_123.pop_tail()
    assert popped_node.value == 3
    assert popped_node.prev is None
    assert popped_node.next is None
    assert dll_123.size == 2
    assert dll_123.tail.value == 2
    assert dll_123.tail.next is None
    assert_doubly_links(dll_123)


def test_pop_only_node_clears_list():
    dll = DoublyLinkedList("only")

    popped_node = dll.pop_head()

    assert popped_node.value == "only"
    assert dll.head is None
    assert dll.tail is None
    assert len(dll) == 0


def test_remove_head_middle_tail_and_only_node():
    dll = DoublyLinkedList()
    dll.append_values(["a", "b", "c", "d"])

    assert dll.remove(0) is True
    assert dll.get_values() == ["b", "c", "d"]
    assert_doubly_links(dll)

    assert dll.remove(1) is True
    assert dll.get_values() == ["b", "d"]
    assert_doubly_links(dll)

    assert dll.remove(1) is True
    assert dll.get_values() == ["b"]
    assert_doubly_links(dll)

    assert dll.remove(0) is True
    assert dll.head is None
    assert dll.tail is None
    assert len(dll) == 0


def test_reverse(dll_123):
    dll_123.reverse()
    assert dll_123.head.value == 3
    assert dll_123.tail.value == 1
    assert_doubly_links(dll_123)


def test_create_cycle_links_tail_to_head(dll_123):
    assert dll_123.create_cycle(0) is True

    assert dll_123.tail.next is dll_123.head
    assert dll_123.head.prev is dll_123.tail
    assert dll_123.get_cycle_start_index() == 0


def test_create_cycle_rejects_non_head_start_index(dll_123):
    assert dll_123.create_cycle(1) is False

    assert dll_123.tail.next is None
    assert dll_123.head.prev is None
    assert dll_123.get_cycle_start_index() is None
    assert_doubly_links(dll_123)


def test_create_cycle_rejects_empty_list():
    dll = DoublyLinkedList()

    assert dll.create_cycle(0) is False


def test_sort_merge():
    ll = DoublyLinkedList()
    values = [4, 2, 5, 1, 3]
    for value in values:
        ll.append(value)

    assert ll.sort(method=1) is True
    assert ll.get_values() == [1, 2, 3, 4, 5]
    assert ll.head.value == 1
    assert ll.tail.value == 5
    assert_doubly_links(ll)


def test_sort_insertion():
    ll = DoublyLinkedList()
    ll.append_values([4, 2, 5, 1, 3])

    assert ll.sort(method=2) is True
    assert ll.get_values() == [1, 2, 3, 4, 5]
    assert ll.head.value == 1
    assert ll.tail.value == 5
    assert_doubly_links(ll)


def test_sort_returns_false_for_invalid_method():
    ll = DoublyLinkedList()
    ll.append_values([2, 1])

    assert ll.sort(method=3) is False
    assert ll.get_values() == [2, 1]


def test_sort_returns_false_without_mutation_for_mixed_unsortable_values():
    ll = DoublyLinkedList()
    ll.append_values([2, "1", 3])

    assert ll.sort(method=1) is False
    assert ll.get_values() == [2, "1", 3]
    assert ll.tail.value == 3


def test_sort_homogeneous_list():
    ll = DoublyLinkedList(value_type=str)
    ll.append_values(["c", "a", "b"])

    assert ll.sort() is True
    assert ll.get_values() == ["a", "b", "c"]
