from collections import Counter, deque
from typing import IO, Iterable

from ._registry import register


def pairs(s: str) -> Iterable[str]:
    for i in range(1, len(s)):
        yield s[i - 1 : i + 1]


def optimal_polymer(
    template: str, pair_insertion_rules: dict[str, str], *, steps: int
) -> int:
    polymer = Counter(pairs(template))
    elements = Counter(template)

    # precompute the affected pairs for each rule
    replacements: list[tuple[str, str, str, str]] = []
    for old, element in pair_insertion_rules.items():
        pair1 = old[0] + element
        pair2 = element + old[1]
        replacements.append((old, element, pair1, pair2))

    for step in range(steps):
        changes: Counter[str] = Counter()
        for old, element, pair1, pair2 in replacements:
            if old in polymer:
                count = polymer[old]
                changes[old] -= count
                changes[pair1] += count
                changes[pair2] += count
                elements[element] += count

        polymer += changes

    most_common, *_, least_common = elements.most_common()
    return most_common[1] - least_common[1]


@register(day=14)
def solve(file: IO[str], verbose: int) -> None:
    template = file.readline().strip()

    pair_insertion_rules: dict[str, str] = dict()

    for line in file:
        line = line.strip()
        if not line:
            continue

        key, value = line.split(" -> ")
        pair_insertion_rules[key] = value

    print("Part 1:", optimal_polymer(template, pair_insertion_rules, steps=10))
    print("Part 2:", optimal_polymer(template, pair_insertion_rules, steps=40))
