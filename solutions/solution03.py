from typing import List

from . import read_input

EXAMPLE = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
EXAMPLE_DO = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def parse_mul(command: str, do: bool = False) -> List[str]:
    starters = ["m", "d"] if do else ["m"]
    processed_commands = []
    working_command = ""
    expected = starters
    dont = False
    working_do_dont = False

    digits = [str(d) for d in range(10)]
    expected_map = {
        "m": ["u"],
        "u": ["l"],
        "l": ["("],
        "(": digits + [")"],
        ",": digits,
        ")": starters,
        "d": ["o"],
        "o": ["(", "n"],
        "n": ["'"],
        "'": ["t"],
        "t": ["("],
    } | {d: digits + [",", ")"] for d in digits}
    for char in command:
        if char in expected:
            working_command += char
            expected = expected_map[char]
            if char == ")":
                if not (dont or working_do_dont or (working_command == "mul()")):
                    processed_commands.append(working_command)
                elif working_command == "do()":
                    dont = False
                elif working_command == "don't()":
                    dont = True
                working_command = ""
            if char == "d":
                working_do_dont = True
            if char == "m":
                working_do_dont = False
        else:
            working_command = ""
            expected = starters
    return processed_commands


def multiply_command(command: str) -> int:
    nums = command.split(",")
    return int(nums[0][4:]) * int(nums[1][:-1])


def parse_and_agg(command: str, do: bool = False) -> int:
    return sum(multiply_command(com) for com in parse_mul(command, do))


assert len(parse_mul(EXAMPLE)) == 4
assert multiply_command("mul(11,8)") == 88
assert parse_and_agg(EXAMPLE) == 161

assert len(parse_mul(EXAMPLE_DO, True)) == 2
assert parse_and_agg(EXAMPLE_DO, True) == 48

print(parse_and_agg(read_input("03")))
print(parse_and_agg(read_input("03"), True))
