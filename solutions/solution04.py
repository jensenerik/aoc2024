from typing import Dict, List, Tuple

from . import read_input

EXAMPLE = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


def create_xmas_map(input_block: str) -> Dict[Tuple[int, int], str]:
    xmas_map = {}
    for i, row in enumerate(input_block.splitlines()):
        for j, item in enumerate(row):
            xmas_map[(i, j)] = item
    return xmas_map


def gen_sequences(start_loc: Tuple[int, int], seq_length: int) -> List[List[Tuple[int, int]]]:
    return [
        [(start_loc[0] + row_iter * seq_iter, start_loc[1] + col_iter * seq_iter) for seq_iter in range(seq_length)]
        for row_iter in [-1, 0, 1]
        for col_iter in [-1, 0, 1]
    ]


def search_xmas_map(xmas_map: Dict[Tuple[int, int], str], search_word: str):
    xmas_count = 0
    for k, v in xmas_map.items():
        if v == search_word[0]:
            word_seqs = gen_sequences(k, len(search_word))
            possible_words = ["".join([xmas_map.get(loc, "?") for loc in seq]) for seq in word_seqs]
            xmas_count += len([word for word in possible_words if word == search_word])
    return xmas_count


def search_for_x(xmas_map: Dict[Tuple[int, int], str]):
    xmas_count = 0
    for k, v in xmas_map.items():
        if v == "A":
            mas_count = 0
            for diag in [-1, 1]:
                letters = set([xmas_map.get((k[0] + diag * end, k[1] + end), "?") for end in [-1, 1]])
                if letters == set(["M", "S"]):
                    mas_count += 1
            if mas_count == 2:
                xmas_count += 1
    return xmas_count


assert search_xmas_map(create_xmas_map(EXAMPLE), "XMAS") == 18
assert search_for_x(create_xmas_map(EXAMPLE)) == 9

xmas_map = create_xmas_map(read_input("04"))

print(search_xmas_map(xmas_map, "XMAS"))
print(search_for_x(xmas_map))
