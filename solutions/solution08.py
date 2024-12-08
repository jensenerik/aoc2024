from typing import Dict, List, Set, Tuple

from . import read_input

EXAMPLE = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


def calc_bounds(input_block: str) -> Tuple[int, int]:
    rows = input_block.splitlines()
    return len(rows), len(rows[0])


def find_antennas(input_block: str) -> Dict[str, List[Tuple[int, int]]]:
    symb_map: Dict[str, List[Tuple[int, int]]] = {}
    for i, row in enumerate(input_block.splitlines()):
        for j, symb in enumerate(row):
            if symb != ".":
                symb_map[symb] = symb_map.get(symb, []) + [(i, j)]
    return symb_map


def calc_antinode(
    antenna_1: Tuple[int, int], antenna_2: Tuple[int, int], resonance: int | None
) -> List[Tuple[int, int]]:
    resonance_nums = range(resonance) if resonance else [2]
    antinodes = []
    for res_num in resonance_nums:
        antinodes.append(
            (
                res_num * antenna_1[0] - (res_num - 1) * antenna_2[0],
                res_num * antenna_1[1] - (res_num - 1) * antenna_2[1],
            )
        )
    return antinodes


def calculate_antinodes(input_block: str, resonance: bool = False) -> int:
    height, width = calc_bounds(input_block)
    max_resonance = max(height, width)
    symb_map = find_antennas(input_block)
    antinode_locs: Set[Tuple[int, int]] = set()
    for antenna_locs in symb_map.values():
        for antenna_1 in antenna_locs:
            for antenna_2 in antenna_locs:
                if (antenna_1 != antenna_2) or resonance:
                    new_antinodes = calc_antinode(antenna_1, antenna_2, max_resonance if resonance else None)
                    antinode_locs.update(
                        [ant for ant in new_antinodes if (ant[0] in range(height)) and (ant[1] in range(width))]
                    )
    return len(antinode_locs)


assert calculate_antinodes(EXAMPLE) == 14
assert calculate_antinodes(EXAMPLE, True) == 34

daily_input = read_input("08")
print(calculate_antinodes(daily_input))
print(calculate_antinodes(daily_input, True))
