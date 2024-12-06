from typing import Dict, Set, Tuple

from . import read_input

EXAMPLE = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


DIRECTION_LOOKUP = {"^": (-1, 0), ">": (0, 1), "<": (0, -1), "v": (1, 0)}


def parse_input(input_block: str) -> Dict[Tuple[int, int], str]:
    return {(i, j): v for i, row in enumerate(input_block.splitlines()) for j, v in enumerate(row)}


def find_guard(location_map: Dict[Tuple[int, int], str]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    for k, v in location_map.items():
        if v in DIRECTION_LOOKUP:
            return k, DIRECTION_LOOKUP[v]
    raise Exception("No guard found")


def trace_path(location_map: Dict[Tuple[int, int], str]) -> Set[Tuple[int, int]]:
    guard_loc, guard_dir = find_guard(location_map)
    guard_visits = set()
    guard_present = True
    while guard_present:
        guard_visits.add(guard_loc)
        next_loc = (guard_loc[0] + guard_dir[0], guard_loc[1] + guard_dir[1])
        next_action = location_map.get(next_loc)
        if next_action == "#":
            guard_dir = (guard_dir[1], -guard_dir[0])  # rotate 90 deg right
        elif next_action in [".", "^"]:
            guard_loc = next_loc
        else:
            guard_present = False
    return guard_visits


def loop_detect(location_map: Dict[Tuple[int, int], str]) -> bool:
    guard_loc, guard_dir = find_guard(location_map)
    guard_history = set()
    guard_loop = False
    while not guard_loop:
        if (guard_loc, guard_dir) in guard_history:
            guard_loop = True
        else:
            guard_history.add((guard_loc, guard_dir))
            next_loc = (guard_loc[0] + guard_dir[0], guard_loc[1] + guard_dir[1])
            next_action = location_map.get(next_loc)
            if next_action == "#":
                guard_dir = (guard_dir[1], -guard_dir[0])  # rotate 90 deg right
            elif next_action in [".", "^"]:
                guard_loc = next_loc
            else:
                return False
    return guard_loop


def check_all_loops(location_map: Dict[Tuple[int, int], str]) -> int:
    original_path = trace_path(location_map)
    original_path.remove(find_guard(location_map)[0])
    loop_cnt = 0
    for obstacle_loc in original_path:
        loop_cnt += loop_detect(location_map | {obstacle_loc: "#"})
    return loop_cnt


assert len(trace_path(parse_input(EXAMPLE))) == 41
assert not loop_detect(parse_input(EXAMPLE))
assert loop_detect(parse_input(EXAMPLE) | {(6, 3): "#"})
assert check_all_loops(parse_input(EXAMPLE)) == 6

daily_input = read_input("06")
print(len(trace_path(parse_input(daily_input))))
print(check_all_loops(parse_input(daily_input)))
