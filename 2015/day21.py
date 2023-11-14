from dataclasses import dataclass
from itertools import product
from typing import Literal


@dataclass
class Character:
    hp: int
    hit: int
    armor: int


WEAPON_COST = [8, 10, 25, 40, 74]
ARMOR_COST = [0, 13, 31, 53, 75, 102]
RING_COST = {
    ("d", 0): 0,
    ("d", 1): 25,
    ("d", 2): 50,
    ("d", 3): 100,
    ("a", 0): 0,
    ("a", 1): 20,
    ("a", 2): 40,
    ("a", 3): 80,
}

WEAPON_VALUES = [4, 5, 6, 7, 8]
ARMOR_VALUES = [0, 1, 2, 3, 4, 5]
RING_VALUES = [0, 1, 2, 3]


@dataclass
class Slots:
    weapon: int
    armor: int
    ring1: tuple[str, int]
    ring2: tuple[str, int]

    def cost(self):
        return (
            WEAPON_COST[self.weapon - 4]
            + ARMOR_COST[self.armor]
            + RING_COST[self.ring1]
            + RING_COST[self.ring2]
        )

    def make_character(self):
        return Character(
            100,
            self.weapon
            + (self.ring1[1] if self.ring1[0] == "d" else 0)
            + (self.ring2[1] if self.ring2[0] == "d" else 0),
            self.armor
            + (self.ring1[1] if self.ring1[0] == "a" else 0)
            + (self.ring2[1] if self.ring2[0] == "a" else 0),
        )


def simulate(boss: Character, player: Character) -> Literal["win", "loss"]:
    whos_turn = "p"
    while True:
        if boss.hp <= 0:
            return "win"
        if player.hp <= 0:
            return "loss"
        if whos_turn == "p":
            boss.hp -= max(player.hit - boss.armor, 1)
            # print(
            #    f"The player deals {player.hit - boss.armor=} damage;"
            #    " the boss goes down to {boss.hp} hit points"
            # )
            whos_turn = "b"
        else:
            player.hp -= max(boss.hit - player.armor, 1)
            # print(
            #    f"The boss deals {boss.hit - player.armor=} damage;"
            #    " the player goes down to {player.hp} hit points"
            # )
            whos_turn = "p"


if __name__ == "__main__":
    max_cost = 0
    for w, a, r1, r2 in product(
        WEAPON_VALUES,
        ARMOR_VALUES,
        product(["a", "d"], RING_VALUES),
        product(["a", "d"], RING_VALUES),
    ):
        if r1 == r2:
            continue
        slots = Slots(w, a, r1, r2)
        if simulate(Character(109, 8, 2), slots.make_character()) == "loss":
            cost = slots.cost()
            if cost > max_cost:
                max_cost = max(max_cost, cost)
    print(max_cost)
