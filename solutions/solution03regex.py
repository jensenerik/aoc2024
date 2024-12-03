import re
from typing import Iterator, Match

from . import read_input

EXAMPLE = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
EXAMPLE_DO = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def find_everything(command: str) -> Iterator[Match]:
    return re.finditer(r"(do\(\)|don't\(\)|mul\(\d{1,3},\d{1,3}\))", command)


def multiply_command(command: str) -> int:
    nums = command.split(",")
    return int(nums[0][4:]) * int(nums[1][:-1])


def sum_em(command: str, do: bool) -> int:
    running_sum = 0
    dont = False
    for match in find_everything(command):
        if match.group(0) == "don't()":
            if do:
                dont = True
        elif match.group(0) == "do()":
            dont = False
        elif not dont:
            running_sum += multiply_command(match.group(0))
    return running_sum


assert sum_em(EXAMPLE, False) == 161
assert sum_em(EXAMPLE_DO, True) == 48

print(sum_em(read_input("03"), False))
print(sum_em(read_input("03"), True))
