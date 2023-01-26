from typing import Sequence


def climb_down_the_tree(current_value: int, branches: list[dict[int, set[int]]]) -> Sequence:
    path = [str(current_value)]
    while True:
        for parent_node, children in branches.items():
            if current_value in children:
                path.append(str(parent_node))
                current_value = parent_node
                break
        else:   # no break
            break
    return ", ".join(path)


if __name__ == "__main__":
    import sys
    from collections import deque

    stdin = deque(sys.stdin.readlines())

    kitten_node = int(stdin.popleft())

    branches = {}
    for line in stdin:
        if (line := line.strip()) == "-1":
            break

        split_line = [int(e) for e in line.split(" ")]
        branches[split_line[0]] = set(split_line[1:])

    print(climb_down_the_tree(kitten_node, branches))
