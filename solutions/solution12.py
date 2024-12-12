from functools import reduce
from typing import Dict, List, NamedTuple, Set, Tuple

from . import read_input

EXAMPLE = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""


def parse_input(input_block: str) -> Dict[str, List[Tuple[int, int]]]:
    plots: Dict[str, List[Tuple[int, int]]] = {}
    for i, row in enumerate(input_block.splitlines()):
        for j, item in enumerate(row):
            plots[item] = plots.get(item, []) + [(i, j)]
    return plots


class PlotBlock(NamedTuple):
    interior: Set[Tuple[int, int]]
    boundary: Set[Tuple[int, int]]

    def check_adjoining(self, other: "PlotBlock"):
        return not other.boundary.isdisjoint(self.interior)

    def merge_blocks(self, other: "PlotBlock") -> "PlotBlock":
        new_interior = self.interior.union(other.interior)
        new_boundary = self.boundary.difference(other.interior).union(other.boundary.difference(self.interior))
        return PlotBlock(new_interior, new_boundary)

    def area(self) -> int:
        return len(self.interior)

    def perimeter(self) -> int:
        perim = 0
        for bound in self.boundary:
            perim += len(calc_boundary(bound).intersection(self.interior))
        return perim

    def squashed_perimeter(self) -> int:
        perimeter_pairs: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        for bound in self.boundary:
            for int_pt in calc_boundary(bound).intersection(self.interior):
                perimeter_pairs.append((bound, int_pt))
        running_sum = 0
        for pair in perimeter_pairs:
            bound_bound = calc_boundary(pair[0])
            int_bound = calc_boundary(pair[1])
            running_sum += 2 - len(
                [
                    other_pair
                    for other_pair in perimeter_pairs
                    if other_pair[0] in bound_bound and other_pair[1] in int_bound
                ]
            )
        return running_sum // 2


def calc_boundary(loc: Tuple[int, int]) -> Set[Tuple[int, int]]:
    return set([(loc[0] + ((coord + 1) % 2) * shift, loc[1] + coord * shift) for coord in [0, 1] for shift in [-1, 1]])


def construct_blocks(plot_map: List[Tuple[int, int]]) -> List[PlotBlock]:
    blocks: List[PlotBlock] = []
    for pt in plot_map:
        pt_block = PlotBlock(set([pt]), calc_boundary(pt))
        adjoining_blocks = [block for block in blocks if block.check_adjoining(pt_block)]
        non_adj_blocks = [block for block in blocks if not block.check_adjoining(pt_block)]
        blocks = non_adj_blocks + [reduce(lambda cur, new: cur.merge_blocks(new), adjoining_blocks, pt_block)]
    return blocks


def calculate_cost(input_block: str) -> int:
    total_cost = 0
    for symb_pts in parse_input(input_block).values():
        block_map = construct_blocks(symb_pts)
        total_cost += sum([block.area() * block.perimeter() for block in block_map])
    return total_cost


def calculate_squashed_cost(input_block: str) -> int:
    total_cost = 0
    for symb_pts in parse_input(input_block).values():
        block_map = construct_blocks(symb_pts)
        total_cost += sum([block.area() * block.squashed_perimeter() for block in block_map])
    return total_cost


assert calculate_cost(EXAMPLE) == 1930
assert calculate_squashed_cost(EXAMPLE) == 1206

daily_input = read_input("12")
print(calculate_cost(daily_input))
print(calculate_squashed_cost(daily_input))
