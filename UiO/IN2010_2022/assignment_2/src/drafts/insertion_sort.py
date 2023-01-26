from typing import Sequence


def insertion_sort(seq: Sequence):
    result = [seq[0]]

    for v in seq[1:]:
        result.append(v)
        for i in range(len(result) - 1, 1, -1):
            if result[i] > result[i - 1]:
                break
            temp = result[i]
            result[i] = result[i - 1]
            result[i - 1] = temp

    return result
