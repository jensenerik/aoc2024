from collections import deque
from typing import Deque, Dict, Tuple

from . import read_input

EXAMPLE = """1
10
100
2024"""

CHANGE_EXAMPLE = """1
2
3
2024"""


def next_secret(x: int) -> int:
    prune_mod = 16777216
    x = ((x * 64) ^ x) % prune_mod
    x = ((x // 32) ^ x) % prune_mod
    x = ((x * 2048) ^ x) % prune_mod
    return x


def run_two_k(input_block: str) -> Tuple[int, int]:
    running_sum = 0
    all_scores: Dict[Tuple[int, ...], int] = {}
    for row in input_block.splitlines():
        x = int(row)
        last = None
        diffs: Deque[int] = deque([], 4)
        scores: Dict[Tuple[int, ...], int] = {}
        for _ in range(2000):
            x = next_secret(x)
            price = x % 10
            if last is not None:
                diffs.append(price - last)
            if len(diffs) == 4 and scores.get(tuple(diffs)) is None:
                scores[tuple(diffs)] = price
            last = price
        running_sum += x
        for k, v in scores.items():
            all_scores[k] = all_scores.get(k, 0) + v
    return running_sum, max(all_scores.values())


assert next_secret(123) == 15887950
assert run_two_k(EXAMPLE)[0] == 37327623
assert run_two_k(CHANGE_EXAMPLE)[1] == 23

daily_input = read_input("22")
print(run_two_k(daily_input))
