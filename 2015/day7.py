import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np

Wire = str
Signal = np.uint16

Operand = Wire | Signal


@dataclass
class UnaryGate(ABC):
    operand1: Operand
    output: Wire

    def operands(self):
        return [self.operand1]

    @classmethod
    @abstractmethod
    def apply(cls, a: Signal) -> Signal:
        ...


@dataclass
class BinaryGate(ABC):
    operand1: Operand
    operand2: Operand
    output: Wire

    def operands(self):
        return [self.operand1, self.operand2]

    @classmethod
    @abstractmethod
    def apply(cls, a: Signal, b: Signal) -> Signal:
        ...


class And(BinaryGate):
    @classmethod
    def apply(cls, a: Signal, b: Signal) -> Signal:
        return np.bitwise_and(a, b)


class Or(BinaryGate):
    @classmethod
    def apply(cls, a: Signal, b: Signal) -> Signal:
        return np.bitwise_or(a, b)


class LeftShift(BinaryGate):
    @classmethod
    def apply(cls, a: Signal, b: Signal) -> Signal:
        return np.left_shift(a, b)


class RightShift(BinaryGate):
    @classmethod
    def apply(cls, a: Signal, b: Signal) -> Signal:
        return np.right_shift(a, b)


class Not(UnaryGate):
    @classmethod
    def apply(cls, a: Signal) -> Signal:
        return np.bitwise_not(a)


class Identity(UnaryGate):
    @classmethod
    def apply(cls, a: Signal) -> Signal:
        return a


def parse_operand(a: str) -> Operand:
    if a.isdigit():
        return np.uint16(a)
    else:
        return a


bin_op_map = {
    "AND": And,
    "OR": Or,
    "LSHIFT": LeftShift,
    "RSHIFT": RightShift,
}


def parse_instruction(instruction: str) -> UnaryGate | BinaryGate:
    arrow_idx = instruction.index("->")
    for key, constructor in bin_op_map.items():
        if key in instruction:
            idx = instruction.index(key)
            return constructor(
                parse_operand(instruction[: idx - 1]),
                parse_operand(instruction[idx + len(key) + 1 : arrow_idx - 1]),
                instruction[arrow_idx + 3 :],
            )
    if "NOT" in instruction:
        return Not(
            parse_operand(instruction[4 : arrow_idx - 1]),
            instruction[arrow_idx + 3 :],
        )
    return Identity(
        parse_operand(instruction[: arrow_idx - 1]),
        instruction[arrow_idx + 3 :],
    )


def eval_gates(gates: Sequence[UnaryGate | BinaryGate]) -> Mapping[Wire, Signal]:
    fixpoint = False
    assignment = {}
    for gate in gates:
        if all(isinstance(o, Signal) for o in gate.operands()):
            assignment[gate.output] = gate.apply(*gate.operands())
    while not fixpoint:
        fixpoint = True
        for gate in gates:
            if all(o in assignment for o in gate.operands() if isinstance(o, Wire)):
                if gate.output not in assignment:
                    fixpoint = False
                assignment[gate.output] = gate.apply(
                    *[
                        assignment[o] if isinstance(o, Wire) else o
                        for o in gate.operands()
                    ]
                )
    return assignment


def part1(gates: Sequence[UnaryGate | BinaryGate]) -> np.uint16:
    return eval_gates(gates)["a"]


def test_parsing_of_instructions():
    assert parse_instruction("a LSHIFT 2 -> x") == LeftShift("a", np.uint16(2), "x")
    assert parse_instruction("NOT 123 -> x") == Not(np.uint16(123), "x")
    assert parse_instruction("123 -> x") == Identity(np.uint16(123), "x")
    assert parse_instruction("1 LSHIFT 2 -> x") == LeftShift(
        np.uint16(1), np.uint16(2), "x"
    )
    assert parse_instruction("he RSHIFT 5 -> hh") == RightShift(
        "he", np.uint16(5), "hh"
    )


def test_gates_apply():
    assert LeftShift.apply(np.uint16(1), np.uint16(2)) == np.uint16(4)
    assert RightShift.apply(np.uint16(4), np.uint16(2)) == np.uint16(1)
    assert And.apply(np.uint16(1), np.uint16(2)) == np.uint16(0)
    assert Or.apply(np.uint16(4), np.uint16(2)) == np.uint16(6)
    assert Not.apply(np.uint16(123)) == np.uint16(65412)
    assert Identity.apply(np.uint16(123)) == np.uint16(123)


def test_example_given_in_part1():
    assert eval_gates(
        [
            Identity(np.uint16(123), "x"),
            Identity(np.uint16(456), "y"),
            And("x", "y", "d"),
            Or("x", "y", "e"),
            LeftShift("x", np.uint16(2), "f"),
            RightShift("y", np.uint16(2), "g"),
            Not("x", "h"),
            Not("y", "i"),
        ]
    ) == {
        "d": 72,
        "e": 507,
        "f": 492,
        "g": 114,
        "h": 65412,
        "i": 65079,
        "x": 123,
        "y": 456,
    }


def part2(gates: list[UnaryGate | BinaryGate]) -> np.uint16:
    for idx, g in enumerate(gates):
        if isinstance(g, Identity) and g.output == "b":
            gates[idx] = Identity(np.uint16(16076), "b")
    return eval_gates(gates)["a"]


if __name__ == "__main__":
    inp = []
    for line in sys.stdin:
        inp.append(parse_instruction(line[:-1]))
    print(part2(inp))
