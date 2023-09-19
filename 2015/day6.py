import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Literal, Self


@dataclass
class Command:
    kind: Literal["turn on", "turn off", "toggle"]
    start: tuple[int, int]
    end: tuple[int, int]

    @classmethod
    def parse(cls, command: str) -> Self:
        middle = command.index("through")
        after_middle = middle + 7
        end = eval(command[after_middle:])
        if command.startswith("turn on"):
            start = eval(command[7:middle])
            kind = "turn on"
        elif command.startswith("turn off"):
            start = eval(command[8:middle])
            kind = "turn off"
        elif command.startswith("toggle"):
            start = eval(command[6:middle])
            kind = "toggle"
        else:
            raise ValueError()

        return cls(kind, start, end)


def part1(commands: list[Command]) -> int:
    grid = defaultdict(lambda: False)

    for c in commands:
        if c.kind == "turn on":
            for i in range(c.start[0], c.end[0] + 1):
                for j in range(c.start[1], c.end[1] + 1):
                    grid[(i, j)] = True
        elif c.kind == "turn off":
            for i in range(c.start[0], c.end[0] + 1):
                for j in range(c.start[1], c.end[1] + 1):
                    grid[(i, j)] = False
        elif c.kind == "toggle":
            for i in range(c.start[0], c.end[0] + 1):
                for j in range(c.start[1], c.end[1] + 1):
                    grid[(i, j)] = not grid[(i, j)]
        else:
            raise ValueError()

    return sum(grid.values())


def test_examples_given_in_part1():
    assert part1([Command.parse("turn on 0,0 through 999,999")]) == 1000 * 1000
    assert part1([Command.parse("toggle 0,0 through 999,0")]) == 1000
    assert (
        part1(
            [
                Command.parse("turn on 0,0 through 999,999"),
                Command.parse("turn off 499,499 through 500,500"),
            ]
        )
        == 1000 * 1000 - 4
    )


def part2(commands: list[Command]) -> int:
    grid = defaultdict(lambda: 0)

    for c in commands:
        if c.kind == "turn on":
            for i in range(c.start[0], c.end[0] + 1):
                for j in range(c.start[1], c.end[1] + 1):
                    grid[(i, j)] += 1
        elif c.kind == "turn off":
            for i in range(c.start[0], c.end[0] + 1):
                for j in range(c.start[1], c.end[1] + 1):
                    grid[(i, j)] -= 1 if grid[(i, j)] else 0
        elif c.kind == "toggle":
            for i in range(c.start[0], c.end[0] + 1):
                for j in range(c.start[1], c.end[1] + 1):
                    grid[(i, j)] += 2
        else:
            raise ValueError()

    return sum(grid.values())


def test_examples_given_in_part2():
    assert part2([Command.parse("turn on 0,0 through 0,0")]) == 1
    assert part2([Command.parse("turn off 0,0 through 0,0")]) == 0
    assert part2([Command.parse("toggle 0,0 through 999,999")]) == 2000000


if __name__ == "__main__":
    commands = []
    for line in sys.stdin:
        commands.append(Command.parse(line))
    print(part2(commands))
