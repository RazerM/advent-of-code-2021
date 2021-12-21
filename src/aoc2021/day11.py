from collections import deque
from itertools import count, product
from typing import IO, Iterable

from ._registry import register


def adjacent(grid: list[list[int]], x: int, y: int) -> Iterable[tuple[int, int]]:
    neighbours = product([-1, 0, 1], [-1, 0, 1])
    width = len(grid[0])
    height = len(grid)

    for dx, dy in neighbours:
        if dx == dy == 0:
            continue
        nx = x + dx
        ny = y + dy

        if 0 <= nx < width and 0 <= ny < height:
            yield nx, ny


@register(day=11)
def solve(file: IO[str], verbose: int) -> None:
    grid: list[list[int]] = []
    for line in file:
        grid.append(list(map(int, line.strip())))

    flashes_after_step_100 = 0
    first_simultaneous_flash_step = None
    for step in count():
        flash_queue: deque[tuple[int, int]] = deque()
        for y, row in enumerate(grid):
            for x, energy in enumerate(row):
                grid[y][x] = energy + 1
                if grid[y][x] > 9:
                    flash_queue.append((x, y))

        flashed: set[tuple[int, int]] = set()

        while flash_queue:
            x, y = flash_queue.pop()
            if (x, y) in flashed:
                continue

            if step < 100:
                flashes_after_step_100 += 1
            flashed.add((x, y))
            for nx, ny in adjacent(grid, x, y):
                grid[ny][nx] += 1
                if grid[ny][nx] > 9:
                    flash_queue.append((nx, ny))

        for x, y in flashed:
            grid[y][x] = 0

        if len(flashed) == len(grid) * len(grid[0]):
            first_simultaneous_flash_step = step + 1
            break

    print("Part 1:", flashes_after_step_100)
    print("Part 2:", first_simultaneous_flash_step)
