from typing import List


def bubble_sort(seq: List):
    made_swaps = False
    for i, (n, m) in enumerate(zip(seq, seq[1:])):
        if n > m:
            temp = n
            seq[i] = m
            seq[i+1] = temp
            made_swaps = True
    if made_swaps:
        return bubble_sort(seq)
    return seq
