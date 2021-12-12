from collections.abc import Iterable
from typing import IO

from more_itertools import sliding_window

from ._registry import register


def count_increases(it: Iterable[int]) -> int:
    return sum(b > a for a, b in sliding_window(it, 2))


@register(day=1)
def solve(file: IO[str], verbose: int) -> None:
    depths = [int(line.strip()) for line in file]

    print("Part 1:", count_increases(depths))
    print("Part 2:", count_increases(map(sum, sliding_window(depths, 3))))
