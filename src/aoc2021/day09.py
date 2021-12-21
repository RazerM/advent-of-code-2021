import math
from collections import deque
from collections.abc import Iterable
from typing import IO

from ._registry import register


def adjacent(grid: list[list[int]], x: int, y: int) -> Iterable[tuple[int, int]]:
    if x > 0:
        yield x - 1, y
    if x < len(grid[0]) - 1:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y < len(grid) - 1:
        yield x, y + 1


def adjacent_cells(grid: list[list[int]], x: int, y: int) -> Iterable[int]:
    for x, y in adjacent(grid, x, y):
        yield grid[y][x]


@register(day=9)
def solve(file: IO[str], verbose: int) -> None:
    grid: list[list[int]] = []
    for line in file:
        grid.append(list(map(int, line.strip())))

    risk_sum = 0
    low_points: list[tuple[int, int]] = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell < min(adjacent_cells(grid, x, y)):
                risk_level = cell + 1
                risk_sum += risk_level
                low_points.append((x, y))

    print("Part 1:", risk_sum)

    basins: list[int] = []
    for x, y in low_points:
        size = 0
        visited: set[tuple[int, int]] = set()
        queue = deque([(x, y)])

        while queue:
            px, py = queue.popleft()
            if (px, py) in visited:
                continue
            visited.add((px, py))
            height = grid[py][px]
            if height < 9:
                size += 1
                queue.extend(adjacent(grid, px, py))
        basins.append(size)

    print("Part 2:", math.prod(sorted(basins)[-3:]))
