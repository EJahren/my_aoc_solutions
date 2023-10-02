import math
import sys
from dataclasses import astuple, dataclass
from typing import Self


@dataclass
class Raindeer:
    name: str
    speed: int
    max_movement: int
    rest_time: int
    travelled: int = 0
    flying: bool = True
    exhaustion: int = 0
    points: int = 0

    @property
    def resting(self):
        return not self.flying

    @classmethod
    def parse(cls, line: str) -> Self:
        words = line.split()
        return cls(words[0], int(words[3]), int(words[6]), int(words[-2]))


def test_rainder_parse():
    assert Raindeer.parse(
        "Rudolph can fly 22 km/s for 8 seconds, but then must rest for 165 seconds."
    ) == Raindeer(name="Rudolph", speed=22, max_movement=8, rest_time=165)


def simulate_travel(raindeers: list[Raindeer]):
    for r in raindeers:
        if r.flying:
            if r.exhaustion >= r.max_movement:
                r.flying = False
                r.exhaustion = r.rest_time
            else:
                r.travelled += r.speed
                r.exhaustion += 1
        else:
            r.exhaustion -= 1
            if r.exhaustion <= 1:
                r.flying = True
                r.exhaustion = 0
    max_travelled = max(r.travelled for r in raindeers)
    for r in raindeers:
        if r.travelled == max_travelled:
            r.points += 1


def test_simulate_travel():
    raindeers = [
        Raindeer.parse(
            "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds"
        ),
        Raindeer.parse(
            "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."
        ),
    ]
    seconds = 1
    simulate_travel(raindeers)
    seconds += 1
    assert raindeers[0].travelled == 14
    assert raindeers[1].travelled == 16
    while seconds <= 10:
        simulate_travel(raindeers)
        seconds += 1
    assert raindeers[0].travelled == 140
    assert raindeers[0].flying
    assert raindeers[1].travelled == 160
    assert raindeers[1].flying
    simulate_travel(raindeers)
    seconds += 1
    assert raindeers[0].resting
    assert raindeers[0].travelled == 140
    assert raindeers[1].flying
    assert raindeers[1].travelled == 176
    simulate_travel(raindeers)
    seconds += 1
    assert raindeers[0].resting
    assert raindeers[0].travelled == 140
    assert raindeers[1].resting
    assert raindeers[1].travelled == 176
    while seconds <= 138:
        simulate_travel(raindeers)
        seconds += 1
    assert raindeers[0].flying

    while seconds <= 1000:
        simulate_travel(raindeers)
        seconds += 1
    assert raindeers[0].resting
    assert raindeers[0].travelled == 1120
    assert raindeers[1].resting
    assert raindeers[1].travelled == 1056
    assert raindeers[0].points == 312
    assert raindeers[1].points == 689


def find_max_points(inp: list[Raindeer]) -> int:
    for _ in range(2503):
        simulate_travel(inp)
    return max(r.points for r in inp)


if __name__ == "__main__":
    print(find_max_points([Raindeer.parse(l) for l in sys.stdin]))
