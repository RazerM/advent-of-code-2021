import math
from typing import IO

from ._registry import register


@register(day=7)
def solve(file: IO[str], verbose: int) -> None:
    positions = list(map(int, file.read().strip().split(",")))
    human_engineering = dict()
    crab_engineering = dict()
    for value in range(min(positions), max(positions) + 1):
        human_engineering[value] = sum(abs(p - value) for p in positions)
        crab_engineering[value] = sum(
            math.comb(abs(p - value) + 1, 2) for p in positions
        )

    print("Part 1:", min(human_engineering.values()))
    print("Part 2:", min(crab_engineering.values()))
