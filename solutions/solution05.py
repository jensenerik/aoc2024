from typing import List, Tuple

from . import read_input

EXAMPLE = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def parse_input(input_block: str) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    rules = []
    page_orders = []
    for row in input_block.splitlines():
        if "|" in row:
            raw_rule = row.split("|")
            rules.append((int(raw_rule[0]), int(raw_rule[1])))
        elif "," in row:
            page_orders.append([int(page) for page in row.split(",")])
    return rules, page_orders


def check_rule(rules: List[Tuple[int, int]], page_order: List[int]) -> bool:
    for rule in rules:
        if rule[0] in page_order and rule[1] in page_order:
            if page_order.index(rule[0]) > page_order.index(rule[1]):
                return False
    return True


def check_all_orders(rules: List[Tuple[int, int]], page_orders: List[List[int]]) -> int:
    running_sum = 0
    for page_order in page_orders:
        if check_rule(rules, page_order):
            running_sum += page_order[len(page_order) // 2]
    return running_sum


def reorder(rules: List[Tuple[int, int]], page_order: List[int]) -> List[int]:
    applicable_rules = [rule for rule in rules if rule[0] in page_order and rule[1] in page_order]
    mutable_order = page_order
    good_pass = False
    while not good_pass:
        good_pass = True
        for rule in applicable_rules:
            left_index = mutable_order.index(rule[0])
            right_index = mutable_order.index(rule[1])
            if left_index > right_index:
                good_pass = False
                mutable_order[left_index] = rule[1]
                mutable_order[right_index] = rule[0]
    return mutable_order


def rearrange_bad_orders(rules: List[Tuple[int, int]], page_orders: List[List[int]]) -> int:
    running_sum = 0
    for page_order in page_orders:
        if not check_rule(rules, page_order):
            reordered_pages = reorder(rules, page_order)
            running_sum += reordered_pages[len(reordered_pages) // 2]
    return running_sum


assert check_all_orders(*parse_input(EXAMPLE)) == 143
assert rearrange_bad_orders(*parse_input(EXAMPLE)) == 123

day_input = read_input("05")
print(check_all_orders(*parse_input(day_input)))
print(rearrange_bad_orders(*parse_input(day_input)))
