from collections import Counter
from typing import IO

from ._registry import register


def estimate_population(fish: list[int], days: int) -> int:
    fish_counts = dict.fromkeys(range(9), 0)
    fish_counts.update(Counter(fish))

    for day in range(days):
        new_counts = dict.fromkeys(range(9), 0)
        for timer, num in fish_counts.items():
            if timer == 0:
                new_counts[6] += num
                new_counts[8] += num
            else:
                new_counts[timer - 1] += num

        fish_counts = new_counts

    return sum(fish_counts.values())


@register(day=6)
def solve(file: IO[str], verbose: int) -> None:
    fish = list(map(int, file.read().strip().split(",")))

    print("Part 1:", estimate_population(fish, 80))
    print("Part 2:", estimate_population(fish, 256))
