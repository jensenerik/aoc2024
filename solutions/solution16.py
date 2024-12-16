from typing import Dict, NamedTuple, Set, Tuple

from . import read_input, v_add

EXAMPLE = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

OTHER_EXAMPLE = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

PART_ONE_ANSWER = 105496


class ReindeerMap(NamedTuple):
    maze: Dict[Tuple[int, int], str]
    start: Tuple[int, int]
    end: Tuple[int, int]


class DeerState(NamedTuple):
    pos: Tuple[int, int]
    vel: Tuple[int, int]


def parse_input(input_block: str) -> ReindeerMap:
    maze = {(i, j): symb for i, row in enumerate(input_block.splitlines()) for j, symb in enumerate(row)}
    return ReindeerMap(maze, [k for k, v in maze.items() if v == "S"][0], [k for k, v in maze.items() if v == "E"][0])


def turn(vector: Tuple[int, int], dir: int) -> Tuple[int, int]:
    return (vector[1] * dir, -vector[0] * dir)


def possible_states(deer_state: DeerState, score: int) -> Dict[DeerState, int]:
    return {
        DeerState(deer_state.pos, turn(deer_state.vel, 1)): score + 1000,
        DeerState(deer_state.pos, turn(deer_state.vel, -1)): score + 1000,
        DeerState(v_add(deer_state.pos, deer_state.vel), deer_state.vel): score + 1,
    }


def run_dfs(reindeer_map: ReindeerMap) -> Tuple[int, int]:
    state_min: Dict[DeerState, int] = {}
    state_history: Dict[DeerState, Set[Tuple[int, int]]] = {
        DeerState(reindeer_map.start, (0, 1)): set([reindeer_map.start])
    }
    check_states = [(DeerState(reindeer_map.start, (0, 1)), 0)]
    best_end = None
    while len(check_states) > 0:
        checking = check_states.pop()
        for state, val in possible_states(*checking).items():
            old_best = state_min.get(state)
            if (
                reindeer_map.maze.get(state.pos) != "#"
                and (old_best is None or val <= old_best)
                and (best_end is None or val <= best_end)
                and val <= PART_ONE_ANSWER
            ):
                state_min[state] = val
                if (
                    old_best is None
                    or val < old_best
                    or not state_history.get(checking[0], set()).issubset(state_history.get(state, set()))
                ):
                    if val == old_best:
                        state_history[state] = state_history.get(state, set()).union(
                            state_history.get(checking[0], set())
                        )
                    else:
                        state_history[state] = state_history.get(checking[0], set()).union([state.pos])
                    check_states.append((state, val))
                    if state.pos == reindeer_map.end:
                        if best_end is not None:
                            best_end = min(val, best_end)
                        else:
                            best_end = val
    end_value = min([v for k, v in state_min.items() if k.pos == reindeer_map.end])
    end_states = [k for k, v in state_min.items() if k.pos == reindeer_map.end and v == end_value]
    end_histories = [state_history.get(k, set()) for k in end_states]
    path_spots = len(set([spot for history in end_histories for spot in history]))

    return end_value, path_spots


assert run_dfs(parse_input(EXAMPLE)) == (7036, 45)
assert run_dfs(parse_input(OTHER_EXAMPLE)) == (11048, 64)

daily_input = read_input("16")
print(run_dfs(parse_input(daily_input)))
