from classes.node import Node

class LinkedList:
    """Class for a linked list."""

    def __init__(self):
        self.head = None
        self.tail = None

    def __repr__(self):
        return f"LinkedList[{self.head}]"
