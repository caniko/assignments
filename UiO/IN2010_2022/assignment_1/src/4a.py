from dataclasses import dataclass

@dataclass
class Node:
    value: int | None

    left: "Node | None" = None
    right: "Node | None" = None


def bst_sequence(node: Node) -> None:
    if not node:
        return
    
    print(node.value)
    bst_sequence(node.right)
    bst_sequence(node.left)


def sorted_list_to_bst(seq: list[int], start: int, end: int) -> Node:
    if start < end:
        return Node(
            value=seq[(mid := (start + end) // 2)],
            left=sorted_list_to_bst(seq, start, mid),
            right=sorted_list_to_bst(seq, mid + 1, end)
        )


if __name__ == "__main__":
    import sys

    stdin = [int(i) for i in sys.stdin.readlines()]
    bst_sequence(sorted_list_to_bst(stdin, 0, len(stdin)))
