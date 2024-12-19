from typing import Dict, List, Set, Tuple

from . import read_input

EXAMPLE = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


def parse_input(input_block: str) -> Tuple[Set[str], List[str]]:
    patterns, designs = input_block.split("\n\n")
    return (set(patterns.split(", ")), designs.splitlines())


def check_design(patterns: Set[str], design: str) -> bool:
    possible = False
    if len(design) == 0:
        return True
    for pattern in patterns:
        if pattern == design[: len(pattern)]:
            possible = possible or check_design(patterns, design[len(pattern) :])
    return possible


def obtainable_designs(input_block: str) -> int:
    patterns, designs = parse_input(input_block)
    return sum([check_design(patterns, design) for design in designs])


def count_designs(input_block: str) -> int:
    patterns, designs = parse_input(input_block)
    lookup: Dict[str, int] = {}

    def count_single(patterns: Set[str], design: str) -> int:
        possible = 0
        if len(design) == 0:
            return 1
        if design in lookup:
            return lookup.get(design, 0)
        for pattern in patterns:
            if pattern == design[: len(pattern)]:
                possible += count_single(patterns, design[len(pattern) :])
        lookup[design] = possible
        return possible

    return sum([count_single(patterns, design) for design in designs])


assert obtainable_designs(EXAMPLE) == 6
assert count_designs(EXAMPLE) == 16
daily_input = read_input("19")
print(obtainable_designs(daily_input))
print(count_designs(daily_input))
