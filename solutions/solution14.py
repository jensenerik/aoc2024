from functools import reduce
from typing import List, Tuple

from . import read_input

EXAMPLE_SIZE = (11, 7)

EXAMPLE = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

DAILY_INPUT_SIZE = (101, 103)


def cmp(x: int, y: int) -> int:
    return (x > y) - (y > x)


class Robot:
    def __init__(self, position: Tuple[int, int], velocity: Tuple[int, int], board_size: Tuple[int, int]):
        self.position = position
        self.velocity = velocity
        self.board_size = board_size

    def move(self, steps: int):
        x = (self.position[0] + self.velocity[0] * steps) % self.board_size[0]
        y = (self.position[1] + self.velocity[1] * steps) % self.board_size[1]
        self.position = (x, y)

    def quadrant(self) -> Tuple[int, int]:
        return (cmp(self.board_size[0] // 2, self.position[0]), cmp(self.board_size[1] // 2, self.position[1]))

    def __repr__(self):
        return str(self.position) + " " + str(self.velocity)


def parse_input(input_block: str, board_size: Tuple[int, int]) -> List[Robot]:
    robots = []
    for row in input_block.splitlines():
        pos, vel = row.split()
        pos_vector = [int(p) for p in pos[2:].split(",")]
        vel_vector = [int(v) for v in vel[2:].split(",")]
        robots.append(Robot((pos_vector[0], pos_vector[1]), (vel_vector[0], vel_vector[1]), board_size))
    return robots


def move_all(robots: List[Robot], steps: int) -> List[Robot]:
    for robot in robots:
        robot.move(steps)
    return robots


def calculate_quadrants(robots: List[Robot]) -> int:
    quads = [robot.quadrant() for robot in robots]
    quad_cnts = []
    for x in [-1, 1]:
        for y in [-1, 1]:
            quad_cnts.append(quads.count((x, y)))
    return reduce(lambda x, y: x * y, quad_cnts, 1)


def check_symm(robots: List[Robot]) -> int:
    check_val = 0
    for row in range(robots[0].board_size[1]):
        rowbots = [robot for robot in robots if robot.position[1] == row]
        for col in range(robots[0].board_size[0] // 2):
            left = len([robot for robot in rowbots if robot.position == (col, row)])
            right = len([robot for robot in rowbots if robot.position == ((-col - 1) % robot.board_size[0], row)])
            check_val += (right == 0) == (left == 0)
    return check_val


def check_bottom_heavy(robots: List[Robot]) -> int:
    return sum(
        row * len([robot for robot in robots if robot.position[1] == row]) for row in range(robots[0].board_size[1])
    )


def check_central_heavy(robots: List[Robot]) -> int:
    middle = (robots[0].board_size[0] // 2, robots[0].board_size[1] // 2)
    return sum(
        [
            robot.board_size[0]
            + robot.board_size[1]
            - abs(robot.position[0] - middle[0])
            - abs(robot.position[1] - middle[1])
            for robot in robots
        ]
    )


def check_cluster(robots: List[Robot]) -> int:
    middle = (
        sum([robot.position[0] for robot in robots]) // len(robots),
        sum([robot.position[1] for robot in robots]) // len(robots),
    )
    return sum(
        [
            robot.board_size[0]
            + robot.board_size[1]
            - abs(robot.position[0] - middle[0])
            - abs(robot.position[1] - middle[1])
            for robot in robots
        ]
    )


def look_for_tree(robots: List[Robot]) -> Tuple[int, int]:
    max_val = 0
    max_iter = 0
    for iter in range(10000):
        robots = move_all(robots, 1)
        new_val = check_cluster(robots)
        if new_val > max_val:
            max_val = new_val
            max_iter = iter + 1
            print(max_val, max_iter)
            print_pos(robots)
    return max_val, max_iter


def print_pos(robots: List[Robot]):
    for y in range(robots[0].board_size[1]):
        row = ""
        for x in range(robots[0].board_size[0]):
            rob_count = len([robot for robot in robots if robot.position == (x, y)])
            row = row + (str(rob_count) if rob_count > 0 else ".")
        print(row + "\n")


assert calculate_quadrants(move_all(parse_input(EXAMPLE, EXAMPLE_SIZE), 100)) == 12

daily_input = read_input("14")
print(calculate_quadrants(move_all(parse_input(daily_input, DAILY_INPUT_SIZE), 100)))
print(look_for_tree(parse_input(daily_input, DAILY_INPUT_SIZE)))
