from typing import List, NamedTuple, Tuple

from . import read_input

COSTS = {"A": 3, "B": 1}

LIMIT = 100
OFFSET = 10000000000000

EXAMPLE = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


class Game(NamedTuple):
    A: Tuple[int, int]
    B: Tuple[int, int]
    Prize: Tuple[int, int]


def parse_game(input_rows: str) -> Game:
    game_input = []
    for row in input_rows.splitlines():
        x, y = row.split(": ")[1].split(", ")
        game_input.append((int(x[2:]), int(y[2:])))
    return Game(*game_input)


def parse_input(input_block: str) -> List[Game]:
    games: List[Game] = []
    for game in input_block.split("\n\n"):
        games.append(parse_game(game))
    return games


def solve_game(game: Game, offset: int) -> int | None:
    if offset > 0:
        prize = (game.Prize[0] + offset, game.Prize[1] + offset)
        limit = None
    else:
        prize = game.Prize
        limit = LIMIT
    det = game.A[0] * game.B[1] - game.A[1] * game.B[0]
    if det == 0:
        if prize[0] * game.A[1] == prize[1] * game.A[0]:
            a_pushes = prize[0] // game.A[0] if prize[0] % game.A[0] == 0 else None
            b_pushes = prize[0] // game.B[0] if prize[0] % game.B[0] == 0 else None
            if a_pushes is not None and b_pushes is not None:
                a_cost = COSTS["A"] * a_pushes if limit is None or a_pushes <= limit else None
                b_cost = COSTS["B"] * b_pushes if limit is None or b_pushes <= limit else None
                if a_cost is not None and b_cost is not None:
                    return min(a_cost, b_cost)
                else:
                    return None
            else:
                return None
        else:
            return None
    else:
        a_push_num = prize[0] * game.B[1] - prize[1] * game.B[0]
        a_pushes = a_push_num // det if a_push_num % det == 0 else None
        b_push_num = -prize[0] * game.A[1] + prize[1] * game.A[0]
        b_pushes = b_push_num // det if b_push_num % det == 0 else None
        if a_pushes is None or b_pushes is None:
            return None
        elif limit is None or (a_pushes <= limit and b_pushes <= limit):
            return a_pushes * COSTS["A"] + b_pushes * COSTS["B"]
        else:
            return None


def sum_games(input_block: str, offset: int = 0) -> int:
    running_total = 0
    for game in parse_input(input_block):
        game_value = solve_game(game, offset)
        if game_value is not None:
            running_total += game_value
    return running_total


assert sum_games(EXAMPLE) == 480

daily_input = read_input("13")
print(sum_games(daily_input))
print(sum_games(daily_input, OFFSET))
