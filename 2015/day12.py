import json
import sys


def part1(inp) -> int:
    if isinstance(inp, list):
        return sum(part1(p) for p in inp)
    if isinstance(inp, dict):
        return sum(part1(p) for p in inp.keys()) + sum(part1(p) for p in inp.values())
    if isinstance(inp, int):
        return inp
    return 0


def test_part1():
    assert part1([]) == 0
    assert part1({}) == 0
    assert part1([1, 2, 3]) == 6
    assert part1({"a": 2, "b": 4}) == 6
    assert part1([[[3]]]) == 3
    assert part1({"a": {"b": 4}, "c": -1}) == 3
    assert part1({"a": [-1, 1]}) == 0
    assert part1([-1, {"a": 1}]) == 0


def has_red(inp) -> bool:
    if isinstance(inp, list):
        return any(has_red(p) for p in inp)
    if isinstance(inp, dict):
        return "red" in inp.keys() or "red" in inp.values() or has_red(inp.keys())
    return False


def part2(inp) -> int:
    if isinstance(inp, list):
        return sum(part2(p) for p in inp)
    if isinstance(inp, dict):
        if has_red(inp):
            return 0
        return sum(part2(p) for p in inp.keys()) + sum(part2(p) for p in inp.values())
    if isinstance(inp, int):
        return inp
    return 0


def test_part2():
    assert part2([1, {"c": "red", "b": 2}, 3]) == 4
    assert part2({"d": "red", "e": [1, 2, 3, 4], "f": 5}) == 0
    assert part2([1, "red", 5]) == 6
    assert part2([]) == 0
    assert part2({}) == 0
    assert part2([1, 2, 3]) == 6
    assert part2({"a": 2, "b": 4}) == 6
    assert part2([[[3]]]) == 3
    assert part2({"a": {"b": 4}, "c": -1}) == 3
    assert part2({"a": [-1, 1]}) == 0
    assert part2([-1, {"a": 1}]) == 0


if __name__ == "__main__":
    inp = json.load(sys.stdin)
    print(part2(inp))
