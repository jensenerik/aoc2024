from math import log10
from typing import Dict, Tuple

from . import read_input

EXAMPLE = "125 17"


def parse_input(input_block: str) -> Dict[int, int]:
    input_stones = [int(item) for item in input_block.split()]
    return {value: input_stones.count(value) for value in input_stones}


def split_stone(value: int) -> Tuple[int, int]:
    half_digits = (int(log10(value)) + 1) // 2
    return value // (10**half_digits), value % (10**half_digits)


def blink(stone_values: Dict[int, int]) -> Dict[int, int]:
    new_values: Dict[int, int] = {}
    for value, count in stone_values.items():
        if value == 0:
            new_values[1] = new_values.get(1, 0) + count
        elif int(log10(value)) % 2 == 1:
            for val in split_stone(value):
                new_values[val] = new_values.get(val, 0) + count
        else:
            new_values[value * 2024] = new_values.get(value * 2024, 0) + count
    return new_values


def blink_and_count(input_block: str, blinks: int) -> int:
    current_stones = parse_input(input_block)
    for _ in range(blinks):
        current_stones = blink(current_stones)
    return sum(current_stones.values())


assert split_stone(10) == (1, 0)
assert split_stone(99) == (9, 9)
assert split_stone(1000) == (10, 0)

assert blink_and_count(EXAMPLE, 25) == 55312

daily_input = read_input("11")
print(blink_and_count(daily_input, 25))
print(blink_and_count(daily_input, 75))
