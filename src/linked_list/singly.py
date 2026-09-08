from typing import Any, Optional

from linked_list.node import Node
from linked_list.base import BaseLinkedList, _MISSING

class SinglyLinkedList(BaseLinkedList):
    def __init__(
        self,
        initial_node_value: Any = _MISSING,
        value_type: type | None = None,
    ):
        super().__init__(initial_node_value, value_type=value_type)


    def append(self, value: Any) -> bool:
        """
        Adds a new node to the end of the linked list.
        Time complexity: O(1)
        """

        if not self._accepts_value(value) or self.has_cycle():
            return False

        new_node = Node(value)
        if self.head:
            self.tail.next = new_node
        else:
            self.head = new_node
        self.tail = new_node
        self.size += 1
        return True


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


    def prepend(self, value: Any) -> bool:
        """
        Adds a new node to the front of the linked list.
        Time complexity: O(1)
        """

        if not self._accepts_value(value) or self.has_cycle():
            return False

        new_node = Node(value)
        new_node.next = self.head
        if self.head is None:
            self.tail = new_node
        self.head = new_node
        self.size += 1
        return True


    def prepend_values(self, values: list[Any]) -> int:
        """
        Adding multiple nodes to the front of the linked list.
        Preserves order
        Time complexity: O(n)
        """

        prepended_count = 0
        for value in values[::-1]:
            if self.prepend(value):
                prepended_count += 1

        return prepended_count


    def insert(self, index: int, value: Any) -> bool:
        """
        Inserts a new node at the specified index.
        Time complexity: O(n)
        """

        if not self._accepts_value(value) or self.has_cycle():
            return False

        if index <= 0:
            return self.prepend(value)
        if index >= self.size:
            return self.append(value)

        new_node = Node(value)
        current_node = self.get_node(index - 1)
        new_node.next = current_node.next
        current_node.next = new_node
        self.size += 1
        return True


    def replace(self, index: int, value: Any) -> bool:
        """
        Replaces the value of a node at the specified index.
        Time complexity: O(n)
        """

        if index < 0 or index >= self.size or not self._accepts_value(value):
            return False

        current_node = self.get_node(index)
        if current_node is None:
            return False

        current_node.value = value
        return True


    def contains(self, value: Any) -> bool:
        """
        Checks if the list contains a node with the specified value.
        Time complexity: O(n)
        """

        current_node = self.head
        while current_node:
            if current_node.value == value: return True
            current_node = current_node.next

        return False


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

        if self.tail is None or self.has_cycle():
            return None
        if self.size == 1:
            return self.pop_head()

        previous_node = self.get_node(self.size - 2)
        popped_node = self.tail
        previous_node.next = None
        self.tail = previous_node
        self.size -= 1

        return popped_node


    def remove(self, index: int) -> bool:
        """
        Removes a node at the specified index.
        Time complexity: O(n)
        """

        if index < 0 or index >= self.size: return False
        if index == 0:
            return self.pop_head() is not None
        elif index >= self.size - 1:
            return self.pop_tail() is not None
        else:
            current_node = self.get_node(index - 1)
            current_node.next = current_node.next.next
            self.size -= 1

        return True


    def has_cycle(self) -> bool:
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


    def get_cycle_start_index(self, method:int = 1) -> Optional[int]:
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


    def reverse(self):
        """
        Reverses the linked list in place.
        Time complexity: O(n)
        """
        if self.size <= 1: return False

        current_node = self.head
        prev_node = None
        while current_node:
            next_node = current_node.next
            current_node.next = prev_node
            prev_node = current_node
            current_node = next_node
        self.head, self.tail = self.tail, self.head

        return True
