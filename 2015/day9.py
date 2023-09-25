import random
import sys
from contextlib import suppress
from functools import reduce

import hypothesis.strategies as st
from hypothesis import given

Edge = tuple[str, str]
Graph = dict[Edge, int]


def parse_graph(lines: list[str]) -> Graph:
    graph = {}
    for l in lines:
        words = l.split()
        graph[(words[0], words[2])] = int(words[-1])
        graph[(words[2], words[0])] = int(words[-1])
    return graph


def test_parse_graph():
    assert parse_graph(
        [
            "London to Dublin = 464",
            "London to Belfast = 518",
            "Dublin to Belfast = 141",
        ]
    ) == {
        ("London", "Dublin"): 464,
        ("London", "Belfast"): 518,
        ("Dublin", "Belfast"): 141,
        ("Dublin", "London"): 464,
        ("Belfast", "London"): 518,
        ("Belfast", "Dublin"): 141,
    }


def all_cities(g: Graph) -> set[str]:
    return set(reduce(lambda a, b: a + list(b), g.keys(), []))


def test_all_cities():
    assert all_cities(
        parse_graph(
            [
                "London to Dublin = 464",
                "London to Belfast = 518",
                "Dublin to Belfast = 141",
            ]
        )
    ) == {"London", "Belfast", "Dublin"}


def path_length(g: Graph, path: list[str]) -> int:
    if len(path) == 0:
        return 0
    length = 0
    previous = path[0]
    for next in path[1:]:
        length += g[(previous, next)]
        previous = next
    return length


def is_hamiltonian_path(g: Graph, path: list[str]) -> bool:
    if len(path) == 0:
        return True
    previous = path[0]
    visited = {previous}
    for next in path[1:]:
        if (previous, next) not in g:
            return False
        visited.add(next)
        previous = next
    return visited == all_cities(g)


class GaveUp(Exception):
    pass


def random_hamiltonian_path(g: Graph, retries: int = 100) -> list[str]:
    if g == {}:
        return []
    to_visit = list(all_cities(g))
    start = random.choice(to_visit)
    to_visit.remove(start)
    path = [start]

    while to_visit:
        choices = list(filter(lambda x: (path[-1], x) in g, to_visit))
        if len(choices) == 0:
            if retries <= 0:
                raise GaveUp()
            return random_hamiltonian_path(g, retries=retries - 1)
        choice = random.choice(choices)
        to_visit.remove(choice)
        path.append(choice)
    return path


def test_random_hamiltonian_example():
    # example only has one valid
    g = parse_graph(
        [
            "London to Dublin = 464",
            "London to Belfast = 518",
            "Dublin to Belfast = 141",
        ]
    )
    assert random_hamiltonian_path(g)
    assert path_length(g, ["London", "Dublin", "Belfast"]) == 605


graphs = st.from_type(Graph)


@given(graphs)
def test_random_hamiltonian(g: Graph):
    with suppress(GaveUp):
        assert is_hamiltonian_path(g, random_hamiltonian_path(g))


def can_swap(g: Graph, path: list[str], i: int, j: int) -> bool:
    n = len(path) - 1
    return (
        (i == 0 or (path[i - 1], path[j]) in g)
        and (i == n or (path[j], path[i + 1]) in g)
        and (j == 0 or (path[j - 1], path[i]) in g)
        and (j == n or (path[i], path[j + 1]) in g)
    )


def swap_improves(g: Graph, path: list[str], i: int, j: int) -> bool:
    if not can_swap(g, path, i, j):
        return False
    n = len(path) - 1
    cost_after = (
        (g[(path[i - 1], path[j])] if i > 0 else 0)
        + (g[(path[j], path[i + 1])] if i < n else 0)
        + (g[(path[j - 1], path[i])] if j > 0 else 0)
        + (g[(path[i], path[j + 1])] if j < n else 0)
    )
    cost_before = (
        (g[(path[i - 1], path[i])] if i > 0 else 0)
        + (g[(path[i], path[i + 1])] if i < n else 0)
        + (g[(path[j - 1], path[j])] if j > 0 else 0)
        + (g[(path[j], path[j + 1])] if j < n else 0)
    )
    return cost_after < cost_before


def swap(path: list[str], i: int, j: int) -> None:
    path[i], path[j] = path[j], path[i]


def find_best_hamiltonian(inp: list[str]):
    g = parse_graph(inp)
    p = random_hamiltonian_path(g)
    for i in range(len(p)):
        for j in range(len(p)):
            if i != j and swap_improves(g, p, i, j):
                swap(p, i, j)
    return path_length(g, p)


if __name__ == "__main__":
    inp = []
    for line in sys.stdin:
        inp.append(line[:-1])
    best = None
    while True:
        try:
            next = find_best_hamiltonian(inp)
            if best is None or next > best:
                best = next
                print("best so far:", best)
        except GaveUp:
            pass
