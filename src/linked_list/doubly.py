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


    def get_node(self, index: int) -> Node:
        """
        Retrieves a node at the specified index.
        Raises IndexError if index is out of bounds.
        Time complexity: O(n)
        """

        if index < 0 or index >= self.size:
            raise IndexError("Linked list index out of range.")
        if index == 0:
            return self.head
        if index == self.size - 1:
            return self.tail

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

        self._validate_value(value)
        self._ensure_acyclic("append")

        new_node = Node(value)
        if self.head:
            self.tail.next = new_node
            new_node.prev = self.tail
        else:
            self.head = new_node
        self.tail = new_node
        self.size += 1
        return True


    def prepend(self, value: Any) -> bool:
        """
        Adds a new node to the front of the linked list.
        Time complexity: O(1)
        """

        self._validate_value(value)
        self._ensure_acyclic("prepend")

        new_node = Node(value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        self.size += 1
        return True


    def prepend_values(self, values: list[Any]) -> int:
        """
        Adding multiple nodes to the front of the linked list.
        Preserves order.
        Time complexity: O(n)
        """

        for value in values:
            self._validate_value(value)

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

        self._validate_value(value)
        self._ensure_acyclic("insert")

        if index <= 0:
            return self.prepend(value)
        if index >= self.size:
            return self.append(value)

        previous_node = self.get_node(index - 1)
        next_node = previous_node.next
        new_node = Node(value, prev=previous_node, next=next_node)
        previous_node.next = new_node
        next_node.prev = new_node
        self.size += 1
        return True


    def replace(self, index: int, value: Any) -> bool:
        """
        Replaces the value of a node at the specified index.
        Time complexity: O(n)
        """

        self._validate_value(value)
        if index < 0 or index >= self.size:
            raise IndexError("Linked list index out of range.")

        current_node = self.get_node(index)

        current_node.value = value
        return True


    def pop_head(self) -> Node:
        """
        Removes and returns the head node.
        Time complexity: O(1)
        """

        self._ensure_acyclic("pop_head")
        if self.head is None:
            raise IndexError("Cannot pop from an empty linked list.")

        popped_node = self.head
        self.head = popped_node.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        popped_node.next = None
        popped_node.prev = None
        self.size -= 1

        return popped_node


    def pop_tail(self) -> Node:
        """
        Removes and returns the tail node.
        Time complexity: O(1)
        """

        self._ensure_acyclic("pop_tail")
        if self.tail is None:
            raise IndexError("Cannot pop from an empty linked list.")
        if self.size == 1:
            return self.pop_head()

        popped_node = self.tail
        self.tail = popped_node.prev
        self.tail.next = None
        popped_node.prev = None
        popped_node.next = None
        self.size -= 1

        return popped_node


    def remove(self, index: int) -> bool:
        """
        Removes the node at the specified index.
        Time complexity: O(n)
        """
        self._ensure_acyclic("remove")
        if index < 0 or index >= self.size:
            raise IndexError("Linked list index out of range.")
        if index == 0:
            self.pop_head()
            return True
        elif index >= self.size - 1:
            self.pop_tail()
            return True
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


    def create_cycle(self, start: int) -> bool:
        """
        Creates a circular doubly linked list by linking the tail to the head.
        Time complexity: O(1)
        """

        if start != 0:
            raise IndexError("Circular doubly linked lists must start at index 0.")
        if self.head is None or self.tail is None:
            raise IndexError("Cannot create a cycle in an empty linked list.")
        self._ensure_acyclic("create_cycle")

        self.tail.next = self.head
        self.head.prev = self.tail
        return True


    def is_circular(self) -> bool:
        """
        Returns True when the tail links to the head and the head links to the tail.
        Time complexity: O(1)
        """

        return (
            self.head is not None
            and self.tail is not None
            and self.tail.next is self.head
            and self.head.prev is self.tail
        )


    def make_linear(self) -> bool:
        """
        Breaks a circular doubly linked list and restores linear endpoints.
        Time complexity: O(1)
        """

        if not self.is_circular():
            return False

        self.tail.next = None
        self.head.prev = None
        return True


    def reverse(self):
        """
        Reverses the order of nodes in the list.
        Time complexity: O(n)
        """

        self._ensure_acyclic("reverse")
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

        if method not in (1, 2):
            raise ValueError("Method must be 1 (merge) or 2 (insertion).")
        self._ensure_acyclic("sort")
        if self.size <= 1:
            return True
        self._values_are_sortable()

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
