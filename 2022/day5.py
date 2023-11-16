import itertools
import sys


def transpose(l):
    return map(reversed, itertools.zip_longest(*l, fillvalue=None))


if __name__ == "__main__":
    stacks = []
    for line in sys.stdin:
        if line == "\n":
            break
        stacks.append(line[1::4])
    stacks = list(
        map(lambda x: list(filter(lambda y: not y.isspace(), x)), transpose(stacks))
    )
    for line in sys.stdin:
        n, f, t = list(map(int, line.split()[1:7:2]))
        stacks[t - 1] += stacks[f - 1][-n:]
        stacks[f - 1] = stacks[f - 1][:-n]
    print([w[-1] for w in stacks])
