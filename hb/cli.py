"""Hash Brown CLI"""

from concurrent.futures import ProcessPoolExecutor
from glob import iglob
from pathlib import Path
from time import time
from typing import Any, Tuple

import click

from hb.main import Checksum


def _shorten(error: Exception) -> str:
    msg = str(error)
    return msg.partition("] ")[-1] if "] " in msg else msg

def _compute(algorithm: str, path: str, given: str) -> Tuple[int, str]:
    try:
        actual = Checksum(path).get(algorithm)
    except OSError as error:
        return (2, f"{click.style(_shorten(error), fg='yellow')}")
    else:
        if given:
            if actual == given:
                return (0, f"{Checksum.print(algorithm, path, given)} {click.style('OK', fg='green')}")
            return (1, f"{Checksum.print(algorithm, path, given)} {click.style(f'BAD', fg='red')}")
        return (0, Checksum.print(algorithm, path, actual))

def _algorithm_mode(algorithm: str, path: str, given: str, parallel: bool) -> None:
    computed = 0
    with ProcessPoolExecutor(max_workers=None if parallel else 1) as executor:
        for filename in iglob(path, recursive=True):
            if not Path(filename).is_file():
                continue
            future = executor.submit(_compute, algorithm, filename, given)
            future.add_done_callback(lambda f: click.echo(f.result()[1]))
            computed += 1
    if not computed:
        click.echo(f"No files matched the pattern: '{path}'")

def _check_mode(path: str, quiet: bool, parallel: bool) -> None:
    def _cb(code: int, result: str) -> None:
        if not quiet:
            click.echo(result)
        elif code:
            click.echo(result)
    with ProcessPoolExecutor(max_workers=None if parallel else 1) as executor:
        for algorithm, filename, given in Checksum.parse(path):
            future = executor.submit(_compute, algorithm, filename, given)
            future.add_done_callback(lambda f: _cb(f.result()[0], f.result()[1]))


@click.version_option(version=Checksum.VERSION)
@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-a", "--algorithm", type=click.Choice(Checksum.SUPPORTED))
@click.option("-c", "--check", is_flag=True, help="Read checksums from a file.")
@click.option("-g", "--given", help="See if the given checksum `TEXT` matches the computed checksum. (use with -a)")
@click.option("-p", "--parallel", is_flag=True, default=False, help="Process files in parallel.")
@click.option("-q", "--quiet", is_flag=True, default=False, help="Hide results that are OK. (use with -c)")
@click.option("-t", "--timer", is_flag=True, help="Display elapsed time in seconds.")
@click.argument("path")
def cli(**kwargs: Any) -> None:
    """Hash Brown: Compute and verify checksums."""
    start_time = time()
    try:
        if kwargs["algorithm"]:
            _algorithm_mode(**{k: v for k, v in kwargs.items() if k in ["algorithm", "path", "given", "parallel"]})
        elif kwargs["check"]:
            _check_mode(**{k: v for k, v in kwargs.items() if k in ["path", "quiet", "parallel"]})
        else:
            pass
    except (OSError, ValueError) as error:
        click.echo(_shorten(error))
    if kwargs["timer"]:
        click.echo(f"# {time() - start_time:.3f}s")


if __name__ == "__main__":
    cli()
