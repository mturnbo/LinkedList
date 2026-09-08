from linked_list.node import Node
from typing import Any, Optional
from exceptions import *

class BaseLinkedList:
    def __init__(self, initial_node_value: Any | None = None):
        self.head: Node | None = (
            Node(initial_node_value) if initial_node_value is not None else None
        )
        self.tail: Node | None = self.head
        self.size: int = 0 if initial_node_value is None else 1


    def __len__(self):
        return self.size


    def get_node(self, index: int) -> Node | None:
        """
        Returns node at index, or head/tail if out of bounds
        Time complexity: O(n)
        """

        if index <= 0: return self.head
        if index >= self.size - 1: return self.tail

        current_node = self.head
        for _ in range(index):
            current_node = current_node.next

        return current_node


    def get_node_address(self, index: int) -> int:
        return id(self.get_node(index))


    def get_values(self, count: Optional[int] = None) -> list[Any]:
        """
        Returns a list of node values to count size, or head/tail if out of bounds
        Time complexity: O(n)
        """

        if count is None: count = self.size
        if count <= 0: return []
        index = min(count, self.size)
        values = []

        current_node = self.head
        for _ in range(index):
            values.append(current_node.value)
            current_node = current_node.next

        return values


    def get_addresses(self, count: Optional[int] = None) -> list[int]:
        """
        Returns a list of node addresses
        Time complexity: O(n)
        """

        if count is None: count = self.size
        if count <= 0: return []
        index = min(count, self.size)
        addresses = []

        current_node = self.head
        for _ in range(index):
            addresses.append(id(current_node))
            current_node = current_node.next

        return addresses


    def clear(self, iterate: bool = False) -> bool:
        """
        Clears the linked list, removing all nodes and resetting size to 0.
        All nodes can be removed by setting the head of the list to None.
        This makes the entire list unreachable, and Python's garbage collector automatically reclaims the memory.
        An iterative option is included for exploring memory management.
        """
        if iterate:
            # Time complexity: O(n)
            current = self.head
            while current:
                # Store the next node to avoid losing the reference
                next_node = current.next
                current = next_node
            self.head = None
        else:
            # Time complexity: O(1)
            self.head = self.tail = None
            self.size = 0

        return True
