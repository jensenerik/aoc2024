from typing import Dict, List, Tuple

from . import read_input

EXAMPLE = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


def parse_input(input_block: str) -> Dict[Tuple[int, int], int]:
    return {(i, j): int(val) for i, row in enumerate(input_block.splitlines()) for j, val in enumerate(row)}


def find_starts(trail_map: Dict[Tuple[int, int], int]) -> List[Tuple[int, int]]:
    return [k for k in trail_map if trail_map[k] == 0]


def neighbors(loc: Tuple[int, int], height: int, width: int) -> List[Tuple[int, int]]:
    neigh = []
    for shift in [-1, 1]:
        for coord in [0, 1]:
            neigh.append((loc[0] + ((coord + 1) % 2) * shift, loc[1] + coord * shift))
    return [n for n in neigh if n[0] in range(height) and n[1] in range(width)]


def trace_trails(trail_map: Dict[Tuple[int, int], int], start: Tuple[int, int]) -> Tuple[int, int]:
    max_height = max(k[1] for k in trail_map.keys()) + 1
    max_width = max(k[0] for k in trail_map.keys()) + 1
    current_elev = 0
    current_locs = [start]
    while current_elev < 9:
        current_elev += 1
        new_locs = []
        for loc in current_locs:
            new_locs.extend([loc for loc in neighbors(loc, max_height, max_width) if trail_map[loc] == current_elev])
        current_locs = new_locs
    return len(set(current_locs)), len(current_locs)


def trail_count(input_block: str) -> Tuple[int, int]:
    trail_map = parse_input(input_block)
    total_endpoints = 0
    total_trails = 0
    for start in find_starts(trail_map):
        new_ends, new_trails = trace_trails(trail_map, start)
        total_endpoints += new_ends
        total_trails += new_trails
    return total_endpoints, total_trails


assert trail_count(EXAMPLE) == (36, 81)
daily_input = read_input("10")
print(trail_count(daily_input))
