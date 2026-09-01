"""
Lab 2: The Complexity Profiler -- starter.

Complete the three functions below. See the assignment,
Part B, for the full requirements. Do not use sorted(), list.sort(), or
the `in` operator inside these implementations -- hand-roll the logic.
"""

from typing import List


def linear_search(data: List[int], target: int) -> int:
    """
    Return the index of `target` in `data`, or -1 if absent.

    Time complexity: TODO -- state best/average/worst case here.
    """
    for i, value in enumerate(data):
        if value == target:
            return i
    return -1


def binary_search(data: List[int], target: int) -> int:
    """
    Return the index of `target` in a SORTED `data`, or -1 if absent.
    Must be iterative, not recursive.

    Time complexity: TODO -- state best/average/worst case here.
    """
    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == target:
            return mid
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def bubble_sort(data: List[int]) -> List[int]:
    """
    Return a new list containing `data`'s elements in ascending order.
    Must not mutate the input list.

    Time complexity: TODO -- state best/average/worst case here.
    """
    sorted_data = data[:]
    n = len(sorted_data)
    for i in range(n):
        for j in range(0, n-i-1):
            if sorted_data[j] > sorted_data[j+1]:
                sorted_data[j], sorted_data[j+1] = sorted_data[j+1], sorted_data[j]
    return sorted_data