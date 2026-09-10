from typing import Any
from linked_list.node import Node
from linked_list.base import BaseLinkedList, _MISSING

class DoublyLinkedList(BaseLinkedList):
    def __init__(
        self,
        initial_node_value: Any = _MISSING,
        value_type: type | None = None,
    ):
        super().__init__(initial_node_value, value_type=value_type)


    def get_node(self, index: int):
        """
        Retrieves a node at the specified index.
        Time complexity: O(n)
        """

        if index <= 0: return self.head
        if index >= self.size - 1: return self.tail

        if index <= self.size // 2:
            current_node = self.head
            for _ in range(index):
                current_node = current_node.next
        else:
            current_node = self.tail
            for _ in range(self.size - index):
                current_node = current_node.prev

        return current_node

    def append(self, value: Any) -> bool:
        """
        Appends a new node with the specified value to the end of the list.
        Time complexity: O(1)
        """

        if not self._accepts_value(value) or self.has_cycle():
            return False

        new_node = Node(value)
        if self.head:
            self.tail.next = new_node
            new_node.prev = self.tail
        else:
            self.head = new_node
        self.tail = new_node
        self.size += 1
        return True


    def remove(self, index: int):
        """
        Removes the node at the specified index.
        Time complexity: O(n)
        """
        if index < 0 or index >= self.size: return False
        if index == 0:
            self.head = self.head.next
            self.head.prev = None
        elif index >= self.size - 1:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            current_node = self.get_node(index -1)
            next_node = current_node.next.next
            current_node.next = next_node
            next_node.prev = current_node
        self.size -= 1
        return True


    def contains(self, value: Any) -> bool:
        """
        Determines if the list contains a node with the specified value.
        Time complexity: O(n)
        """

        if not self._accepts_value(value):
            return False

        forward = self.head
        backward = self.tail

        for _ in range((self.size + 1) // 2):
            if forward and forward.value == value:
                return True
            if backward and backward.value == value:
                return True
            forward = forward.next if forward else None
            backward = backward.prev if backward else None

        return False


