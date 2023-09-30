import sys
from dataclasses import dataclass
from itertools import permutations
from typing import Sequence


@dataclass
class Constraint:
    name: str
    hapiness_increase: int
    sitting_next_to: str


def parse(line: str) -> Constraint:
    splitted = line.split()
    name1 = splitted[0]
    gainlose = splitted[2]
    number = int(splitted[3])
    name2 = splitted[-1][:-1]
    if gainlose == "gain":
        return Constraint(name1, number, name2)
    else:
        return Constraint(name1, -number, name2)


def test_parse():
    assert parse(
        "Alice would gain 54 happiness units by sitting next to Bob."
    ) == Constraint("Alice", 54, "Bob")
    assert parse(
        "Alice would lose 79 happiness units by sitting next to Carol."
    ) == Constraint("Alice", -79, "Carol")


def names(constraints: list[Constraint]) -> set[str]:
    return set(c.name for c in constraints).union(
        set(c.sitting_next_to for c in constraints)
    )


def test_names():
    constraints = [
        parse("Alice would gain 54 happiness units by sitting next to Bob."),
        parse("Alice would lose 79 happiness units by sitting next to Carol."),
        parse("Alice would lose 2 happiness units by sitting next to David."),
        parse("Bob would gain 83 happiness units by sitting next to Alice."),
        parse("Bob would lose 7 happiness units by sitting next to Carol."),
        parse("Bob would lose 63 happiness units by sitting next to David."),
        parse("Carol would lose 62 happiness units by sitting next to Alice."),
        parse("Carol would gain 60 happiness units by sitting next to Bob."),
        parse("Carol would gain 55 happiness units by sitting next to David."),
        parse("David would gain 46 happiness units by sitting next to Alice."),
        parse("David would lose 7 happiness units by sitting next to Bob."),
        parse("David would gain 41 happiness units by sitting next to Carol."),
    ]
    assert names(constraints) == {"Alice", "Bob", "Carol", "David"}


def hapiness(seeting: Sequence[str], lookup: dict[tuple[str, str], int]) -> int:
    hapiness = 0
    for i, n in enumerate(seeting):
        hapiness += lookup[(n, seeting[i + 1 if i + 1 < len(seeting) else 0])]
        hapiness += lookup[(n, seeting[i - 1])]
    return hapiness


def test_hapiness():
    constraints = [
        parse("Alice would gain 54 happiness units by sitting next to Bob."),
        parse("Alice would lose 79 happiness units by sitting next to Carol."),
        parse("Alice would lose 2 happiness units by sitting next to David."),
        parse("Bob would gain 83 happiness units by sitting next to Alice."),
        parse("Bob would lose 7 happiness units by sitting next to Carol."),
        parse("Bob would lose 63 happiness units by sitting next to David."),
        parse("Carol would lose 62 happiness units by sitting next to Alice."),
        parse("Carol would gain 60 happiness units by sitting next to Bob."),
        parse("Carol would gain 55 happiness units by sitting next to David."),
        parse("David would gain 46 happiness units by sitting next to Alice."),
        parse("David would lose 7 happiness units by sitting next to Bob."),
        parse("David would gain 41 happiness units by sitting next to Carol."),
    ]
    assert hapiness(["Alice", "Bob", "Carol", "David"], make_lookup(constraints)) == 330


def make_lookup(constraints: list[Constraint]) -> dict[tuple[str, str], int]:
    result = {}
    for c in constraints:
        result[(c.name, c.sitting_next_to)] = c.hapiness_increase
    return result


def test_lookup():
    constraints = [
        parse("Alice would gain 54 happiness units by sitting next to Bob."),
        parse("Alice would lose 79 happiness units by sitting next to Carol."),
        parse("Alice would lose 2 happiness units by sitting next to David."),
        parse("Bob would gain 83 happiness units by sitting next to Alice."),
    ]
    assert make_lookup(constraints) == {
        ("Alice", "Bob"): 54,
        ("Alice", "Carol"): -79,
        ("Alice", "David"): -2,
        ("Bob", "Alice"): 83,
    }


def brute_force_hapiness(constraints: list[Constraint]) -> int:
    best = 0
    seeting = names(constraints)
    lookup = make_lookup(constraints)
    for p in permutations(seeting):
        h = hapiness(p, lookup)
        if h > best:
            best = h
    return best


def test_brute_force_hapiness():
    constraints = [
        parse("Alice would gain 54 happiness units by sitting next to Bob."),
        parse("Alice would lose 79 happiness units by sitting next to Carol."),
        parse("Alice would lose 2 happiness units by sitting next to David."),
        parse("Bob would gain 83 happiness units by sitting next to Alice."),
        parse("Bob would lose 7 happiness units by sitting next to Carol."),
        parse("Bob would lose 63 happiness units by sitting next to David."),
        parse("Carol would lose 62 happiness units by sitting next to Alice."),
        parse("Carol would gain 60 happiness units by sitting next to Bob."),
        parse("Carol would gain 55 happiness units by sitting next to David."),
        parse("David would gain 46 happiness units by sitting next to Alice."),
        parse("David would lose 7 happiness units by sitting next to Bob."),
        parse("David would gain 41 happiness units by sitting next to Carol."),
    ]
    assert brute_force_hapiness(constraints) == 330


def part2(constraints: list[Constraint]) -> int:
    best = 0
    seeting = list(names(constraints))
    lookup = make_lookup(constraints)
    for n in seeting:
        lookup[("myself", n)] = 0
        lookup[(n, "myself")] = 0
    seeting.append("myself")
    for p in permutations(seeting):
        h = hapiness(p, lookup)
        if h > best:
            best = h
    return best


if __name__ == "__main__":
    inp = []
    for line in sys.stdin:
        inp.append(parse(line))
    print(part2(inp))
