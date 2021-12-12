import math
from typing import IO, TypeVar

import numpy as np
from numpy.typing import NDArray

from ._registry import register

NDArrayBool = NDArray[np.bool_]
DT = TypeVar("DT", bound=np.generic)


def most_common_by_col(a: NDArrayBool) -> NDArrayBool:
    summed = np.sum(a, axis=0)
    half = a.shape[0] // 2
    return summed >= half


def least_common_by_col(a: NDArrayBool) -> NDArrayBool:
    summed = np.sum(a, axis=0)
    half = a.shape[0] // 2
    return summed <= half


def least_common(a: NDArray[DT]) -> DT:
    values, counts = np.unique(a, return_counts=True)
    ind = np.argmin(counts)
    return values[ind]


def gamma_rate(a: NDArrayBool) -> int:
    return bits_to_int(most_common_by_col(a))


def epsilon_rate(a: NDArrayBool) -> int:
    return bits_to_int(least_common_by_col(a))


def bits_to_int(a: NDArrayBool) -> int:
    s = "".join(map(str, a.astype(int)))
    return int(s, 2)


def oxygen_generator_rating(a: NDArrayBool) -> int:
    col = 0
    b = a.copy()
    while b.shape[0] > 1:
        keep_mask = b[:, col] == ~least_common(b[:, col])
        b = b[keep_mask, :]
        col += 1
    return bits_to_int(b[0])


def co2_scrubber_rating(a: NDArrayBool) -> int:
    col = 0
    b = a.copy()
    while b.shape[0] > 1:
        keep_mask = b[:, col] == least_common(b[:, col])
        b = b[keep_mask, :]
        col += 1
    return bits_to_int(b[0])


def life_support_rating(a: NDArrayBool) -> int:
    return oxygen_generator_rating(a) * co2_scrubber_rating(a)


@register(day=3)
def solve(file: IO[str], verbose: int) -> None:
    a = np.array([list(map(int, line.strip())) for line in file], dtype=bool)
    print("Part 1:", gamma_rate(a) * epsilon_rate(a))
    print("Part 2:", life_support_rating(a))
