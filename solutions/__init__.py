__version__ = "0.1.0"
from typing import Tuple


def read_input(day: str) -> str:
    with open(f"inputs/input{day}.txt") as file:
        return file.read().strip("\n")


def v_add(position: Tuple[int, int], velocity: Tuple[int, int]) -> Tuple[int, int]:
    return position[0] + velocity[0], position[1] + velocity[1]
