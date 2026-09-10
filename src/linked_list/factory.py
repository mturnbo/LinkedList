from typing import Any, Callable

from linked_list.base import _MISSING
from linked_list.doubly import DoublyLinkedList
from linked_list.singly import SinglyLinkedList


class LinkedList:
    """Factory for creating linked list instances."""

    @staticmethod
    def create(
        list_type: str = "singly",
        initial_node_value: Any = _MISSING,
        value_type: type | None = None,
        sort_key: Callable[[Any], Any] | None = None,
        sortable: bool = False,
    ) -> SinglyLinkedList | DoublyLinkedList:
        list_class = LinkedList._get_list_class(list_type)
        return list_class(
            initial_node_value,
            value_type=value_type,
            sort_key=sort_key,
            sortable=sortable,
        )


    @staticmethod
    def from_values(
        list_type: str,
        values: list[Any],
        value_type: type | None = None,
        sort_key: Callable[[Any], Any] | None = None,
        sortable: bool = False,
    ) -> SinglyLinkedList | DoublyLinkedList:
        list_class = LinkedList._get_list_class(list_type)
        return list_class.from_values(
            values,
            value_type=value_type,
            sort_key=sort_key,
            sortable=sortable,
        )


    @staticmethod
    def _get_list_class(list_type: str):
        match list_type.lower():
            case "s" | "single" | "singly":
                return SinglyLinkedList
            case "d" | "double" | "doubly":
                return DoublyLinkedList
            case _:
                raise ValueError(f"Unknown linked list type '{list_type}'.")
