from collections import defaultdict, deque
from collections.abc import Iterable
from typing import IO, TypeAlias

from ._registry import register

Graph: TypeAlias = dict[str, set[str]]
State: TypeAlias = tuple[str, set[str], list[str], bool]


def explore(
    nodes: Graph,
    *,
    source: str,
    target: str,
    allow_one_double_visit: bool = False,
) -> Iterable[list[str]]:
    path = [source]
    visited = {source}

    states: deque[State] = deque([(source, visited, path, False)])
    while states:
        source, visited, path, double_visit_used = states.popleft()
        if source.islower():
            visited.add(source)

        for adjacent in nodes[source]:
            new_path = [*path, adjacent]

            if adjacent == target:
                yield new_path
            else:
                if adjacent in visited:
                    if (
                        allow_one_double_visit
                        and not double_visit_used
                        and adjacent not in {"start", "end"}
                    ):
                        states.append(
                            (adjacent, visited.difference(adjacent), new_path, True)
                        )
                    continue

                states.append((adjacent, visited.copy(), new_path, double_visit_used))


@register(day=12)
def solve(file: IO[str], verbose: int) -> None:

    nodes: Graph = defaultdict(set)
    for line in file:
        a, b = line.strip().split("-")
        nodes[a].add(b)
        nodes[b].add(a)

    part1 = explore(nodes, source="start", target="end")
    part2 = explore(nodes, source="start", target="end", allow_one_double_visit=True)

    if verbose:
        part1 = list(part1)
        for path in part1:
            print(",".join(path))

    print("Part 1:", sum(1 for _ in part1))

    if verbose:
        part2 = list(part2)
        for path in part2:
            print(",".join(path))

    print("Part 2:", sum(1 for _ in part2))
