from dataclasses import dataclass


@dataclass
class Node:
    value: int | None = None

    next: "Node | None" = None
    previous: "Node | None" = None


@dataclass
class Teque:
    back: Node | None = None
    middle: Node | None = None
    front: Node | None = None

    size: int = 0

    def _check_and_move_middle_during_push(self) -> None:
        if self.size % 3 == 0:
            self.middle = self.middle.next

    def __repr__(self):
        return ", ".join([str(self.get(n)) for n in range(self.size)])

    def push_back(self, n: int) -> None:
        node_to_push = Node(value=n)
        if not self.back:
            self.back, self.middle = node_to_push, node_to_push
        elif not self.front:
            node_to_push.previous = self.back
            self.back.next = node_to_push
            self.front = node_to_push
        else:
            self.front.next = node_to_push
            node_to_push.previous = self.front
            self.front = node_to_push

            self._check_and_move_middle_during_push()

        self.size += 1
    
    def push_front(self, n: int) -> None:
        if not self.back:
            return self.push_back(n)
        node_to_push = Node(value=n)
        if not self.front:
            self.back.previous = node_to_push
            node_to_push.next = self.back

            self.front = self.back
            self.back = node_to_push
            self.middle = node_to_push
        else:
            self.back.previous = node_to_push
            node_to_push.next = self.back
            self.back = node_to_push

            self._check_and_move_middle_during_push()

        self.size += 1

    def push_middle(self, n: int) -> None:
        if not self.back or not self.front:
            return self.push_back(n)

        node_to_push = Node(value=n, previous=self.middle.previous or self.back, next=self.middle.next)
        self.middle.next = node_to_push
        self.middle = node_to_push

        self.size += 1

    def get(self, i: int) -> int | None:
        if not self.back or self.size == 0:
            return None
        if not self.front or i == 0:
            return self.back.value
        if i == self.size - 1:
            return self.front.value
        current_node = self.back
        for c in range(i):
            current_node = current_node.next
        return current_node.value


if __name__ == "__main__":
    import sys

    teque = Teque()
    for line in sys.stdin.readlines()[1:]:
        split_line = line.strip().split(" ")
        value = int(split_line.pop())
        match command := split_line.pop():
            case "push_back":
                teque.push_back(value)
            case "push_front":
                teque.push_front(value)
            case "push_middle":
                teque.push_middle(value)
            case "get":
                print(teque.get(value))
            case _:
                raise NotImplementedError(command)
        assert not split_line, "no more than two items per line!"
