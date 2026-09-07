from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Node:
    """Class for a single node in a linked list."""
    value: int | float | str | bool
    prev: Node | None = None
    next: Node | None = None

    def __repr__(self):
        return f"Node[{self.value}]"
