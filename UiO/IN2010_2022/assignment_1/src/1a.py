from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Optional


logger = getLogger(__name__)


@dataclass
class Node:
    value: int | None = None

    left: "Node | None" = None
    right: "Node | None" = None


@dataclass
class BinaryTree:
    root_node: Node
    size: int = 0

    out_path: Optional[Path] = None

    @staticmethod
    def _validate_input_value(value: int):
        if not isinstance(value, int):
            msg = f"value is not int, but {type(value)}"
            raise ValueError(msg)
        if not 1 <= value <= 10 ** 9:
            logger.error(
                f"value must be 1 <= value <= 10 ** 9, but is {value}; however, I choose to head your call!"
            )

    @staticmethod
    def _find_min(node: Node):
        current_node = node
        while current_node.left:
            current_node = current_node.left
        return current_node.value

    def _remove_value_from_node(self, node: Node, value_to_remove: int) -> Node:
        self._validate_input_value(value_to_remove)

        if value_to_remove < node.value:
            node.left = self._remove_value_from_node(node.left, value_to_remove)
            return node

        if value_to_remove > node.value:
            node.right = self._remove_value_from_node(node.right, value_to_remove)
            return node

        if node.left is None:
            return node.right

        if node.right is None:
            return node.left

        smallest_element = self._find_min(node.right)
        node.value = smallest_element
        node.right = self._remove_value_from_node(node.right, smallest_element)
        return node

    def contains(self, value_to_be_found: int) -> bool:
        self._validate_input_value(value_to_be_found)

        current_node = self.root_node
        while True:
            try:
                if current_node.value == value_to_be_found:
                    return True
            except AttributeError:
                # When value is None, this only happens if a Node had its value removed
                return False

            try:
                current_node = current_node.left if current_node.value < value_to_be_found else current_node.right
            except TypeError:
                # When value is None
                return False

    def insert(self, value_to_insert: int) -> None:
        self._validate_input_value(value_to_insert)

        if not self.root_node.value:
            self.root_node.value = value_to_insert
            self.size += 1
            return

        current_node = self.root_node
        while True:
            if current_node.value == value_to_insert:
                return

            if current_node.value < value_to_insert:
                if current_node.left:
                    current_node = current_node.left
                else:
                    current_node.left = Node(value=value_to_insert)
                    break
            else:  # current_node.value > value_to_insert
                if current_node.right:
                    current_node = current_node.right
                else:
                    current_node.right = Node(value=value_to_insert)
                    break

        self.size += 1

    def remove(self, value_to_remove: int) -> None:
        self.root_node = self._remove_value_from_node(self.root_node, value_to_remove)
        self.size -= 1


if __name__ == "__main__":
    import sys

    bt = BinaryTree(root_node=Node())
    for line in sys.stdin.readlines()[1:]:
        split_line = line.strip().split(" ")
        pseudo_value_command = split_line.pop()
        if pseudo_value_command.isdigit():
            value = int(pseudo_value_command)
            match split_line.pop():
                case "insert":
                    bt.insert(value)
                case "contains":
                    print(bt.contains(value))
                case "remove":
                    bt.remove(value)
                case _:
                    raise NotImplemented
            assert not split_line, "no more than two items per line!"
        else:
            print(bt.size)
