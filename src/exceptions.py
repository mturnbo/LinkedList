from typing import Any

class EmptyValueException(ValueError):
    """Raised when an empty value is passed to a linked list operation."""
    def __init__(self, value: Any, msg="Cannot perform operation with empty value."):
        self.value = value
        self.message = msg
        super().__init__(self.message)


class ValueTypeException(TypeError):
    """Raised when value type passed to a linked list does not match its configured value type."""
    def __init__(self, value: Any, expected_type: type | None = None):
        self.value = value
        self.expected_type = expected_type
        expected = expected_type.__name__ if expected_type else "configured value type"
        self.message = f"Invalid value type: {type(self.value).__name__}. Expected {expected}."
        super().__init__(self.message)


class CycleDetectedException(RuntimeError):
    """Raised when a linked list contains a cycle and an operation that would break the cycle is attempted."""
    def __init__(self, operation: Any, msg="Cannot perform operation on linked list with cycle."):
        self.operation = operation
        self.message = f"Invalid operation: {self.operation}. {msg}"
        super().__init__(self.message)
