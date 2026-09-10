from abc import ABC, abstractmethod
from linked_list.node import Node
from typing import Any, Callable, Optional, Self
from linked_list.exceptions import CycleDetectedException, ValueTypeException

_MISSING = object()

class BaseLinkedList(ABC):
    def __init__(
        self,
        initial_node_value: Any = _MISSING,
        value_type: type | None = None,
        sort_key: Callable[[Any], Any] | None = None,
        sortable: bool = False,
    ):
        if value_type is not None and not self._is_valid_value_type(value_type):
            raise TypeError("value_type must be a type.")
        if sort_key is not None and not callable(sort_key):
            raise TypeError("sort_key must be callable.")
        if sortable and value_type is None and sort_key is None:
            raise TypeError("sortable lists require value_type or sort_key.")

        self.value_type = value_type
        self.sort_key = sort_key
        self.sortable = sortable
        self.head: Node | None = (
            Node(initial_node_value) if initial_node_value is not _MISSING else None
        )
        self.tail: Node | None = self.head
        self.size: int = 0 if initial_node_value is _MISSING else 1

        if self.head and not self._accepts_value(self.head.value):
            raise ValueTypeException(self.head.value, self.value_type)
        if self.head:
            self._validate_sortable_value(self.head.value)


    def _is_valid_value_type(self, value_type: type) -> bool:
        return isinstance(value_type, type)


    def _accepts_value(self, value: Any) -> bool:
        if self.value_type is None:
            return True

        return type(value) is self.value_type


    def _validate_value(self, value: Any) -> None:
        if not self._accepts_value(value):
            raise ValueTypeException(value, self.value_type)
        self._validate_sortable_value(value)


    def _sort_value(self, value: Any) -> Any:
        if self.sort_key is None:
            return value

        return self.sort_key(value)


    def _validate_sortable_value(self, value: Any) -> None:
        if not self.sortable:
            return

        try:
            sort_value = self._sort_value(value)
            sort_value <= sort_value
        except TypeError:
            raise TypeError("Linked list value is not sortable.")


    def _ensure_acyclic(self, operation: str) -> None:
        if self._has_cycle():
            raise CycleDetectedException(operation)


    def _value_type_name(self) -> str:
        if self.value_type is None:
            return "Any"

        return self.value_type.__name__


    def __len__(self):
        return self.size


    def __iter__(self):
        current_node = self.head
        for _ in range(self.size):
            if current_node is None:
                return
            yield current_node.value
            current_node = current_node.next


    def __repr__(self):
        values = []
        current_node = self.head
        for _ in range(min(self.size, 20)):
            if current_node is None:
                break
            values.append(current_node.value)
            current_node = current_node.next
        if self.size > 20:
            values.append("...")

        type_label = (
            f", value_type={self._value_type_name()}"
            if self.value_type is not None
            else ""
        )
        sort_label = ", sortable=True" if self.sortable else ""
        return (
            f"{type(self).__name__}(size={self.size}, "
            f"values={values!r}{type_label}{sort_label})"
        )


    def get_node(self, index: int) -> Node:
        """
        Returns node at index.
        Raises IndexError if index is out of bounds.
        Time complexity: O(n)
        """

        if index < 0 or index >= self.size:
            raise IndexError("Linked list index out of range.")
        if index == 0:
            return self.head
        if index == self.size - 1:
            return self.tail

        current_node = self.head
        for _ in range(index):
            current_node = current_node.next

        return current_node


    def get_node_address(self, index: int) -> int:
        return id(self.get_node(index))


    @classmethod
    def from_values(
        cls,
        values: list[Any],
        value_type: type | None = None,
        sort_key: Callable[[Any], Any] | None = None,
        sortable: bool = False,
    ) -> Self:
        linked_list = cls(
            value_type=value_type,
            sort_key=sort_key,
            sortable=sortable,
        )
        linked_list.append_values(values)
        return linked_list


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


    def to_list(self, count: Optional[int] = None) -> list[Any]:
        """
        Returns a list of node values.
        Time complexity: O(n)
        """

        return self.get_values(count)


    def to_nodes(self, count: Optional[int] = None) -> list[Node]:
        """
        Returns a list of nodes.
        Time complexity: O(n)
        """

        if count is None:
            count = self.size
        if count <= 0:
            return []

        nodes = []
        current_node = self.head
        for _ in range(min(count, self.size)):
            if current_node is None:
                break
            nodes.append(current_node)
            current_node = current_node.next

        return nodes


    def _values_are_sortable(self) -> bool:
        values = self.get_values()
        try:
            sorted(values, key=self._sort_value)
        except TypeError:
            raise TypeError("Linked list values are not sortable.")

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
    def append(self, value: Any) -> bool:
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
        for value in values:
            self._validate_value(value)

        appended_count = 0
        for value in values:
            if self.append(value):
                appended_count += 1

        return appended_count


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
        if self.head is None:
            self.tail = None
        popped_node.next = None
        self.size -= 1

        return popped_node


    def pop_tail(self) -> Node:
        """
        Removes and returns the tail node.
        Time complexity: O(n)
        """

        self._ensure_acyclic("pop_tail")
        if self.tail is None:
            raise IndexError("Cannot pop from an empty linked list.")
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


    def is_circular(self) -> bool:
        """
        Returns True when the tail links directly back to the head.
        Time complexity: O(1)
        """

        return self.head is not None and self.tail is not None and self.tail.next is self.head


    def make_linear(self) -> bool:
        """
        Breaks a tail-originating cycle and restores the list to linear form.
        Time complexity: O(1)
        """

        if not self._has_cycle():
            return False

        self.tail.next = None
        return True


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
            raise IndexError("Cannot create a cycle in an empty linked list.")
        if start < 0 or start >= self.size - 1:
            raise IndexError("Cycle start index out of range.")

        start_node = self.get_node(start)
        self.tail.next = start_node
        return True
