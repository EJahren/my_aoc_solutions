import sys


def irange(start, stop):
    return list(range(start, stop + 1))


def part1(lines):
    return sum(
        (set(x) & set(y) in (set(y), set(x)))
        for x, y in (
            list(map(lambda x: irange(*map(int, x.split("-"))), l.split(",")))
            for l in lines
        )
    )


def test_part1():
    assert (
        part1(
            [
                "2-4,6-8",
                "2-3,4-5",
                "5-7,7-9",
                "2-8,3-7",
                "6-6,4-6",
                "2-6,4-8",
            ]
        )
        == 2
    )


def part2(lines):
    return sum(
        len(set(x) & set(y)) > 0
        for x, y in (
            list(map(lambda x: irange(*map(int, x.split("-"))), l.split(",")))
            for l in lines
        )
    )


if __name__ == "__main__":
    print(part2([l[:-1] for l in sys.stdin]))
