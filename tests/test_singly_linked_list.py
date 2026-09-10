import pytest
from linked_list.singly import SinglyLinkedList

@pytest.fixture(autouse=True)
def sll():
    return SinglyLinkedList()

@pytest.fixture(autouse=True)
def sll_123():
    dll = SinglyLinkedList()
    dll.append_values([1,2,3])
    return dll


def test_empty_list_initialization(sll):
    assert sll.size == 0
    assert sll.head is None
    assert sll.tail is None


def test_nonempty_list_initialization():
    initial_value = 123
    ll = SinglyLinkedList(initial_value)
    assert ll.size == 1
    assert ll.head.value == initial_value
    assert ll.tail.value == initial_value
    assert ll.head.next is None
    assert ll.tail.next is None


def test_list_append(sll):
    sll.append(1)
    assert sll.size == 1
    assert sll.head.value == 1
    assert sll.tail.value == 1

    sll.append(2)
    assert sll.size == 2
    assert sll.head.value == 1
    assert sll.tail.value == 2


def test_list_multiple_append(sll):
    vals = [1, 2, 3]
    for val in vals:
        sll.append(val)
        assert sll.head.value == vals[0]
        assert sll.tail.value == val

    assert sll.size == len(vals)


def test_get_node(sll_123):
    assert sll_123.get_node(1).value == 2


def test_insert(sll_123):
    sll_123.insert(1, 4)
    assert sll_123.get_node(1).value == 4


def test_replace(sll_123):
    sll_123.replace(1, 4)
    assert sll_123.get_node(1).value == 4

    sll_123.replace(2, 5)
    assert sll_123.get_node(2).value == 5


def test_pop_head(sll_123):
    assert sll_123.size == 3

    sll_123.pop_head()
    assert sll_123.size == 2
    assert sll_123.head.value == 2


def test_pop_tail(sll_123):
    assert sll_123.size == 3

    sll_123.pop_tail()
    assert sll_123.size == 2
    assert sll_123.tail.value == 2


def test_contains(sll_123):
    assert sll_123.contains(1) is True
    assert sll_123.contains(2) is True
    assert sll_123.contains(4) is False


def test_remove(sll_123):
    sll_123.remove(1)
    assert sll_123.size == 2


def test_reverse(sll_123):
    sll_123.reverse()
    assert sll_123.head.value == 3
    assert sll_123.tail.value == 1


def test_append_and_prepend_accept_any_values():
    linked_list = SinglyLinkedList()
    values = [0, False, "", None, {"key": "value"}]

    assert linked_list.append_values(values) == len(values)
    assert linked_list.get_values() == values

    marker = object()
    assert linked_list.prepend(marker) is True
    assert linked_list.head.value is marker


def test_insert_returns_true_for_boundary_insertions():
    linked_list = SinglyLinkedList()

    assert linked_list.insert(0, "head") is True
    assert linked_list.insert(99, "tail") is True
    assert linked_list.get_values() == ["head", "tail"]


def test_replace_returns_false_for_invalid_index():
    linked_list = SinglyLinkedList()
    linked_list.append_values(["a", "b"])

    assert linked_list.replace(-1, "x") is False
    assert linked_list.replace(2, "x") is False
    assert linked_list.replace(1, "x") is True
    assert linked_list.get_values() == ["a", "x"]


def test_pop_head_removes_and_returns_head_node():
    linked_list = SinglyLinkedList()
    linked_list.append_values(["a", "b"])

    popped_node = linked_list.pop_head()

    assert popped_node.value == "a"
    assert popped_node.next is None
    assert linked_list.get_values() == ["b"]
    assert len(linked_list) == 1


def test_pop_tail_removes_and_returns_tail_node():
    linked_list = SinglyLinkedList()
    linked_list.append_values(["a", "b", "c"])

    popped_node = linked_list.pop_tail()

    assert popped_node.value == "c"
    assert popped_node.next is None
    assert linked_list.get_values() == ["a", "b"]
    assert linked_list.tail.value == "b"
    assert len(linked_list) == 2


def test_popping_only_node_clears_list():
    linked_list = SinglyLinkedList("only")

    popped_node = linked_list.pop_tail()

    assert popped_node.value == "only"
    assert linked_list.head is None
    assert linked_list.tail is None
    assert len(linked_list) == 0


def test_remove_uses_pop_behavior_for_head_and_tail():
    linked_list = SinglyLinkedList()
    linked_list.append_values(["a", "b", "c"])

    assert linked_list.remove(0) is True
    assert linked_list.get_values() == ["b", "c"]
    assert linked_list.remove(1) is True
    assert linked_list.get_values() == ["b"]


def test_homogeneous_list_accepts_matching_values():
    linked_list = SinglyLinkedList(value_type=str)

    assert linked_list.append("a") is True
    assert linked_list.prepend("b") is True
    assert linked_list.insert(1, "c") is True
    assert linked_list.replace(1, "d") is True
    assert linked_list.get_values() == ["b", "d", "a"]


def test_homogeneous_list_rejects_mismatched_values():
    linked_list = SinglyLinkedList(value_type=int)

    assert linked_list.append(1) is True
    assert linked_list.append("2") is False
    assert linked_list.prepend(False) is False
    assert linked_list.insert(1, 2.0) is False
    assert linked_list.replace(0, "1") is False
    assert linked_list.get_values() == [1]
    assert linked_list.contains("1") is False


def test_contains_accepts_any_value_for_unconstrained_list():
    linked_list = SinglyLinkedList()
    value = {"key": ["nested", "value"]}
    linked_list.append(value)

    assert linked_list.contains({"key": ["nested", "value"]}) is True
    assert linked_list.contains({"key": ["other"]}) is False


def test_get_cycle_start_index_methods():
    ll = SinglyLinkedList()
    ll.append_values([1, 2, 3, 4, 5])
    assert ll.get_cycle_start_index() is None

    ll.create_cycle(2)
    assert ll.get_cycle_start_index() == 2


def test_create_cycle_rejects_invalid_start_index():
    ll = SinglyLinkedList()
    ll.append_values([1, 2, 3])

    assert ll.create_cycle(-1) is False
    assert ll.create_cycle(2) is False
    assert ll.create_cycle(3) is False
    assert ll.has_cycle() is False


def test_sort_merge():
    ll = SinglyLinkedList()
    values = [4, 2, 5, 1, 3]
    for value in values:
        ll.append(value)

    assert ll.sort(method=1) is True
    assert ll.get_values() == [1, 2, 3, 4, 5]
    assert ll.head.value == 1
    assert ll.tail.value == 5


def test_sort_insertion():
    ll = SinglyLinkedList()
    ll.append_values([4, 2, 5, 1, 3])

    assert ll.sort(method=2) is True
    assert ll.get_values() == [1, 2, 3, 4, 5]
    assert ll.head.value == 1
    assert ll.tail.value == 5


def test_sort_returns_false_for_invalid_method():
    ll = SinglyLinkedList()
    ll.append_values([2, 1])

    assert ll.sort(method=3) is False
    assert ll.get_values() == [2, 1]


def test_sort_returns_false_without_mutation_for_mixed_unsortable_values():
    ll = SinglyLinkedList()
    ll.append_values([2, "1", 3])

    assert ll.sort(method=1) is False
    assert ll.get_values() == [2, "1", 3]
    assert ll.tail.value == 3


def test_sort_homogeneous_list():
    ll = SinglyLinkedList(value_type=str)
    ll.append_values(["c", "a", "b"])

    assert ll.sort() is True
    assert ll.get_values() == ["a", "b", "c"]
