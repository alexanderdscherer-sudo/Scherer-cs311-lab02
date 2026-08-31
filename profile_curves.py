"""
Lab 2: The Complexity Profiler -- verification suite.

Run: python profile_curves.py
Requires matplotlib (`pip install matplotlib`) for curves.png.
Prints the Success Token only if every check below passes.
"""

import base64
import hashlib
import random
import statistics
import sys
import timeit
from math import log
from typing import Callable, List, Tuple

from algorithms import binary_search, bubble_sort, linear_search

ASSIGNMENT_ID = "LAB02"


def get_student_id() -> str:
    """Prompt for the student's USI username; baked into the Success Token
    so a copied/shared token decodes to someone else's name, not yours."""
    student_id = input("Enter your USI username (e.g. cwill): ").strip()
    while not student_id:
        student_id = input("Username cannot be blank. Enter your USI username: ").strip()
    return student_id


def generate_token(assignment_id: str, student_id: str) -> str:
    digest = hashlib.sha256(f"CS311-{assignment_id}-{student_id}-VERIFIED".encode()).hexdigest()[:16]
    raw = f"CS311|{assignment_id}|{student_id}|PASS|{digest}"
    return base64.b64encode(raw.encode()).decode()


def print_success_banner(assignment_id: str) -> None:
    student_id = get_student_id()
    token = generate_token(assignment_id, student_id)
    print("\n" + "=" * 60)
    print(f"  ALL CHECKS PASSED -- {assignment_id}")
    print(f"  STUDENT: {student_id}")
    print("  SUCCESS TOKEN (paste this into Blackboard):")
    print(f"  {token}")
    print("=" * 60 + "\n")


def check(label: str, condition: bool, failures: list) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}")
    if not condition:
        failures.append(label)


def verify_correctness(failures: list) -> None:
    data = [4, 1, 7, 3, 9, 2, 8, 5, 6, 0]
    sorted_data = sorted(data)

    check("linear_search finds present element", linear_search(data, 7) == data.index(7), failures)
    check("linear_search returns -1 for absent element", linear_search(data, 99) == -1, failures)
    check("binary_search finds present element", sorted_data[binary_search(sorted_data, 7)] == 7, failures)
    check("binary_search returns -1 for absent element", binary_search(sorted_data, 99) == -1, failures)

    sorted_by_student = bubble_sort(data)
    check("bubble_sort produces correctly sorted output", sorted_by_student == sorted_data, failures)
    check("bubble_sort does not mutate the input list", data != sorted_data, failures)


def estimate_growth_exponent(sizes: List[int], times: List[float]) -> float:
    """
    Estimate the empirical complexity exponent via log-log linear
    regression: slope of log(time) vs log(n). O(n) ~ 1.0, O(n^2) ~ 2.0,
    O(log n) / O(1) ~ near 0 (grows far slower than any positive power).
    """
    xs = [log(n) for n in sizes]
    ys = [log(t) for t in times]
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    denominator = sum((x - mean_x) ** 2 for x in xs)
    return numerator / denominator if denominator else 0.0


def time_calls(fn: Callable, sizes: List[int], make_args: Callable, repeats: int = 5) -> Tuple[List[int], List[float]]:
    per_call_times = []
    for n in sizes:
        samples = []
        for _ in range(repeats):
            args = make_args(n)
            elapsed = timeit.timeit(lambda: fn(*args), number=1)
            samples.append(max(elapsed, 1e-9))  # guard against a zero-time read
        per_call_times.append(statistics.median(samples))
    return sizes, per_call_times


def main() -> int:
    failures: list = []

    print("Verifying correctness on known inputs...\n")
    verify_correctness(failures)
    if failures:
        print(f"\n{len(failures)} correctness check(s) failed -- fix these before profiling. No token issued.")
        return 1

    print("\nProfiling growth curves (this takes a little while)...\n")

    search_sizes = [1000, 5000, 25000, 100000]

    def sorted_list_args(n: int):
        data = list(range(n))
        target = data[-1]  # worst case: present at the end / not found path exercised separately
        return (data, target)

    def unsorted_list_args(n: int):
        data = list(range(n))
        random.shuffle(data)
        target = -1  # guaranteed absent -> worst case for linear_search
        return (data, target)

    _, linear_times = time_calls(linear_search, search_sizes, unsorted_list_args)
    _, binary_times = time_calls(binary_search, search_sizes, sorted_list_args)

    sort_sizes = [200, 400, 800, 1600]

    def unsorted_for_sort(n: int):
        data = list(range(n))
        random.shuffle(data)
        return (data,)

    _, sort_times = time_calls(bubble_sort, sort_sizes, unsorted_for_sort, repeats=3)

    linear_exp = estimate_growth_exponent(search_sizes, linear_times)
    binary_exp = estimate_growth_exponent(search_sizes, binary_times)
    sort_exp = estimate_growth_exponent(sort_sizes, sort_times)

    print(f"  linear_search  empirical exponent: {linear_exp:.2f}  (expect ~1.0, O(n))")
    print(f"  binary_search  empirical exponent: {binary_exp:.2f}  (expect well under 1.0, O(log n))")
    print(f"  bubble_sort    empirical exponent: {sort_exp:.2f}  (expect ~2.0, O(n^2))\n")

    # Generous tolerances: real hardware/noise means exact exponents are
    # never observed. These bands only need to distinguish the complexity
    # CLASS, not pin down a precise constant.
    check("linear_search grows roughly linearly (0.6 <= exp <= 1.5)", 0.6 <= linear_exp <= 1.5, failures)
    check("binary_search grows far slower than linear (exp <= 0.6)", binary_exp <= 0.6, failures)
    check("bubble_sort grows roughly quadratically (exp >= 1.5)", sort_exp >= 1.5, failures)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.plot(search_sizes, linear_times, marker="o", label="linear_search")
        ax.plot(search_sizes, binary_times, marker="o", label="binary_search")
        ax.plot(sort_sizes, sort_times, marker="o", label="bubble_sort")
        ax.set_xlabel("input size (n)")
        ax.set_ylabel("time (s)")
        ax.set_title("Lab 2: Measured Growth Curves")
        ax.legend()
        fig.savefig("curves.png")
        print("Saved curves.png\n")
    except ImportError:
        print("matplotlib not installed -- skipping curves.png (run `pip install matplotlib`).")
        print("This does not block the Success Token, but your Part A write-up should still")
        print("reference the printed exponents above.\n")

    if failures:
        print(f"{len(failures)} check(s) failed. No token issued.")
        return 1

    print_success_banner(ASSIGNMENT_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
