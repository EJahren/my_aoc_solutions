import sys


def priority(x):
    """
    >>> priority("p")
    16
    >>> priority("L")
    38
    >>> priority("P")
    42
    """
    return ord(x) - ord("a") + 1 if x.islower() else ord(x) - ord("A") + 27


if __name__ == "__main__":
    lines = [l[:-1] for l in sys.stdin]
    print(
        sum(
            sum(
                map(priority, set(line[: len(line) // 2]) & set(line[len(line) // 2 :]))
            )
            for line in lines
        )
    )
    print(
        sum(
            sum(map(priority, set(x) & set(y) & set(z)))
            for x, y, z in zip(*([iter(lines)] * 3))
        )
    )
