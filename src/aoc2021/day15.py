# This implementation is largely based off of
# https://www.redblobgames.com/pathfinding/a-star/implementation.html
#
# Copyright 2014 Red Blob Games <redblobgames@gmail.com>
# SPDX-License-Identifer: Apache-2.0
import heapq
from collections.abc import Iterable
from typing import IO, Callable, Generic, Protocol, TypeAlias, TypeVar

from ._registry import register

Location = TypeVar("Location")
T = TypeVar("T")


class Graph(Protocol[Location]):
    def neighbours(self, id: Location) -> Iterable[Location]:
        ...


class WeightedGraph(Graph[Location], Protocol):
    def cost(self, from_id: Location, to_id: Location) -> float:
        ...


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self.elements: list[tuple[float, T]] = []

    def __bool__(self) -> bool:
        return bool(self.elements)

    def put(self, item: T, priority: float) -> None:
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


def a_star_search(
    graph: WeightedGraph[Location],
    start: Location,
    goal: Location,
    heuristic: Callable[[Location, Location], float],
) -> tuple[dict[Location, Location | None], dict[Location, float]]:
    frontier: PriorityQueue[Location] = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Location | None] = dict()
    cost_so_far: dict[Location, float] = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = frontier.get()

        if current == goal:
            break

        for next_ in graph.neighbours(current):
            new_cost = cost_so_far[current] + graph.cost(current, next_)
            if next_ not in cost_so_far or new_cost < cost_so_far[next_]:
                cost_so_far[next_] = new_cost
                priority = new_cost + heuristic(next_, goal)
                frontier.put(next_, priority)
                came_from[next_] = current

    return came_from, cost_so_far


def reconstruct_path(
    came_from: dict[Location, Location], start: Location, goal: Location
) -> list[Location]:
    current: Location = goal
    path: list[Location] = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


GridLocation: TypeAlias = tuple[int, int]


def grid_heuristic(a: GridLocation, b: GridLocation) -> float:
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


class Grid:
    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid

    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)

    def in_bounds(self, id: GridLocation) -> bool:
        x, y = id
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbours(self, id: GridLocation) -> Iterable[GridLocation]:
        x, y = id
        neighbours = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]

        # "Ugly Paths" fix
        if (x + y) % 2 == 0:
            neighbours.reverse()

        for id in neighbours:
            if self.in_bounds(id):
                yield id

    def cost(self, from_id: GridLocation, to_id: GridLocation) -> float:
        x, y = to_id
        return self.grid[y][x]

    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self.grid)


def expand(i: int, n: int) -> int:
    n += i
    if n > 9:
        n = n % 9
    return n


class kylo_ren_more:
    @staticmethod
    def gif(grid: Grid) -> Grid:
        return Grid(
            [
                [expand(x + y, n) for x in range(5) for n in row]
                for y in range(0, 5)
                for row in grid.grid
            ]
        )


def top_left_to_bottom_right_risk(grid: Grid) -> float:
    start = (0, 0)
    goal = (grid.width - 1, grid.height - 1)
    _, cost_so_far = a_star_search(
        grid, start=start, goal=goal, heuristic=grid_heuristic
    )
    return cost_so_far[goal]


@register(day=15)
def solve(file: IO[str], verbose: int) -> None:
    grid = Grid([[int(c) for c in line.strip()] for line in file])
    print("Part 1:", top_left_to_bottom_right_risk(grid))

    full_grid = kylo_ren_more.gif(grid)
    print("Part 2:", top_left_to_bottom_right_risk(full_grid))
