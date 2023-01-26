import sys
from collections import deque, defaultdict
from typing import Sequence
import time
from pathlib import Path

import pandas as pd

comparison_count: int = 0
swap_count: int = 0

# sys.setrecursionlimit(10**6)


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
    "merge": merge_sort,
    "quick": quicksort,
}
HEADERS = ["n", "data_type", "algo", "cmp", "swap", "time"]


algo_to_data = defaultdict(list)
for file_path in (Path(__file__).parent / "inputs").iterdir():
    split_name = file_path.name.split("_")
    data_size = int(split_name.pop(-1))
    data_type = "_".join(split_name)

    with open(file_path, "r") as in_file:
        int_sequence = [int(line.strip()) for line in in_file.readlines()]

    for name, algo in SORTER_NAME_TO_FUNCTION.items():
        if data_type == "nearly_sorted" and data_size >= 10000 and name == "quick":
            continue

        t = time.time_ns()
        result = algo(int_sequence)
        time_used = (time.time_ns() - t) / 1000

        algo_to_data[name].append((
            data_size, data_type, name, comparison_count, swap_count, time_used
        ))

        comparison_count = 0
        swap_count = 0

df = pd.concat([pd.DataFrame(data, columns=HEADERS) for data in algo_to_data.values()], axis=0)
df.to_csv("result.csv", index=False)
