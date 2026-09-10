# Linked List

A small Python package for creating singly and doubly linked lists.

The package supports arbitrary Python values by default, with optional value-type enforcement for homogeneous lists. It also includes sorting helpers, circular-list utilities, bounded iteration, and a factory for creating the list type you need.

## Requirements

- Python 3.12+

## Installation

The distribution package is named `mt-linked-list`. Import code from `linked_list`.

Install from a local checkout:

```bash
pip install /path/to/LinkedListModule
```

Install in editable mode while developing the package:

```bash
pip install -e /path/to/LinkedListModule
```

Or with `uv` from another project:

```bash
uv add /path/to/LinkedListModule
```

Install directly from GitHub:

```bash
pip install git+https://github.com/mturnbo/LinkedList.git
```

Or add the GitHub dependency with `uv`:

```bash
uv add git+https://github.com/mturnbo/LinkedList.git
```

## Basic Usage

Import the factory:

```python
from linked_list import LinkedList

linked_list = LinkedList.from_values("singly", [1, 2, 3])
linked_list.append(4)

print(linked_list.to_list())
# [1, 2, 3, 4]
```

Or import a concrete list class:

```python
from linked_list import DoublyLinkedList, SinglyLinkedList

singly = SinglyLinkedList.from_values(["a", "b", "c"])
doubly = DoublyLinkedList.from_values([1, 2, 3])
```

## Factory

Use `LinkedList.create()` for an empty list:

```python
from linked_list import LinkedList

singly = LinkedList.create("singly")
doubly = LinkedList.create("doubly")
```

Accepted list type names:

- Singly: `"s"`, `"single"`, `"singly"`
- Doubly: `"d"`, `"double"`, `"doubly"`

Create a list from values:

```python
linked_list = LinkedList.from_values("doubly", [3, 1, 2])
```

Factory methods pass through list configuration:

```python
linked_list = LinkedList.from_values(
    "singly",
    [3, 1, 2],
    value_type=int,
    sortable=True,
)
```

## Values And Types

Lists accept any value type by default:

```python
linked_list = SinglyLinkedList()
linked_list.append({"id": 1})
linked_list.append(None)
linked_list.append(False)
```

Use `value_type` to enforce one exact value type:

```python
linked_list = SinglyLinkedList(value_type=int)
linked_list.append(1)

linked_list.append("2")
# raises ValueTypeException
```

The type check is exact. For example, `False` is not accepted by `value_type=int`.

## Methods

Both `SinglyLinkedList` and `DoublyLinkedList` support:

- `append(value) -> bool`
- `append_values(values) -> int`
- `prepend(value) -> bool`
- `prepend_values(values) -> int`
- `insert(index, value) -> bool`
- `replace(index, value) -> bool`
- `remove(index) -> bool`
- `pop_head() -> Node`
- `pop_tail() -> Node`
- `contains(value) -> bool`
- `get_node(index) -> Node`
- `get_node_address(index) -> int`
- `get_values(count=None) -> list`
- `to_list(count=None) -> list`
- `to_nodes(count=None) -> list[Node]`
- `reverse() -> bool`
- `sort(method=1, reverse=False) -> bool`
- `create_cycle(start) -> bool`
- `get_cycle_start_index() -> int | None`
- `is_circular() -> bool`
- `make_linear() -> bool`
- `clear(iterate=False) -> bool`

Lists also support:

```python
len(linked_list)
list(linked_list)
repr(linked_list)
```

`to_list()` is an alias for `get_values()`.

## Nodes

`pop_head()`, `pop_tail()`, `get_node()`, and `to_nodes()` return `Node` objects.

```python
node = linked_list.pop_head()
print(node.value)
```

A node has:

- `value`
- `next`
- `prev`

The `prev` field is used by doubly linked lists.

## Sorting

Use `sort()` to sort values in place.

```python
linked_list = SinglyLinkedList.from_values([3, 1, 2])
linked_list.sort()

print(linked_list.to_list())
# [1, 2, 3]
```

Sorting methods:

- `method=1`: merge sort
- `method=2`: insertion sort

Sort descending:

```python
linked_list.sort(reverse=True)
```

Sort complex values with `sort_key`:

```python
tasks = SinglyLinkedList.from_values(
    [
        {"name": "low", "priority": 3},
        {"name": "high", "priority": 1},
    ],
    sort_key=lambda task: task["priority"],
)

tasks.sort()
```

Use `sortable=True` to validate sortable values as they enter the list:

```python
numbers = DoublyLinkedList(value_type=int, sortable=True)
numbers.append_values([3, 1, 2])
numbers.sort()
```

`sortable=True` requires either `value_type` or `sort_key`.

## Circular Lists

Singly linked lists can create a cycle from the tail to an earlier node:

```python
linked_list = SinglyLinkedList.from_values([1, 2, 3])
linked_list.create_cycle(1)

print(linked_list.get_cycle_start_index())
# 1
```

Doubly linked lists support circular lists where the tail points to the head and the head points back to the tail:

```python
linked_list = DoublyLinkedList.from_values([1, 2, 3])
linked_list.create_cycle(0)

print(linked_list.is_circular())
# True
```

Use `make_linear()` to break a cycle:

```python
linked_list.make_linear()
```

Iteration and `repr()` are bounded by list size, so they are safe for circular lists.

## Exceptions

Invalid operations raise exceptions:

- `IndexError`: invalid index, empty pop, or invalid cycle start
- `ValueTypeException`: value does not match the configured `value_type`
- `CycleDetectedException`: mutation cannot run while the list has a cycle
- `ValueError`: invalid sort method or unknown factory list type
- `TypeError`: invalid configuration or unsortable values

Example:

```python
from linked_list import SinglyLinkedList, ValueTypeException

linked_list = SinglyLinkedList(value_type=int)

try:
    linked_list.append("not an int")
except ValueTypeException:
    print("Wrong value type")
```

## Development

Run the test suite:

```bash
uv run pytest -q
```
