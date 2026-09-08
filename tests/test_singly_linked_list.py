from linked_list.singly import SinglyLinkedList


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
