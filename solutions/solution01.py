from typing import Any, Tuple

from solutions import read_input

EXAMPLE = """3   4
4   3
2   5
1   3
3   9
3   3"""


def parse_cols(col_text: str) -> Tuple[Tuple[Any, ...], ...]:
    rows = []
    for row in col_text.splitlines():
        rows.append(row.split())
    return tuple(zip(*rows))


def compare_cols(cols: Tuple[Tuple[Any, ...], ...]) -> int:
    left = sorted([int(item) for item in cols[0]])
    right = sorted([int(item) for item in cols[1]])
    return sum([abs(item[0] - item[1]) for item in zip(left, right)])


def similarity_score(cols: Tuple[Tuple[Any, ...], ...]) -> int:
    left_counts = {item: cols[0].count(item) for item in cols[0]}
    return sum([int(item) * lc * (cols[1].count(item)) for item, lc in left_counts.items()])


assert compare_cols(parse_cols(EXAMPLE)) == 11
assert similarity_score(parse_cols(EXAMPLE)) == 31

problem_input = parse_cols(read_input("01"))

print(compare_cols(problem_input))
print(similarity_score(problem_input))
