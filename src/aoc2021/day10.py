import statistics
from collections import deque
from typing import IO

from ._registry import register

error_points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

completion_points = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

closing = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


@register(day=10)
def solve(file: IO[str], verbose: int) -> None:
    lines = [line.strip() for line in file]

    syntax_error_score = 0
    completion_scores: list[int] = []
    for line in lines:
        if verbose:
            print(line, end=" - ")
        valid = True
        unclosed: deque[str] = deque()
        for char in line:
            match char:
                case "(" | "[" | "{" | "<":
                    unclosed.append(closing[char])
                case ")" | "]" | "}" | ">":
                    expected = unclosed.pop()
                    if expected != char:
                        valid = False
                        syntax_error_score += error_points[char]
                        break
                case char:
                    raise ValueError(f"Unexpected character: {char}")

        if valid:
            if unclosed:
                completion_score = 0
                completion_str = ""
                while unclosed:
                    close_char = unclosed.pop()
                    completion_str += close_char
                    completion_score *= 5
                    completion_score += completion_points[close_char]
                completion_scores.append(completion_score)
                if verbose:
                    print("incomplete", completion_str)
            else:
                if verbose:
                    print("valid")
        else:
            if verbose:
                print("invalid")

    print("Part 1:", syntax_error_score)
    print("Part 2:", statistics.median(sorted(completion_scores)))
