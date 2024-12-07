from typing import List, Tuple

from . import read_input

EXAMPLE = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def parse_row(input_row: str) -> Tuple[int, List[int]]:
    answer_split = input_row.split(":")
    return (int(answer_split[0]), [int(item) for item in answer_split[1].split()])


def parse_input(input_block: str) -> List[Tuple[int, List[int]]]:
    return [parse_row(row) for row in input_block.splitlines()]


def concat_ints(left_int: int, right_int: int) -> int:
    return int(str(left_int) + str(right_int))


def try_operations(answer: int, input_nums: List[int], concat: bool = False) -> int:
    possible_values = [input_nums[0]]
    for item in input_nums[1:]:
        possible_values = (
            [old_val + item for old_val in possible_values]
            + [old_val * item for old_val in possible_values]
            + [concat_ints(old_val, item) for old_val in possible_values if concat]
        )
    return answer if answer in possible_values else 0


def count_winning_rows(input_block: str, concat: bool = False) -> int:
    cnt = 0
    for row in parse_input(input_block):
        cnt += try_operations(*row, concat)
    return cnt


assert count_winning_rows(EXAMPLE) == 3749
assert count_winning_rows(EXAMPLE, True) == 11387

print(count_winning_rows(read_input("07")))
print(count_winning_rows(read_input("07"), True))
