from typing import Dict, List

EXAMPLE = """029A
980A
179A
456A
379A"""

DAILY_INPUT = """935A
319A
480A
789A
176A"""

num_buttons = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

dir_buttons = {"^": (0, 1), "B": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}

all_buttons = num_buttons | dir_buttons

BIG_GLOBAL_MATRIX: Dict[str, Dict[str, int]] = {}


def convert_to_moves(vert_diff: int, horiz_diff: int, button_type) -> str:
    if button_type == "num1":
        return "^" * (-vert_diff) + "<" * (-horiz_diff)
    elif button_type == "num2":
        return ">" * horiz_diff + "v" * vert_diff
    elif button_type == "dir1":
        return ">" * horiz_diff + "^" * (-vert_diff)
    elif button_type == "dir2":
        return "v" * vert_diff + "<" * (-horiz_diff)
    else:
        return "<" * (-horiz_diff) + "v" * vert_diff + "^" * (-vert_diff) + ">" * horiz_diff


def find_num_paths(start_button: str, end_button: str) -> str:
    start_spot = all_buttons[start_button]
    end_spot = all_buttons[end_button]
    vert_diff = end_spot[0] - start_spot[0]
    horiz_diff = end_spot[1] - start_spot[1]
    if start_button in ["0", "A"] and end_button in ["1", "4", "7"]:
        button_type = "num1"
    elif start_button in ["1", "4", "7"] and end_button in ["0", "A"]:
        button_type = "num2"
    elif start_button == "<" and end_button in ["^", "B"]:  # start at <, end at ^ or B
        button_type = "dir1"
    elif start_button in ["^", "B"] and end_button == "<":  # end at <, start at ^ or B
        button_type = "dir2"
    else:
        button_type = "other"
    return convert_to_moves(vert_diff, horiz_diff, button_type)


def push_sequence(num_seq: str) -> Dict[str, int]:
    poss_answer = BIG_GLOBAL_MATRIX.get(num_seq)
    if poss_answer is not None:
        return poss_answer
    start_button = "A" if num_seq[0] in num_buttons.keys() else "B"
    total_seq: List[str] = []
    for button in num_seq:
        total_seq.append(find_num_paths(start_button, button) + "B")
        start_button = button
    solved_seq = {item: total_seq.count(item) for item in total_seq}
    BIG_GLOBAL_MATRIX[num_seq] = solved_seq
    return solved_seq


def push_repeated(num_seq: Dict[str, int], rounds: int) -> int:
    working_seq = num_seq
    for _ in range(rounds):
        new_working: Dict[str, int] = {}
        for seq, val in working_seq.items():
            pre_mult_sol = push_sequence(seq)
            for item, newval in pre_mult_sol.items():
                new_working[item] = new_working.get(item, 0) + val * newval
        working_seq = new_working
    return sum(working_seq.values())


def calculate_complexities(input_block: str, rounds: int) -> int:
    total_sum = 0
    for row in input_block.splitlines():
        total_sum += push_repeated({row: 1}, rounds) * int(row[:-1])
    return total_sum


assert push_repeated({"029A": 1}, 4) == 68
assert calculate_complexities(EXAMPLE, 4) == 126384
print(calculate_complexities(DAILY_INPUT, 4))
print(calculate_complexities(DAILY_INPUT, 27))
