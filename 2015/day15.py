import sys
from dataclasses import astuple, dataclass
from math import prod
from typing import Self


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    @classmethod
    def parse(cls, inp: str) -> Self:
        """ """
        words = inp.split()
        return cls(
            words[0][:-1],
            int(words[2][:-1]),
            int(words[4][:-1]),
            int(words[6][:-1]),
            int(words[8][:-1]),
            int(words[-1]),
        )


def test_parse():
    assert Ingredient.parse(
        "Frosting: capacity 4, durability -2, flavor 0, texture 0, calories 5"
    ) == Ingredient("Frosting", 4, -2, 0, 0, 5)


Recepie = list[tuple[int, Ingredient]]


def tastiness(recepie: Recepie) -> int:
    amounts = [
        [amount * c for c in astuple(ingredient)[1:-1]]
        for amount, ingredient in recepie
    ]
    property_scores = [sum(x) for x in zip(*amounts)]
    if any(a <= 0 for a in property_scores):
        return 0
    return prod(sum(x) for x in zip(*amounts))


def calories(recepie: Recepie) -> int:
    return sum(amount * ingredient.calories for amount, ingredient in recepie)


def test_tastiness():
    ingredients = list(
        map(
            Ingredient.parse,
            [
                "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8",
                "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3",
            ],
        )
    )
    assert tastiness([(44, ingredients[0]), (56, ingredients[1])]) == 62842880


def optimize(recepie: list[Ingredient]) -> int:
    amounts = []
    incumbent = 0
    for x1 in range(100):
        for x2 in range(100 - x1):
            for x3 in range(100 - (x1 + x2)):
                x4 = 100 - (x1 + x2 + x3)
                amounts = [x1, x2, x3, x4]
                assert sum(amounts) == 100
                if calories(list(zip(amounts, recepie))) != 500:
                    continue
                new_tastiness = tastiness(list(zip(amounts, recepie)))
                if new_tastiness >= incumbent:
                    incumbent = new_tastiness
    return incumbent


if __name__ == "__main__":
    print(optimize([Ingredient.parse(x) for x in sys.stdin]))
