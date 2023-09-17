import sys
from collections import defaultdict


def move_direction(position, direction):
    if direction == "^":
        position[0] += 1
    if direction == "v":
        position[0] -= 1
    if direction == ">":
        position[1] += 1
    if direction == "<":
        position[1] -= 1


def part1(puzzle_input):
    houses = defaultdict(lambda: 0)
    position = [0, 0]
    for direction in puzzle_input:
        houses[tuple(position)] += 1
        move_direction(position, direction)
    houses[tuple(position)] += 1
    return len([v for v in houses.values() if v > 0])


def test_examples_given_in_part1():
    assert part1(">") == 2
    assert part1("^>v<") == 4
    assert part1("^v^v^v^v^v") == 2


def part2(puzzle_input):
    houses = defaultdict(lambda: 0)
    santa = [0, 0]
    robo = [0, 0]
    for santa_dir, robo_dir in zip(*[iter(puzzle_input)] * 2):
        houses[tuple(santa)] += 1
        houses[tuple(robo)] += 1
        move_direction(santa, santa_dir)
        move_direction(robo, robo_dir)
    houses[tuple(santa)] += 1
    houses[tuple(robo)] += 1
    return len([v for v in houses.values() if v > 0])


def test_examples_given_in_part2():
    assert part2("^v") == 3
    assert part2("^>v<") == 3
    assert part2("^v^v^v^v^v") == 11


if __name__ == "__main__":
    puzzle_input = ""
    total = 0
    for line in sys.stdin:
        puzzle_input += line
    print(part2(puzzle_input))
