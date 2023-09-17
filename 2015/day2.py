import sys


def parse(puzzle_input):
    return [int(x) for x in puzzle_input.split("x")]


def part1(l, w, h):
    side1 = l * w
    side2 = w * h
    side3 = h * l
    return 2 * side1 + 2 * side2 + 2 * side3 + min(side1, side2, side3)


def test_examples_given_in_part1():
    assert parse("2x3x4") == [2, 3, 4]
    assert part1(2, 3, 4) == 58

    assert parse("1x1x10") == [1, 1, 10]
    assert part1(1, 1, 10) == 43


def part2(l, w, h):
    m1, m2, _ = sorted([l, w, h])
    smallest_perimeter = 2 * m1 + 2 * m2
    volume = l * w * h
    return smallest_perimeter + volume


def test_examples_given_in_part2():
    assert part2(2, 3, 4) == 34
    assert part2(1, 1, 10) == 14


if __name__ == "__main__":
    puzzle_input = ""
    total = 0
    for line in sys.stdin:
        total += part2(*parse(line))
    print(total)
