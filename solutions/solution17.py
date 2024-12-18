from typing import List

EXAMPLE = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

MIRROR_EXAMPLE = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

daily_input = """Register A: 23999685
Register B: 0
Register C: 0

Program: 2,4,1,1,7,5,1,5,0,3,4,4,5,5,3,0"""


class Registers:
    def __init__(self, registers: List[int], instructions: List[int]):
        self.A = registers[0]
        self.B = registers[1]
        self.C = registers[2]
        self.instructions = instructions
        self.pointer = 0
        self.output: List[int] = []

    def __repr__(self):
        return (
            f"RegA: {self.A}, RegB: {self.B}, RegC: {self.C}, output: {self.output}, "
            + f"instr: {self.instructions}, pointer: {self.pointer}"
        )

    def next_instr(self):
        instr, operand = tuple(self.instructions[self.pointer : self.pointer + 2])
        self.pointer += 2
        self.apply_instr(instr, operand)

    def run_program(self) -> str:
        while self.pointer < len(self.instructions):
            self.next_instr()
        return ",".join([str(item) for item in self.output])

    def mirror_program(self) -> int:
        regA = 0
        finished = False
        while not finished:
            self.A = regA
            while (
                self.pointer < len(self.instructions)
                and len(self.output) <= len(self.instructions)
                and self.output == self.instructions[: len(self.output)]
            ):
                self.next_instr()
            if self.output == self.instructions:
                finished = True
            else:
                regA += 1
                self.B = 0
                self.C = 0
                self.pointer = 0
                self.output = []
        return regA

    def combo_operand(self, operand: int) -> int:
        match operand:
            case x if x in [0, 1, 2, 3]:
                return operand
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case _:
                raise Exception("combo operand 7")
        raise Exception("combo failed")

    def apply_instr(self, instr: int, operand: int):
        match instr:
            case 0:
                self.A = self.A // (2 ** self.combo_operand(operand))
            case 1:
                self.B = self.B ^ operand
            case 2:
                self.B = self.combo_operand(operand) % 8
            case 3:
                if self.A != 0:
                    self.pointer = operand
            case 4:
                self.B = self.B ^ self.C
            case 5:
                self.output.append(self.combo_operand(operand) % 8)
            case 6:
                self.B = self.A // (2 ** self.combo_operand(operand))
            case 7:
                self.C = self.A // (2 ** self.combo_operand(operand))


def parse_input(input_block: str) -> Registers:
    regs, prog = input_block.split("\n\n")
    reg_vals = [int(reg.split(": ")[1]) for reg in regs.splitlines()]
    return Registers(reg_vals, [int(command) for command in prog.split(": ")[1].split(",")])


def skip_all() -> int:
    program = [2, 4, 1, 1, 7, 5, 1, 5, 0, 3, 4, 4, 5, 5, 3, 0]
    checking = [(i, 1) for i in range(8)]
    answers = []
    while len(checking) > 0:
        regA, digit = checking.pop(0)
        # regA = regA_start
        # while regA > 0:
        val = (((regA % 8) ^ 1) ^ 5) ^ (regA // 2 ** ((regA % 8) ^ 1)) % 8
        # output.append(val)
        # regA = regA // 8
        if val == program[-digit]:
            if digit == len(program):
                answers.append(regA)
            else:
                checking.extend([(regA * 8 + i, digit + 1) for i in range(8)])
    return min(answers)


assert parse_input(EXAMPLE).run_program() == "4,6,3,5,6,3,5,2,1,0"
assert parse_input(MIRROR_EXAMPLE).mirror_program() == 117440


print(parse_input(daily_input).run_program())
print(skip_all())
