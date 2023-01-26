from collections import deque
from typing import Sequence

comparison_count: int = 0
swap_count: int = 0


def insertion_sort(seq: Sequence):
    global comparison_count
    global swap_count

    for j in range(1, len(seq)):
        k = j
        while seq[k - 1] > seq[k] and k > 0:
            seq[k], seq[k - 1] = seq[k - 1], seq[k]
            swap_count += 1

            k -= 1

    return seq


def quicksort(seq: Sequence):
    global comparison_count
    global swap_count

    seq = list(seq)
    if not seq:
        return seq

    lower, higher = [], []

    pivot = seq.pop(-1)
    for value in seq:
        if value < pivot:
            lower.append(value)
        else:
            higher.append(value)

        comparison_count += 1

    sorted_lower = quicksort(lower)
    sorted_higher = quicksort(higher)

    return [*sorted_lower, pivot, *sorted_higher]


def bubble_sort(seq: Sequence):
    # O(n ** 2)

    global comparison_count
    global swap_count

    if not seq:
        return seq

    made_swaps = False
    for i, (n, m) in enumerate(zip(seq, seq[1:])):
        if n > m:
            comparison_count += 1

            seq[i], seq[i + 1] = m, n
            swap_count += 1

            made_swaps = True

    if made_swaps:
        return bubble_sort(seq)
    return seq


def merge_sort(seq: Sequence):
    # O(n * log(n))

    global comparison_count
    global swap_count

    length = len(seq)
    if length > 1:
        floor_mid = length // 2

        lefty = merge_sort(seq[:floor_mid])
        righty = merge_sort(seq[floor_mid:])

        merge_sorted = deque()
        while lefty and righty:
            if lefty[0] <= righty[0]:
                merge_sorted.append(lefty.popleft())
            else:
                merge_sorted.append(righty.popleft())
            comparison_count += 1

        merge_sorted.extend((*lefty, *righty))
        return merge_sorted

    elif length == 1 or length == 0:
        return deque(seq)

    else:
        raise NotImplementedError


SORTER_NAME_TO_FUNCTION = {
    "bubble": bubble_sort,
    "merge": merge_sort,
    "quick": quicksort,
    "insertion": insertion_sort
}


if __name__ == "__main__":
    import sys
    import time
    from copy import copy
    from pathlib import Path

    file_path = None
    try:
        file_path = sys.argv[1]
    except IndexError:
        print("No input provided, using my own input!")
        file_path = "test_input.dat"
    finally:
        file_path = Path(file_path)

    with open(file_path, "r") as in_file:
        int_sequence = [int(line.strip()) for line in in_file.readlines()]

    # Part 1
    for name, algo in SORTER_NAME_TO_FUNCTION.items():
        result = algo(copy(int_sequence))
        # print(f"{name}({int_sequence}) = {result}")
        with open(f"{file_path.stem}_{name}.out", "w") as out_file:
            for v in result:
                out_file.write(f"{v}\n")

    # Part 2
    with open(f"{file_path.stem}.csv", "w") as out_file:
        algo_headers = ", ".join(f"{name}_cmp, {name}_swaps, {name}_time" for name in SORTER_NAME_TO_FUNCTION)
        out_file.write(f"n, {algo_headers}\n")

        for i in range(len(int_sequence)):
            csv_row = [str(i)]
            for name, algo in SORTER_NAME_TO_FUNCTION.items():
                t = time.time_ns()
                result = algo(int_sequence[:i])
                time_used = (time.time_ns() - t) / 1000

                csv_row.append(f"{comparison_count}, {swap_count}, {time_used}")

                comparison_count = 0
                swap_count = 0

            str_csv_row = ", ".join(csv_row)
            out_file.write(f"{str_csv_row}\n")
