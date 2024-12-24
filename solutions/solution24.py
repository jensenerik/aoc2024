from typing import Dict, List, NamedTuple, Tuple

from solutions.solution24_examples import EXAMPLE, LARGE_EXAMPLE

from . import read_input


class Gate(NamedTuple):
    val_1: str
    operator: str
    val_2: str
    result: str

    def apply_val(self, value_map: Dict[str, int]) -> int:
        if self.operator == "AND":
            return value_map[self.val_1] * value_map[self.val_2]
        elif self.operator == "OR":
            return int(value_map[self.val_1] + value_map[self.val_2] > 0)
        elif self.operator == "XOR":
            return (value_map[self.val_1] + value_map[self.val_2]) % 2
        else:
            raise Exception("no operator")


def parse_input(input_block: str) -> Tuple[Dict[str, int], List[Gate]]:
    initial, gates = input_block.split("\n\n")
    return (
        {init.split(": ")[0]: int(init.split(": ")[1]) for init in initial.splitlines()},
        [
            Gate(split_gate[0], split_gate[1], split_gate[2], split_gate[4])
            for split_gate in [gate.split() for gate in gates.splitlines()]
        ],
    )


def run_gates(value_map: Dict[str, int], gates: List[Gate]) -> Dict[str, int]:
    while len(gates) > 0:
        gate = gates.pop(0)
        if gate.val_1 in value_map and gate.val_2 in value_map:
            value_map[gate.result] = gate.apply_val(value_map)
        else:
            gates.append(gate)
    return value_map


def binary_z(value_map: Dict[str, int]) -> int:
    just_z = sorted([k for k in value_map if k[0] == "z"])
    running_sum = 0
    cur_exponent = 0
    for z_val in just_z:
        running_sum += value_map[z_val] * (2**cur_exponent)
        cur_exponent += 1
    return running_sum


def impossible_gates(gates: List[Gate]):
    imp_gates = []
    for gate in gates:
        if gate.operator == "XOR":
            if gate.val_1[0] not in ["x", "y"] and gate.result[0] != "z":
                imp_gates.append(gate)
    return imp_gates


def and_or_wires(gates: List[Gate]):
    and_results = []
    or_vals = []
    for gate in gates:
        if gate.operator == "OR":
            or_vals.extend([gate.val_1, gate.val_2])
        elif gate.operator == "AND":
            and_results.append(gate.result)
    return (set(and_results).difference(or_vals), set(or_vals).difference(and_results))


assert binary_z(run_gates(*parse_input(EXAMPLE))) == 4
assert binary_z(run_gates(*parse_input(LARGE_EXAMPLE))) == 2024

daily_input = read_input("24")
print(binary_z(run_gates(*parse_input(daily_input))))
print(impossible_gates(parse_input(daily_input)[1]))
print(and_or_wires(parse_input(daily_input)[1]))
# Then manually figure it out
