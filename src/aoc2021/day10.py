from typing import IO

from ._registry import register


@register(day=10)
def solve(file: IO[str], verbose: int) -> None:
    pass