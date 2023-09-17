import sys


def part1(instructions):
    floor = 0
    for character in instructions:
        if character == "(":
            floor += 1
        elif character == ")":
            floor -= 1
        else:
            raise ValueError()
    return floor


def test_examples_given_in_part1():
    assert part1("(())") == 0
    assert part1("()()") == 0
    assert part1("(((") == 3
    assert part1("(()(()(") == 3
    assert part1("())") == -1
    assert part1("))(") == -1
    assert part1(")))") == -3
    assert part1(")())())") == -3


def part2(instructions):
    position = 1
    floor = 0
    for character in instructions:
        if character == "(":
            floor += 1
        elif character == ")":
            floor -= 1
        else:
            raise ValueError()
        if floor == -1:
            return position
        position += 1
    return None


def test_examples_given_in_part2():
    assert part2(")") == 1
    assert part2("()())") == 5


if __name__ == "__main__":
    puzzle_input = ""
    for line in sys.stdin:
        puzzle_input += line
    print(part2(puzzle_input))
