"""Hash Brown CLI"""

from glob import iglob
from os.path import isfile

import click

from main import Checksum


def _compare(actual: str, expected: str):
    if actual.endswith(expected):
        return click.style("OK", fg="green")
    return click.style(f"ACTUAL: {expected}", fg="red")

@click.version_option(version="0.1.0")
@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-a", "--algorithm", type=click.Choice(Checksum.supported.split(" ")))
@click.option("-c", "--check", is_flag=True, help="Read checksums from `FILE` and check them.")
@click.option("-m", "--match", help="See if the checksum `TEXT` matches the computed checksum. (use with -a)")
@click.argument("file")
def cli(algorithm: str, check: str, match: str, file: str) -> None:
    """Hash Brown: Compute and verify checksums."""
    if algorithm:
        computed = 0
        for filename in iglob(file, recursive=True):
            if isfile(filename):
                output = Checksum(filename).print(algorithm)
                if match:
                    output = f"{algorithm} ({filename}) = {match}"
                    output += f" {_compare(output, match)}"
                click.echo(output)
                computed += 1
        if not computed:
            click.echo(f"No files matched the pattern: '{file}'")
    elif check:
        try:
            for algorithm, path, checksum in Checksum.parse(file):
                output = f"{algorithm} ({path}) = {checksum}"
                try:
                    checksum = Checksum(path).compute(algorithm)
                except FileNotFoundError:
                    output += f" {click.style('SKIP: File not found', fg='yellow')}"
                except OSError:
                    output += f" {click.style('SKIP: Unable to read', fg='yellow')}"
                else:
                    output += f" {_compare(output, checksum)}"
                click.echo(output)
        except (OSError, ValueError) as error:
            click.echo(error)
    else:
        pass

if __name__ == "__main__":
    cli()
