from collections import deque
from typing import Sequence


def merge_sort(seq: Sequence):
    """O(n * log(n))"""

    length = len(seq)
    if length > 1:
        floor_mid = length // 2

        lefty = merge_sort(seq[:floor_mid])
        righty = merge_sort(seq[floor_mid:])

        result = deque()
        while lefty and righty:
            if lefty[0] <= righty[0]:
                result.append(lefty.popleft())
            else:
                result.append(righty.popleft())
        result.extend(*lefty, *righty)
        return result

    elif length == 1:
        return deque((seq,))

    else:
        raise NotImplementedError
