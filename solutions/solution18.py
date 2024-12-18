from typing import List, Tuple

from . import read_input, v_add

EXAMPLE = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

EXAMPLE_DIMENSIONS = (7, 7)
INPUT_DIMENSIONS = (71, 71)


def parse_input(input_block: str) -> List[Tuple[int, int]]:
    return [(int(coord.split(",")[0]), int(coord.split(",")[1])) for coord in input_block.splitlines()]


def calc_path(blocks: List[Tuple[int, int]], dimensions: Tuple[int, int], max_blocks: int):
    seen_spaces = {(0, 0): 0}
    checking = [(0, 0)]
    step = 1
    block_set = set(blocks[:max_blocks])
    finished = False
    end_spot = (dimensions[0] - 1, dimensions[1] - 1)
    while not finished:
        new_checking = []
        for start in checking:
            for dir in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                new_spot = v_add(start, dir)
                if (
                    new_spot[0] in range(dimensions[0])
                    and new_spot[1] in range(dimensions[1])
                    and new_spot not in block_set
                ):
                    old_min = seen_spaces.get(new_spot)
                    if old_min is None or step < old_min:
                        seen_spaces[new_spot] = step
                        new_checking.append(new_spot)
                    if new_spot == end_spot:
                        finished = True
        step += 1
        checking = new_checking
        if len(checking) == 0:
            return None
    return seen_spaces[end_spot]


def drop_blocks(blocks: List[Tuple[int, int]], dimensions: Tuple[int, int]):
    for num in range(len(blocks)):
        if calc_path(blocks, dimensions, num) is None:
            return blocks[num - 1]
    else:
        return None


assert calc_path(parse_input(EXAMPLE), EXAMPLE_DIMENSIONS, 12) == 22
assert drop_blocks(parse_input(EXAMPLE), EXAMPLE_DIMENSIONS) == (6, 1)
daily_input = read_input("18")
print(calc_path(parse_input(daily_input), INPUT_DIMENSIONS, 1024))
print(drop_blocks(parse_input(daily_input), INPUT_DIMENSIONS))
