"""Hash Brown CLI"""

import os.path
from glob import iglob
from typing import List

import click

import main as hb


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(version="0.1.0")
def cli() -> None:
    """Hash Brown: Compute and verify hashes."""
    pass

@cli.command()  # type: ignore
@click.option("-a", "--algorithm", required=True, type=click.Choice(hb.HASHLIBS + hb.ZLIBS))
@click.option("-p", "--progress", is_flag=True, help="Display hashing progress.")
@click.argument("paths", required=True, nargs=-1, type=click.Path())
def compute(algorithm: str, paths: List[str], progress: bool) -> None:
    """Compute a hash."""
    count = 0
    for path in paths:
        for filename in iglob(path, recursive=True):
            if os.path.isfile(filename):
                click.echo(f"{algorithm} ({filename}) = {hb.compute(algorithm, filename, show_progress=progress)}")
                count += 1
        if not count:
            click.echo(f"Error: No files matched the pattern: '{path}'")
        count = 0

@cli.command()  # type: ignore
@click.option("-a", "--algorithm", required=True, type=click.Choice(hb.HASHLIBS + hb.ZLIBS))
@click.option("-p", "--progress", is_flag=True, help="Display hashing progress.")
@click.argument("path", required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument("digest", required=True)
def single(algorithm: str, path: str, digest: str, progress: bool) -> None:
    """Verify a single hash on the command line."""
    click.echo(f"{algorithm} ({path}) = {digest} {'OK' if digest == hb.compute(algorithm, path, show_progress=progress) else 'BAD'}")

@cli.command()  # type: ignore
@click.option("-p", "--progress", is_flag=True, help="Display hashing progress.")
@click.argument("path", required=True, type=click.Path(exists=True, dir_okay=False))
def verify(path: str, progress: bool) -> None:
    """Verify multiple hashes with a checksum file."""
    good = 0
    bad = 0
    skip = 0
    if not hb.parsable(path):
        click.echo("Error: Checksum file contains bad formatting")
    else:
        for algorithm, filepath, digest in hb.parse(path):
            output = f"{algorithm} ({filepath}) = {digest} "
            try:
                computed = hb.compute(algorithm, filepath, show_progress=progress)
            except FileNotFoundError:
                click.echo(output + "SKIP: File not found")
                skip += 1
            except OSError:
                click.echo(output + "SKIP: Unable to read file")
                skip += 1
            except ValueError as err:
                click.echo(output + f"SKIP: {err}")
                skip += 1
            else:
                if digest == computed:
                    good += 1
                else:
                    click.echo(output + "BAD")
                    bad += 1
        click.echo(f"GOOD: {good}, BAD: {bad}, SKIP: {skip}")

if __name__ == "__main__":
    cli()
