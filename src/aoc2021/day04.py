from collections.abc import Iterable
from itertools import islice
from typing import IO, cast

import numpy as np
from numpy.typing import NDArray

from ._registry import register

NDArrayInt = NDArray[np.int_]


class BingoBoard:
    _bingos: list[set[int]]
    _all: set[int]
    finished: bool = False

    def __init__(self, board: NDArrayInt):
        self._bingos = [
            *(set(row) for row in board),
            *(set(col) for col in board.T),
        ]
        self._all = set(cast(Iterable[int], board.flat))

    def check(self, num: int) -> bool:
        self._all.discard(num)
        for b in self._bingos:
            b.discard(num)
            if not b:
                self.finished = True
                return True

        return False

    @property
    def score(self) -> int:
        return sum(self._all)


def read_input(file: IO[str]) -> tuple[list[int], list[BingoBoard]]:
    order = list(map(int, file.readline().strip().split(",")))

    boards: list[BingoBoard] = []

    while True:
        file.readline()
        board = np.array(
            [list(map(int, line.strip().split())) for line in islice(file, 5)]
        )
        if not board.size:
            break
        boards.append(BingoBoard(board))

    return order, boards


@register(day=4)
def solve(file: IO[str], verbose: int) -> None:
    order, boards = read_input(file)

    first_score = None
    last_score = None

    for i, num in enumerate(order):
        for board in boards:
            if board.finished:
                continue

            if board.check(num):
                last_score = num * board.score
                if first_score is None:
                    first_score = last_score

    print("Part 1:", first_score)
    print("Part 2:", last_score)
