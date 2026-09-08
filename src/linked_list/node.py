from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    """Class for a single node in a linked list."""
    value: Any
    prev: Node | None = None
    next: Node | None = None

    def __repr__(self):
        return f"Node[{self.value}]"
