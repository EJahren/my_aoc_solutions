import sys
from itertools import product


def parse_grid(inp: list[str]):
    return {(x, y): z[y] == "#" for x, z in enumerate(inp) for y in range(len(z))}


def grid_shape(grid):
    maxi, maxj = 0, 0
    for i, j in grid:
        maxi = max(i, maxi)
        maxj = max(j, maxi)
    return maxi, maxj


def print_grid(grid):
    result = ""
    maxi, maxj = grid_shape(grid)

    for i in range(maxi + 1):
        for j in range(maxj + 1):
            result += "#" if grid[i, j] else "."
        result += "\n"
    return result


def num_lit_neighbours(grid, i, j):
    return sum(
        grid.get((i2, j2), 0)
        for i2, j2 in product([i - 1, i, i + 1], [j - 1, j, j + 1])
        if (i2, j2) != (i, j)
    )


def step(grid):
    new_grid = grid.copy()
    for i, j in grid:
        num_set = num_lit_neighbours(grid, i, j)
        if grid[i, j]:
            new_grid[i, j] = num_set in [2, 3]
        else:
            new_grid[i, j] = num_set == 3

    return new_grid


def test_step():
    test_grid = parse_grid(
        """\
.#.#.#
...##.
#....#
..#...
#.#..#
####..
    """.split()
    )
    assert not test_grid[0, 0]
    assert (
        print_grid(step(test_grid))
        == """\
..##..
..##.#
...##.
......
#.....
#.##..
"""
    )
    assert (
        print_grid(step(step(test_grid)))
        == """\
..###.
......
..###.
......
.#....
.#....
"""
    )
    assert (
        print_grid(step(step(step(test_grid))))
        == """\
...#..
......
...#..
..##..
......
......
"""
    )

    assert (
        print_grid(step(step(step(step(test_grid)))))
        == """\
......
......
..##..
..##..
......
......
"""
    )


def step2(grid):
    new_grid = grid.copy()
    maxi, maxj = grid_shape(grid)
    for i, j in grid:
        if i in (0, maxi) and j in (0, maxj):
            new_grid[i, j] = True
            continue
        num_set = num_lit_neighbours(grid, i, j)
        if grid[i, j]:
            new_grid[i, j] = num_set in [2, 3]
        else:
            new_grid[i, j] = num_set == 3

    return new_grid


def test_step2():
    test_grid = parse_grid(
        """\
##.#.#
...##.
#....#
..#...
#.#..#
####.#
    """.split()
    )
    assert test_grid[0, 0]
    assert (
        print_grid(step2(test_grid))
        == """\
#.##.#
####.#
...##.
......
#...#.
#.####
"""
    )


if __name__ == "__main__":
    inp = list(x[:-1] for x in sys.stdin)
    g = parse_grid(inp)
    maxi, maxj = grid_shape(g)
    for i, j in product([0, maxi], [0, maxj]):
        g[i, j] = True
    for i in range(100):
        g = step2(g)
    print(sum(g.values()))
