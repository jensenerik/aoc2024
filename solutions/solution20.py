from typing import Dict, Tuple

from . import read_input, v_add

EXAMPLE = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


class RaceMap:
    def __init__(self, input_block: str):
        race_map: Dict[Tuple[int, int], str] = {}
        for i, row in enumerate(input_block.splitlines()):
            for j, char in enumerate(row):
                if char == "S":
                    self.start = (i, j)
                elif char == "E":
                    self.end = (i, j)
                race_map[(i, j)] = char
        self.race_map = race_map

    def breadth_first(
        self, race_map: Dict[Tuple[int, int], str] | None = None, key_stone: Tuple[int, int] | None = None
    ) -> Tuple[int, int]:
        """SLOW"""
        if race_map is None:
            race_map = self.race_map
        best_times: Dict[Tuple[int, int], int] = {self.start: 0}
        working = [self.start]
        step = 0
        key_count = 1
        finished = False
        while not finished:
            step += 1
            new_working = []
            for spot in working:
                for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    check = v_add(spot, dir)
                    if check == self.end:
                        finished = True
                        return step, key_count
                    elif race_map.get(check) == "." and best_times.get(check) is None:
                        best_times[check] = step
                        new_working.append(check)
                    elif check == key_stone and best_times.get(check) == step:
                        key_count += 1
            working = new_working
        return step, key_count

    def remove_blocks(self, min_diff: int = 0) -> int:
        """SLOW"""
        base_case = self.breadth_first()[0]
        block_cnts: Dict[int, int] = {}
        for block, char in self.race_map.items():
            if char == "#":
                steps, cnt = self.breadth_first(self.race_map | {block: "."}, block)
                block_cnts[steps] = block_cnts.get(steps, 0) + cnt
        return sum([v for k, v in block_cnts.items() if base_case - k >= min_diff])

    def bfs(self, start, end) -> Dict[Tuple[int, int], int]:
        best_times: Dict[Tuple[int, int], int] = {start: 0}
        working = [start]
        step = 0
        finished = False
        while not finished:
            step += 1
            new_working = []
            for spot in working:
                for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    check = v_add(spot, dir)
                    if check == end:
                        finished = True
                    if self.race_map.get(check) != "#" and best_times.get(check) is None:
                        best_times[check] = step
                        new_working.append(check)
            working = new_working
        return best_times

    def check_shortcuts(self, max_shortcut: int, min_improve: int) -> int:
        start_start = self.bfs(self.start, self.end)
        end_start = self.bfs(self.end, self.start)
        longest_path = start_start[self.end]
        paths = 0
        for start_jump, start_dist in start_start.items():
            if longest_path - start_dist >= min_improve:
                for end_jump, end_dist in end_start.items():
                    if longest_path - (start_dist + end_dist) >= min_improve:
                        jump_dist = abs(start_jump[0] - end_jump[0]) + abs(start_jump[1] - end_jump[1])
                        if (
                            jump_dist <= max_shortcut
                            and longest_path - (start_dist + jump_dist + end_dist) >= min_improve
                        ):
                            paths += 1
        return paths


assert RaceMap(EXAMPLE).breadth_first() == (84, 1)
assert RaceMap(EXAMPLE).check_shortcuts(2, 1) == 44

daily_input = read_input("20")
print(RaceMap(daily_input).check_shortcuts(2, 100))
print(RaceMap(daily_input).check_shortcuts(20, 100))
