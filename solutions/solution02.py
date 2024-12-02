from copy import deepcopy
from typing import List

from solutions import read_input

EXAMPLE = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def parse_input(input_block: str) -> List[List[int]]:
    return [[int(item) for item in row.split()] for row in input_block.splitlines()]


def check_safety(row: List[int]) -> bool:
    diffs = [row[i] - row[i + 1] for i in range(len(row) - 1)]
    abs_diffs = [abs(diff) for diff in diffs]
    return ((max(diffs) > 0) == (min(diffs) > 0)) and (max(abs_diffs) <= 3) and (min(abs_diffs) > 0)


def count_safe_rows(input_block: str) -> int:
    safe_rows = 0
    for row in parse_input(input_block):
        if check_safety(row):
            safe_rows += 1
    return safe_rows


def count_damp_rows(input_block: str) -> int:
    safe_rows = 0
    for row in parse_input(input_block):
        if check_safety(row):
            safe_rows += 1
        else:
            for i in range(len(row)):
                removed_row = deepcopy(row)
                del removed_row[i]
                if check_safety(removed_row):
                    safe_rows += 1
                    break
    return safe_rows


assert count_safe_rows(EXAMPLE) == 2
assert count_damp_rows(EXAMPLE) == 4

print(count_safe_rows(read_input("02")))
print(count_damp_rows(read_input("02")))
