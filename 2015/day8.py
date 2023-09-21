import sys


def characters_of_code(code: str) -> int:
    return len(code)


def characters_of_data(code: str) -> int:
    return len(eval(code))


def test_character_counting():
    assert characters_of_code('""') == 2
    assert characters_of_data('""') == 0

    assert characters_of_code('"abc"') == 5
    assert characters_of_data('"abc"') == 3

    assert characters_of_code('"aaa\\"aaa"') == 10
    assert characters_of_data('"aaa\\"aaa"') == 7

    assert characters_of_code('"\\x27"') == 6
    assert characters_of_data('"\\x27"') == 1


def part1(lines_of_code: list[str]) -> int:
    return sum(characters_of_code(l) - characters_of_data(l) for l in lines_of_code)


def test_example_given_in_part1():
    assert part1(['""', '"abc"', '"aaa\\"aaa"', '"\\x27"']) == 12


def codify(code: str) -> str:
    return '"' + code.replace("\\", "\\\\").replace('"', '\\"') + '"'


def test_using_repr_for_other_way():
    assert codify('""') == '"\\"\\""'
    assert len(codify('""')) == 6
    assert codify('"abc"') == '"\\"abc\\""'
    assert len(codify('"abc"')) == 9
    assert codify('"\\x27"') == '"\\"\\\\x27\\""'
    assert len(codify('"\\x27"')) == 11


def part2(lines_of_code: list[str]) -> int:
    return sum(len(codify(l)) - characters_of_code(l) for l in lines_of_code)


if __name__ == "__main__":
    inp = []
    for line in sys.stdin:
        inp.append(line[:-1])
    print(part2(inp))
