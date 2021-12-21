from collections import defaultdict
from typing import IO, Callable, TypeAlias

from ._registry import register

SignalPattern: TypeAlias = set[str]

normal_segments_map = {
    0: set("abcefg"),
    1: set("cf"),
    2: set("acdeg"),
    3: set("acdfg"),
    4: set("bcdf"),
    5: set("abdfg"),
    6: set("abdefg"),
    7: set("acf"),
    8: set("abcdefg"),
    9: set("abcdfg"),
}


def parse(line: str) -> tuple[list[SignalPattern], list[str]]:
    raw_patterns, raw_output = line.strip().split(" | ")
    patterns = [set(pattern) for pattern in raw_patterns.split()]
    output = ["".join(sorted(signal)) for signal in raw_output.split()]
    return patterns, output


@register(day=8)
def solve(file: IO[str], verbose: int) -> None:
    displays = [parse(line) for line in file]

    digits_by_num_segments: dict[int, set[int]] = defaultdict(set)
    for digit, segments in normal_segments_map.items():
        digits_by_num_segments[len(segments)].add(digit)
    digits_by_num_segments = dict(digits_by_num_segments)

    unique_by_length = {
        next(iter(digits))
        for num_segments, digits in digits_by_num_segments.items()
        if len(digits) == 1
    }

    output_sum = 0
    appearances_1478 = 0

    for signal_patterns, output in displays:

        def find(f: Callable[[SignalPattern], bool]) -> SignalPattern:
            # unpack like this to assert there's only one result!
            (result,) = (s for s in signal_patterns if f(s))
            return result

        results: dict[int, SignalPattern] = dict()
        for digit in unique_by_length:
            normal_segments = normal_segments_map[digit]
            results[digit] = next(
                s for s in signal_patterns if len(s) == len(normal_segments)
            )

        results[6] = find(lambda s: len(s) == 6 and len(results[1] & s) == 1)
        results[5] = find(lambda s: len(s) == 5 and results[6] & s == s)
        results[3] = find(lambda s: len(s) == 5 and len(results[1] & s) == 2)
        results[9] = find(lambda s: len(s) == 6 and len(results[4] & s) == 4)
        results[0] = find(lambda s: len(s) == 6 and s != results[9] and s != results[6])
        results[2] = find(lambda s: len(s) == 5 and s != results[3] and s != results[5])

        lookup = {"".join(sorted(s)): digit for digit, s in results.items()}

        output_str = ""
        for key in output:
            digit = lookup[key]
            appearances_1478 += digit in [1, 4, 7, 8]
            output_str += str(digit)
        output_num = int(output_str)
        output_sum += output_num

    print("Part 1:", appearances_1478)
    print("Part 2:", output_sum)
