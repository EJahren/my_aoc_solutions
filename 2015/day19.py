import heapq
import sys

from pygtrie import CharTrie


def parse(inp: list[str]) -> list[tuple[str, str]]:
    res = []
    for w in inp:
        k, _, v = w.split()
        res.append((k, v))
    return res


def count_molecules(replacements, molecule):
    distinct = set()

    for k, v in replacements:
        i = 0
        start = 0
        i = molecule.find(k, start)
        while i >= 0:
            distinct.add(molecule[:i] + v + molecule[i + len(k) :])
            start = i + 1
            i = molecule.find(k, start)
    return len(distinct)


def test_part1():
    replacements = parse(
        [
            "H => HO",
            "H => OH",
            "O => HH",
        ]
    )

    assert replacements == [("H", "HO"), ("H", "OH"), ("O", "HH")]

    assert count_molecules(replacements, "HOH") == 4
    assert count_molecules(replacements, "HOHOHO") == 7


if __name__ == "__main__":
    inp = list(sys.stdin)
    replacements = parse(inp[:-2])
    to_generate = inp[-1]
    print(count_molecules(replacements, to_generate))

    # For part2 finding the generation sequence is challenging
    # However looking at the rewrite rules, there must be a unique
    # number of steps, and each rule increases the size by the
    # same number of "molecules", except for each "Y" there is
    # an additional molecule

    molecules = set(r[0] for r in replacements)

    num_molecules = sum(to_generate.count(m) for m in molecules)
    print(num_molecules - to_generate.count("Y"))
