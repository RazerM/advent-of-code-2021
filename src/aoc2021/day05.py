import re
from collections import defaultdict
from collections.abc import Iterable
from typing import IO

import attr
import numpy as np

from ._registry import register
from ._util import Vector


@attr.s(auto_attribs=True, frozen=True)
class Line:
    start: Vector
    end: Vector

    def walk(self) -> Iterable[Vector]:
        increment = Vector(
            np.sign(self.end.x - self.start.x),
            np.sign(self.end.y - self.start.y),
        )

        pos = self.start
        yield pos
        while pos != self.end:
            pos += increment
            yield pos

    @property
    def straight(self) -> bool:
        return self.horizontal or self.vertical

    @property
    def horizontal(self) -> bool:
        return self.start.y == self.end.y

    @property
    def vertical(self) -> bool:
        return self.start.x == self.end.x


def count_intersections(lines: list[Line]) -> int:
    grid: dict[tuple[int, int], int] = defaultdict(int)

    for line in lines:
        for pos in line.walk():
            grid[int(pos.y), int(pos.x)] += 1

    return sum(1 for value in grid.values() if value > 1)


@register(day=5)
def solve(file: IO[str], verbose: int) -> None:
    lines = []
    for line in file:
        if match := re.match(r"(\d+),(\d+)\s*->\s*(\d+),(\d+)", line):
            x1, y1, x2, y2 = map(int, match.groups())
            lines.append(Line(Vector(x1, y1), Vector(x2, y2)))

    straight_lines = [line for line in lines if line.straight]
    print("Part 1:", count_intersections(straight_lines))
    print("Part 2:", count_intersections(lines))
