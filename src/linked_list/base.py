from abc import ABC, abstractmethod
from linked_list.node import Node
from typing import Any, Optional

_MISSING = object()

class BaseLinkedList:
    def __init__(
        self,
        initial_node_value: Any = _MISSING,
        value_type: type | None = None,
    ):
        if value_type is not None and not self._is_valid_value_type(value_type):
            raise TypeError("value_type must be a type.")

        self.value_type = value_type
        self.head: Node | None = (
            Node(initial_node_value) if initial_node_value is not _MISSING else None
        )
        self.tail: Node | None = self.head
        self.size: int = 0 if initial_node_value is _MISSING else 1

        if self.head and not self._accepts_value(self.head.value):
            raise TypeError(
                f"Initial node value must be of type {self._value_type_name()}."
            )


    def _is_valid_value_type(self, value_type: type) -> bool:
        return isinstance(value_type, type)


    def _accepts_value(self, value: Any) -> bool:
        if self.value_type is None:
            return True

        return type(value) is self.value_type


    def _value_type_name(self) -> str:
        if self.value_type is None:
            return "Any"

        return self.value_type.__name__


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


    def _values_are_sortable(self) -> bool:
        values = self.get_values()
        try:
            sorted(values)
        except TypeError:
            return False

        return True


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

    @abstractmethod
    def append(self, value: Any) -> None:
        """
        Appends a new node with the given value to the end of the list.
        Time complexity: O(n)
        """
        pass


    def append_values(self, values: list[Any]) -> int:
        """
        Adds multiple new nodes to the end of the linked list.
        Time complexity: O(n)
        """
        appended_count = 0
        for value in values:
            if self.append(value):
                appended_count += 1

        return appended_count


    def pop_head(self) -> Node | None:
        """
        Removes and returns the head node.
        Time complexity: O(1)
        """

        if self.head is None:
            return None

        popped_node = self.head
        self.head = popped_node.next
        if self.head is None:
            self.tail = None
        popped_node.next = None
        self.size -= 1

        return popped_node


    def pop_tail(self) -> Node | None:
        """
        Removes and returns the tail node.
        Time complexity: O(n)
        """

        if self.tail is None or self._has_cycle():
            return None
        if self.size == 1:
            return self.pop_head()

        previous_node = self.get_node(self.size - 2)
        popped_node = self.tail
        previous_node.next = None
        self.tail = previous_node
        self.size -= 1

        return popped_node


    def _has_cycle(self) -> bool:
        """
        Detects if the linked list has a cycle.
        Floyd's Cycle-Finding Algorithm
        Time complexity: O(n)
        """

        fast_runner = slow_runner = self.head
        while fast_runner and fast_runner.next:
            fast_runner = fast_runner.next.next
            slow_runner = slow_runner.next
            if fast_runner is slow_runner:
                return True

        return False


    def get_cycle_start_index(self) -> Optional[int]:
        """
        Returns the index of the node where the cycle begins, or None if no cycle.
        Floyd's Cycle-Finding Algorithm
        Time complexity: O(n)
        """

        fast_runner = slow_runner = self.head
        while fast_runner and fast_runner.next:
            fast_runner = fast_runner.next.next
            slow_runner = slow_runner.next
            if fast_runner is slow_runner:
                break
        else:
            return None

        slow_runner = self.head
        index = 0
        while slow_runner is not fast_runner:
            slow_runner = slow_runner.next
            fast_runner = fast_runner.next
            index += 1

        return index


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


    def create_cycle(self, start: int):
        """
        Create a cycle in the linked list.
        Accepts start index.  Start index must be less than tail index.
        Example:
        1 → 2 → 3 → 4 → 5
                ↑       ↓
                ← ← ← ← ←
        Time complexity: O(1)
        """

        if self._has_cycle() or self.tail is None:
            return False
        if start < 0 or start >= self.size - 1:
            return False

        start_node = self.get_node(start)
        self.tail.next = start_node
        return True
