from typing import List, NamedTuple, Tuple

from . import read_input

EXAMPLE = "2333133121414131402"


def parse_input(input_block: str) -> List[int | None]:
    system_seq = []
    cur_file = 0
    free = False
    for item in input_block:
        system_seq.extend([None if free else cur_file] * int(item))
        if free:
            cur_file += 1
        free = not free
    return system_seq


def defrag(system_seq: List[int | None]) -> List[int | None]:
    forward_loc = 0
    backward_loc = len(system_seq) - 1
    while forward_loc < backward_loc:
        early_entry = system_seq[forward_loc]
        late_entry = system_seq[backward_loc]
        if early_entry is not None:
            forward_loc += 1
        elif late_entry is None:
            backward_loc -= 1
        else:
            system_seq[forward_loc] = late_entry
            system_seq[backward_loc] = early_entry
            forward_loc += 1
            backward_loc -= 1
    return system_seq


def calc_hash(system_seq: List[int | None]) -> int:
    return sum([i * val for i, val in enumerate(system_seq) if val is not None])


class Fileblock(NamedTuple):
    start: int
    length: int
    value: int | None


def parse_input_smartly(input_block: str) -> Tuple[List[Fileblock], List[Fileblock]]:
    files = []
    free_blocks = []
    cur_file = 0
    free = False
    location = 0
    for item in input_block:
        length = int(item)
        if free:
            free_blocks.append(Fileblock(location, length, None))
        else:
            files.append(Fileblock(location, length, cur_file))
            cur_file += 1
        location += length
        free = not free
    return files, free_blocks


def defrag_smartly(files: List[Fileblock], free_blocks: List[Fileblock]) -> List[Fileblock]:
    defragged_files = []
    corrected_free = None
    corrected_spot = None
    for file in reversed(files):
        still_looking = True
        while still_looking:
            for i, free_space in enumerate(free_blocks):
                leftover = free_space.length - file.length
                if (leftover >= 0) and (file.start > free_space.start):
                    defragged_files.append(Fileblock(free_space.start, file.length, file.value))
                    corrected_free = Fileblock(free_space.start + file.length, leftover, None)
                    corrected_spot = i
                    still_looking = False
                    break
            if still_looking:
                defragged_files.append(file)
                still_looking = False
        if isinstance(corrected_spot, int) and isinstance(corrected_free, Fileblock):
            free_blocks[corrected_spot] = corrected_free
            corrected_free = None
            corrected_spot = None
    return defragged_files


def calc_hash_smartly(defragged_blocks: List[Fileblock]) -> int:
    running_sum = 0
    for file in defragged_blocks:
        running_sum += sum(
            [
                file.value * position
                for position in range(file.start, file.start + file.length)
                if file.value is not None
            ]
        )
    return running_sum


assert calc_hash(defrag(parse_input(EXAMPLE))) == 1928
assert calc_hash_smartly(defrag_smartly(*parse_input_smartly(EXAMPLE))) == 2858

daily_input = read_input("09")
print(calc_hash(defrag(parse_input(daily_input))))
print(calc_hash_smartly(defrag_smartly(*parse_input_smartly(daily_input))))
