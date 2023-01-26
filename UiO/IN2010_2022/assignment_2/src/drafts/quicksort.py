from typing import Tuple, List


def quicksort(seq: List) -> Tuple:
    lower, higher = [], []

    pivot = seq.pop(-1)
    for v in seq:
        if v < pivot:
            lower.append(v)
        else:
            higher.append(v)

    sorted_lower = quicksort(lower)
    sorted_higher = quicksort(higher)

    return *sorted_lower, pivot, *sorted_higher
