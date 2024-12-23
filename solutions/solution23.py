from typing import Dict, List

from . import read_input

EXAMPLE = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""


def sort_t(x: str) -> int:
    return (x[0] != "t") * 7000 + int.from_bytes(x.encode(), byteorder="big") - 24929


def parse_input(input_block: str) -> Dict[str, List[str]]:
    connections: Dict[str, List[str]] = {}
    for row in input_block.splitlines():
        vals = sorted(row.split("-"), key=sort_t)
        connections[vals[0]] = connections.get(vals[0], list()) + [vals[1]]
    return connections


def find_three(graph: Dict[str, List[str]]) -> int:
    cnt = 0
    for k, v in graph.items():
        if k[0] == "t":
            for i, first in enumerate(v[:-1]):
                for second in v[i + 1 :]:
                    if second in graph.get(first, list()) or first in graph.get(second, list()):
                        cnt += 1
    return cnt


def find_clique(graph: Dict[str, List[str]]) -> List[str]:
    current_best: List[str] = list()
    sorted_keys = sorted(graph.keys(), key=sort_t)
    for item in sorted_keys:
        pointed = graph.get(item, list())
        if len(pointed) == 1:
            item_best = pointed + [item]
        else:
            subgraph = {
                k: [subpoint for subpoint in v if subpoint in pointed] for k, v in graph.items() if k in pointed
            }
            subbest = find_clique(subgraph)
            item_best = subbest + [item]
        if len(item_best) > len(current_best):
            current_best = item_best
    return current_best


def password_style(clique: List[str]) -> str:
    return ",".join(sorted(clique))


assert find_three(parse_input(EXAMPLE)) == 7
assert password_style(find_clique(parse_input(EXAMPLE))) == "co,de,ka,ta"
daily_input = read_input("23")
print(find_three(parse_input(daily_input)))
print(password_style(find_clique(parse_input(daily_input))))
