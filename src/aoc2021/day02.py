from typing import IO

from ._registry import register


def part1(commands: list[tuple[str, int]]) -> int:
    pos = depth = 0

    for command, n in commands:
        match command:
            case "forward":
                pos += n
            case "down":
                depth += n
            case "up":
                depth -= n

    return pos * depth


def part2(commands: list[tuple[str, int]]) -> int:
    aim = pos = depth = 0

    for command, n in commands:
        match command:
            case "forward":
                pos += n
                depth += aim * n
            case "down":
                aim += n
            case "up":
                aim -= n

    return pos * depth


@register(day=2)
def solve(file: IO[str], verbose: int) -> None:
    commands = []
    for line in file:
        command, n = line.strip().split()
        commands.append((command, int(n)))

    print("Part 1:", part1(commands))
    print("Part 2:", part2(commands))
