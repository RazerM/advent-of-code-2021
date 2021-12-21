import re
from typing import IO, TypeAlias

from ._registry import register

Grid: TypeAlias = set[tuple[int, int]]
Fold: TypeAlias = tuple[str, int]


def apply_fold(grid: Grid, fold: Fold) -> Grid:
    axis, pos = fold
    applied = set()
    for x, y in grid:
        if axis == "y" and y > pos:
            applied.add((x, 2 * pos - y))
        elif axis == "x" and x > pos:
            applied.add((2 * pos - x, y))
        else:
            applied.add((x, y))

    return applied


def draw_grid(grid: Grid) -> None:
    xmax = max(x for x, _ in grid)
    ymax = max(y for _, y in grid)

    for y in range(ymax + 1):
        for x in range(xmax + 1):
            print("█" if (x, y) in grid else " ", end="")
        print()


@register(day=13)
def solve(file: IO[str], verbose: int) -> None:
    grid: Grid = set()
    folds: list[Fold] = []

    for line in file:
        line = line.strip()
        if not line:
            break

        x, y = map(int, line.split(","))
        grid.add((x, y))

    for line in file:
        if match := re.match(r"fold along ([xy])=(\d+)", line):
            axis = match.group(1)
            pos = int(match.group(2))
            folds.append((axis, pos))

    for i, fold in enumerate(folds):
        if i == 1:
            print("Part 1:", len(grid))
        grid = apply_fold(grid, fold)

    print("Part 2:")
    draw_grid(grid)
