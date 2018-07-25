"""Hash Brown CLI"""

from glob import iglob
from os.path import isfile

import click

from main import Checksum


def _is_match(checksum1: str, checksum2: str) -> bool:
    if checksum1.endswith(checksum2):
        return True
    return False

def _algorithm_mode(algorithm: str, file: str, given: str) -> None:
    computed = 0
    for filename in iglob(file, recursive=True):
        if isfile(filename):
            actual = Checksum(filename).get(algorithm)
            if given:
                output = Checksum.print(algorithm, filename, given)
                output += f" {click.style('OK', fg='green') if _is_match(actual, given) else click.style(f'ACTUAL: {actual}', fg='red')}"
            else:
                output = Checksum.print(algorithm, filename, actual)
            click.echo(output)
            computed += 1
    if not computed:
        click.echo(f"No files matched the pattern: '{file}'")

def _check_mode(file: str) -> None:
    try:
        for algorithm, filename, given in Checksum.parse(file):
            output = Checksum.print(algorithm, filename, given)
            try:
                actual = Checksum(filename).get(algorithm)
            except FileNotFoundError:
                output += f" {click.style('SKIP: File not found', fg='yellow')}"
            except OSError:
                output += f" {click.style('SKIP: Unable to read', fg='yellow')}"
            else:
                output += f" {click.style('OK', fg='green') if _is_match(actual, given) else click.style(f'ACTUAL: {actual}', fg='red')}"
            click.echo(output)
    except (OSError, ValueError) as error:
        click.echo(error)  # type: ignore

@click.version_option(version="1.1.0")
@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-a", "--algorithm", type=click.Choice(Checksum.supported))
@click.option("-c", "--check", is_flag=True, help="Read checksums from a file.")
@click.option("-g", "--given", help="See if the given checksum `TEXT` matches the computed checksum. (use with -a)")
@click.argument("file")
def cli(algorithm: str, check: str, given: str, file: str) -> None:
    """Hash Brown: Compute and verify checksums."""
    if algorithm:
        _algorithm_mode(algorithm, file, given)
    elif check:
        _check_mode(file)
    else:
        pass

if __name__ == "__main__":
    cli()
