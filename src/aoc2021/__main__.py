import datetime as dt
import os
import re
from pathlib import Path
from typing import IO

import click
import httpx
from dotenv import load_dotenv

from ._registry import solvers

INPUT_URL = "https://adventofcode.com/2021/day/{day}/input"


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli() -> None:
    pass


@cli.command()
@click.argument("day", type=click.IntRange(min=1, max=25))
@click.argument("file", type=click.File("x"))
def download(day: int, file: IO[str]) -> None:
    """Download input for DAY to FILE. Will not overwrite."""
    load_dotenv()
    try:
        cookies = dict(session=os.environ["AOC_SESSION"])
    except KeyError:
        raise click.UsageError(
            "Set AOC_SESSION environment variable (or add to .env file)"
        )
    response = httpx.get(INPUT_URL.format(day=day), cookies=cookies)
    response.raise_for_status()
    file.write(response.text)


verbose = click.option(
    "-v",
    "--verbose",
    count=True,
    help=(
        "Typically -v will print some progress information, -vvv may spam the "
        "screen with puzzle state."
    ),
)


@cli.command()
@click.argument("day", type=click.IntRange(min=1, max=25))
@click.argument("file", type=click.File("r"), default="-")
@verbose
def run(day: int, file: IO[str], verbose: int) -> None:
    """If FILE is not passed, stdin is used instead."""
    try:
        solve = solvers[day]
    except KeyError:
        raise click.UsageError("Unimplemented!")

    solve(file, verbose)


def default_day() -> int:
    today = dt.date.today()
    if today.year == 2021 and today.month == 12:
        day = today.day
    else:
        click.secho(
            "It's not december 2021, so I can't guess which day you want to run!",
            fg="yellow",
        )
        day = 25
    click.secho(f"Using day {day}", fg="green")
    return day


@cli.command()
@click.argument("day", type=click.IntRange(min=1, max=25), default=default_day)
@verbose
def autorun(day: int, verbose: int) -> None:
    try:
        solve = solvers[day]
    except KeyError:
        raise click.UsageError("Unimplemented!")

    input_path = f"input/{day:02d}.txt"
    try:
        file = open(input_path)
    except FileNotFoundError:
        raise click.UsageError(f"Input file does not exist: {input_path}")

    with file as fp:
        solve(fp, verbose)


MODULE_TEMPLATE = """\
from typing import IO

from ._registry import register


@register(day={day})
def solve(file: IO[str], verbose: int) -> None:
    pass
"""


@cli.command()
def prepare() -> None:
    load_dotenv()
    input_dir = Path("input")
    package_dir = Path(__file__).parent
    expected_src_dir = package_dir.parent
    expected_root_dir = expected_src_dir.parent

    try:
        Path.cwd().relative_to(expected_root_dir)
    except ValueError:
        click.secho(
            "Either aoc2021 is not an editable install, or you're running this "
            "command from outside the repository root. Skipping creation of "
            "dayXX.py files",
            fg="red",
        )
        create_modules = False
    else:
        create_modules = True

    last_available_day = min(dt.date.today(), dt.date(2021, 12, 25)).day

    try:
        aoc_session = os.environ["AOC_SESSION"]
    except KeyError:
        raise click.UsageError(
            "Set AOC_SESSION environment variable (or add to .env file)"
        )
    else:
        cookies = dict(session=aoc_session)

    with httpx.Client(cookies=cookies) as client:
        for day in range(1, last_available_day + 1):
            if create_modules:
                module_file = package_dir / f"day{day:02d}.py"
                try:
                    with open(module_file, "x") as file:
                        file.write(MODULE_TEMPLATE.format(day=day))
                except FileExistsError:
                    pass

            input_file = input_dir / f"{day:02d}.txt"
            try:
                with open(input_file, "x") as file:
                    response = client.get(INPUT_URL.format(day=day))
                    response.raise_for_status()
                    file.write(response.text)
            except FileExistsError:
                pass

    if create_modules:
        with open(package_dir / "__init__.py", "r+") as file:
            lines = file.readlines()
            output = []
            in_autogenerate = False

            for line in lines:
                if in_autogenerate:
                    if re.match(r"# autogenerate end", line):
                        output.append(line)
                        in_autogenerate = False
                    continue

                output.append(line)
                if re.match(r"# autogenerate start", line):
                    in_autogenerate = True
                    # This formatting is set up to match what isort will reformat
                    # it as.
                    output.append("from . import (\n")
                    for day in range(1, last_available_day + 1):
                        output.append(f"    day{day:02d},\n")
                    output.append(f")\n\n")

            file.seek(0)
            file.truncate()
            file.writelines(output)


if __name__ == "__main__":
    cli()
