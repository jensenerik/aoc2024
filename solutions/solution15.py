from typing import Dict, Tuple

from . import read_input, v_add

EXAMPLE = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""


class RobotMap:
    def __init__(self, input_block: str, double: bool):
        robot_map: Dict[Tuple[int, int], str] = {}
        for i, row in enumerate(input_block.splitlines()):
            for j, symb in enumerate(row):
                pos = (i, 2 * j) if double else (i, j)
                other_pos = (i, 2 * j + 1)
                if symb == "@":
                    self.robot_pos = pos
                    robot_map[pos] = "@"
                elif symb == "O":
                    robot_map[pos] = "[" if double else symb
                else:
                    robot_map[pos] = symb
                if double:
                    robot_map[other_pos] = "." if symb == "@" else ("]" if symb == "O" else symb)
        self.robot_map = robot_map
        self.double = double

    def move(self, input_move: str):
        move_lookup = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}
        new_robot_pos = v_add(self.robot_pos, move_lookup[input_move])
        new_box_pos = {}
        current_checks = set([new_robot_pos])
        done_checks = set()
        finish_move = True
        cleared_spaces = [self.robot_pos]
        while len(current_checks) > 0:
            current_check = current_checks.pop()
            done_checks.add(current_check)
            current_symb = self.robot_map[current_check]
            if current_symb == "O":
                new_box = v_add(current_check, move_lookup[input_move])
                current_checks.add(new_box)
                new_box_pos[new_box] = current_symb
            elif current_symb in ["[", "]"]:
                new_box = v_add(current_check, move_lookup[input_move])
                if input_move in ["^", "v"]:
                    other_side_loc = v_add(current_check, (0, -1) if current_symb == "]" else (0, 1))
                    if other_side_loc not in done_checks:
                        new_other = v_add(other_side_loc, move_lookup[input_move])
                        current_checks.add(new_other)
                        new_box_pos[new_other] = "[" if current_symb == "]" else "]"
                        cleared_spaces.append(other_side_loc)
                current_checks.add(new_box)
                new_box_pos[new_box] = current_symb
            elif current_symb == "#":
                finish_move = False
                break
        if finish_move:
            for cleared in cleared_spaces:
                self.robot_map[cleared] = "."
            for box_loc, box_type in new_box_pos.items():
                self.robot_map[box_loc] = box_type

            self.robot_pos = new_robot_pos
            self.robot_map[new_robot_pos] = "@"

    def calc_coords(self) -> int:
        return sum([100 * k[0] + k[1] for k, v in self.robot_map.items() if v in ["O", "["]])

    def print_map(self):
        print(self.robot_pos)
        row_length = max([k[1] for k in self.robot_map.keys() if k[0] == 0]) + 1
        height = max([k[0] for k in self.robot_map.keys() if k[1] == 0]) + 1
        for row_num in range(height):
            row = ""
            for row_coord in range(row_length):
                row = row + self.robot_map[(row_num, row_coord)]
            print(row)


def parse_input(input_block: str, double: bool) -> Tuple[RobotMap, str]:
    map_input, move_input = input_block.split("\n\n")
    return RobotMap(map_input.strip(), double), move_input.replace("\n", "")


def move_and_count(input_block: str, double: bool = False) -> int:
    robot_map, move_input = parse_input(input_block, double)
    for command in move_input:
        robot_map.move(command)
    return robot_map.calc_coords()


def parse_and_print(input_block: str, double: bool):
    robot_map, move_input = parse_input(input_block, double)
    robot_map.print_map()


assert move_and_count(EXAMPLE) == 10092
assert move_and_count(EXAMPLE, True) == 9021


daily_input = read_input("15")
print(move_and_count(daily_input))
print(move_and_count(daily_input, True))
