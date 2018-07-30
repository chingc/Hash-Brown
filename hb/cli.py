"""Hash Brown CLI"""

from glob import iglob
from pathlib import Path
from time import time

import click

from hb.main import Checksum


def _is_match(checksum1: str, checksum2: str) -> bool:
    if checksum1.endswith(checksum2):
        return True
    return False

def _algorithm_mode(algorithm: str, path: str, given: str) -> None:
    computed = 0
    for filename in iglob(path, recursive=True):
        if Path(filename).is_file():
            try:
                actual = Checksum(filename).get(algorithm)
            except OSError as error:
                msg = str(error).partition("] ")[-1]
                output = f"{click.style(msg, fg='yellow')}"
            else:
                if given:
                    output = Checksum.print(algorithm, filename, given)
                    output += f" {click.style('OK', fg='green') if _is_match(actual, given) else click.style(f'ACTUAL: {actual}', fg='red')}"
                else:
                    output = Checksum.print(algorithm, filename, actual)
            click.echo(output)
            computed += 1
    if not computed:
        click.echo(f"No files matched the pattern: '{path}'")

def _check_mode(path: str) -> None:
    try:
        for algorithm, filename, given in Checksum.parse(path):
            output = Checksum.print(algorithm, filename, given)
            try:
                actual = Checksum(filename).get(algorithm)
            except OSError as error:
                msg = str(error).partition("] ")[-1]
                output += f" {click.style(msg, fg='yellow')}"
            else:
                result, color = ("OK", "green") if _is_match(actual, given) else (f"ACTUAL: {actual}", "red")
                output += f" {click.style(result, fg=color)}"
            click.echo(output)
    except (OSError, ValueError) as error:
        click.echo(f"Unable to read checksum file: {error}")

@click.version_option(version=Checksum.VERSION)
@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-a", "--algorithm", type=click.Choice(Checksum.SUPPORTED))
@click.option("-c", "--check", is_flag=True, help="Read checksums from a file.")
@click.option("-g", "--given", help="See if the given checksum `TEXT` matches the computed checksum. (use with -a)")
@click.option("-t", "--timer", is_flag=True, help="Display elapsed time.")
@click.argument("file")
def cli(algorithm: str, check: bool, given: str, file: str, timer: bool) -> None:
    """Hash Brown: Compute and verify checksums."""
    start_time = time()
    if algorithm:
        _algorithm_mode(algorithm, file, given)
    elif check:
        _check_mode(file)
    else:
        pass
    if timer:
        click.echo(f"# {time() - start_time:.3f}s")


if __name__ == "__main__":
    cli()
