import sys
from functools import lru_cache


@lru_cache
def knapsack(containers: list[int], target: int, num_chosen: int) -> int:
    if target == 0:
        return 1
    if num_chosen >= 4:
        # minimum possible is 4, easily found
        # by printing num_chosen for each solutiont to
        # part1
        return 0
    return sum(
        knapsack(tuple(list(containers)[i + 1 :]), target - c, num_chosen + 1)
        for i, c in enumerate(containers)
        if c <= target
    )


def test_part1():
    assert knapsack((20, 15, 10, 5, 5), 25, 0) == 4


if __name__ == "__main__":
    containers = list(int(l) for l in sys.stdin)
    print(knapsack(tuple(containers), 150, 0))
