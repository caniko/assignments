import heapq


def heap_to_bst(seq: list[int]) -> None:
    if not seq:
        return

    left, right = [], []
    distance_to_node_value = len(seq) // 2
    for _ in range(distance_to_node_value):
        heapq.heappush(left, heapq.heappop(seq))

    print(heapq.heappop(seq))

    while seq:
        heapq.heappush(right, heapq.heappop(seq))

    heap_to_bst(right)
    heap_to_bst(left)


if __name__ == "__main__":
    import sys

    stdin = [int(i) for i in sys.stdin.readlines()]
    heapq.heapify(stdin)
    heap_to_bst(stdin)
