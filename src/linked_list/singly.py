import sys
from linked_list.node import Node
from linked_list.base import BaseLinkedList
from exceptions import *

class SinglyLinkedList(BaseLinkedList):
    def __init__(self):
        super().__init__()

    def append(self, value: Any):
        """
        Adds a new node to the end of the linked list.
        Time complexity: O(1)
        """

        try:
            if not value:
                raise EmptyValueException(value)

            if self.has_cycle():
                raise CycleDetectedException(sys._getframe().f_code.co_name)

            new_node = Node(value)
            if self.head:
                self.tail.next = new_node
            else:
                self.head = new_node
            self.tail = new_node
            self.size += 1
            return True
        except EmptyValueException as e:
            print(e)
        except ValueTypeException as e:
            print(e)
        except CycleDetectedException as e:
            print(e)

        return False


    def append_values(self, values: list[Any]) -> int:
        """
        Adds multiple new nodes to the end of the linked list.
        Time complexity: O(n)
        """
        for value in values:
            self.append(value)

        return len(values)


    def prepend(self, value: Any):
        """
        Adds a new node to the front of the linked list.
        Time complexity: O(1)
        """
        try:
            if not value:
                raise EmptyValueException(value)

            new_node = Node(value)
            new_node.next = self.head
            self.head = new_node
            self.size += 1
            return True
        except EmptyValueException as e:
            print(e)
        except ValueTypeException as e:
            print(e)

        return False


    def prepend_values(self, values: list[Any]) -> int:
        """
        Adding multiple nodes to the front of the linked list.
        Preserves order
        Time complexity: O(n)
        """

        for value in values[::-1]:
            self.prepend(value)

        return len(values)


    def insert(self, index: int, value: Any):
        """
        Inserts a new node at the specified index.
        Time complexity: O(n)
        """

        try:
            if self.has_cycle():
                raise CycleDetectedException(sys._getframe().f_code.co_name)

            if index == 0:
                self.prepend(value)
            elif index >= self.size:
                self.append(value)
            else:
                new_node = Node(value)
                current_node = self.get_node(index -1)
                new_node.next = current_node.next
                current_node.next = new_node
                self.size += 1
                return True
        except ValueTypeException as e:
            print(e)
        except CycleDetectedException as e:
            print(e)

        return False


    def replace(self, index: int, value: Any) -> bool:
        """
        Replaces the value of a node at the specified index.
        Time complexity: O(n)
        """

        try:
            current_node = self.get_node(index)
            current_node.value = value
            return True
        except Exception as e:
            print(e)

        return False


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


    def remove(self, index: int):
        """
        Removes a node at the specified index.
        Time complexity: O(n)
        """

        if index < 0 or index >= self.size: return False
        if index == 0:
            self.head = self.head.next
            self.size -= 1
        elif index >= self.size - 1:
            self.trim()
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
