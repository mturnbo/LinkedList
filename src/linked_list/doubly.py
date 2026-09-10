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

        if not self._accepts_value(value) or self._has_cycle():
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


    def reverse(self):
        """
        Reverses the order of nodes in the list.
        Time complexity: O(n)
        """

        current_node = self.head
        while current_node:
            current_node.prev, current_node.next = current_node.next, current_node.prev
            current_node = current_node.prev
        self.head, self.tail = self.tail, self.head
        return True


    def sort(self, method: int = 1) -> bool:
        """
        Sorts the linked list in place.
        method=1: Merge sort
        method=2: Insertion sort
        """

        if method not in (1, 2) or self._has_cycle():
            return False
        if self.size <= 1:
            return True
        if not self._values_are_sortable():
            return False

        if method == 1:
            def split(head: Node | None):
                if head is None or head.next is None:
                    return head, None
                slow = head
                fast = head
                prev = None
                while fast and fast.next:
                    prev = slow
                    slow = slow.next
                    fast = fast.next.next
                if prev:
                    prev.next = None
                if slow:
                    slow.prev = None
                return head, slow

            def merge(left: Node | None, right: Node | None):
                if left is None:
                    tail = right
                    while tail and tail.next:
                        tail = tail.next
                    return right, tail
                if right is None:
                    tail = left
                    while tail and tail.next:
                        tail = tail.next
                    return left, tail

                if left.value <= right.value:
                    head = left
                    left = left.next
                else:
                    head = right
                    right = right.next
                head.prev = None
                tail = head
                tail.next = None

                while left and right:
                    if left.value <= right.value:
                        tail.next = left
                        left.prev = tail
                        tail = left
                        left = left.next
                    else:
                        tail.next = right
                        right.prev = tail
                        tail = right
                        right = right.next
                    tail.next = None

                remainder = left if left else right
                if remainder:
                    remainder.prev = tail
                tail.next = remainder
                while tail.next:
                    tail = tail.next
                return head, tail

            def merge_sort(head: Node | None):
                if head is None or head.next is None:
                    return head, head
                left, right = split(head)
                left_head, left_tail = merge_sort(left)
                right_head, right_tail = merge_sort(right)
                return merge(left_head, right_head)

            head, tail = merge_sort(self.head)
            self.head = head
            self.tail = tail
            if self.head:
                self.head.prev = None
            if self.tail:
                self.tail.next = None
            return True

        if method == 2:
            sorted_head = None
            sorted_tail = None
            current = self.head
            while current:
                next_node = current.next
                current.prev = None
                current.next = None
                if sorted_head is None:
                    sorted_head = current
                    sorted_tail = current
                elif current.value <= sorted_head.value:
                    current.next = sorted_head
                    sorted_head.prev = current
                    sorted_head = current
                else:
                    search = sorted_head
                    while search.next and search.next.value <= current.value:
                        search = search.next
                    current.next = search.next
                    current.prev = search
                    if search.next:
                        search.next.prev = current
                    else:
                        sorted_tail = current
                    search.next = current
                current = next_node

            self.head = sorted_head
            self.tail = sorted_tail
            return True



