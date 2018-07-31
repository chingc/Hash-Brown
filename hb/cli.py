"""Hash Brown CLI"""

from glob import iglob
from pathlib import Path
from time import time
from typing import Tuple

import click

from main import Checksum


def _shorten(error: Exception) -> str:
    return str(error).partition("] ")[-1]

def _compute(algorithm: str, path: str, given: str) -> Tuple[int, str]:
    try:
        actual = Checksum(path).get(algorithm)
    except OSError as error:
        return (2, f"{click.style(_shorten(error), fg='yellow')}")
    else:
        if given:
            if actual == given:
                return (0, f"{Checksum.print(algorithm, path, given)} {click.style('OK', fg='green')}")
            return (1, f"{Checksum.print(algorithm, path, given)} {click.style(f'ACTUAL: {actual}', fg='red')}")
        return (0, Checksum.print(algorithm, path, actual))

def _algorithm_mode(algorithm: str, path: str, given: str) -> None:
    computed = 0
    for filename in iglob(path, recursive=True):
        if not Path(filename).is_file():
            continue
        click.echo(_compute(algorithm, filename, given)[1])
        computed += 1
    if not computed:
        click.echo(f"No files matched the pattern: '{path}'")

def _check_mode(path: str) -> None:
    codes = {k: 0 for k in [0, 1, 2]}
    for algorithm, filename, given in Checksum.parse(path):
        code, result = _compute(algorithm, filename, given)
        codes[code] += 1
        if code:
            click.echo(result)
    click.secho(f"OK: {codes[0]}", fg="green")
    if codes[1]:
        click.secho(f"BAD: {codes[1]}", fg="red")
    if codes[2]:
        click.secho(f"SKIP: {codes[2]}", fg="yellow")


@click.version_option(version=Checksum.VERSION)
@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-a", "--algorithm", type=click.Choice(Checksum.SUPPORTED))
@click.option("-c", "--check", is_flag=True, help="Read checksums from a file.")
@click.option("-g", "--given", help="See if the given checksum `TEXT` matches the computed checksum. (use with -a)")
@click.option("-t", "--timer", is_flag=True, help="Display elapsed time in seconds.")
@click.argument("file")
def cli(**kwargs: str) -> None:
    """Hash Brown: Compute and verify checksums."""
    start_time = time()
    try:
        if kwargs["algorithm"]:
            _algorithm_mode(kwargs["algorithm"], kwargs["file"], kwargs["given"])
        elif kwargs["check"]:
            _check_mode(kwargs["file"])
        else:
            pass
    except (OSError, ValueError) as error:
        click.echo(_shorten(error))
    if kwargs["timer"]:
        click.echo(f"# {time() - start_time:.3f}s")


if __name__ == "__main__":
    cli()
