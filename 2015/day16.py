import sys


def parse_sue(line: str) -> dict[str, int]:
    assert line[-1] == "\n"
    words = line.split()
    assert words[0] == "Sue"
    result = eval(
        "{" + "'" + "".join(words[2:]).replace(":", "':").replace(",", ",'") + "}"
    )
    result.update(Sue=int(words[1][:-1]))
    return result


looking_for = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def search(inp: list[dict[str, int]]) -> list[int]:
    prospects = []
    for sue in inp:
        is_match = True
        for key in [
            "children",
            "samoyeds",
            "akitas",
            "vizslas",
            "cars",
            "perfumes",
        ]:
            is_match &= looking_for[key] == sue.get(key, looking_for[key])
        for key in ["cats", "trees"]:
            is_match &= looking_for[key] <= sue.get(key, looking_for[key])
        for key in ["pomeranians", "goldfish"]:
            is_match &= looking_for[key] >= sue.get(key, looking_for[key])

        if is_match:
            prospects.append(sue["Sue"])
    return prospects


if __name__ == "__main__":
    print(search([parse_sue(x) for x in sys.stdin]))
