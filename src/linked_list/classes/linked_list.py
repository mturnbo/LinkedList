import sys
from classes.node import Node
from typing import Optional
from constants import PRINT_ARROW_SINGLE as LINK_ARROW, PRINT_ARROW_UP, PRINT_ARROW_DOWN, PRINT_ARROW_LEFT, PRINT_COLOR, RESET
from exceptions import *
from utils import filter_values, to_ll_type

class LinkedList:
    def __init__(self, initial_node_value: Any = None):
        self.head: Node | None = Node(initial_node_value) if initial_node_value else None
        self.tail: Node | None = self.head
        self.size: int = 0 if initial_node_value is None else 1

    def __len__(self):
        return self.size

    def get_node(self, index: int) -> Node:
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


    def get_values(self, count: Optional[int] = None) -> list[int | float | str | bool]:
        """
        Returns list of node values to count size, or head/tail if out of bounds
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

    def get_addresses(self, count: Optional[int] = None) -> list[int | float | str | bool]:
        """
        Returns list of node addresses
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