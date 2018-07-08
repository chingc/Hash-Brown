"""Hash Brown CLI"""

from glob import iglob
from os.path import isfile

import click

from main import Checksum


@click.version_option(version="0.1.0")
@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-a", "--algorithm", type=click.Choice(Checksum.supported))
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
                    output += f" {click.style('OK', fg='green') if output.endswith(match) else click.style('BAD', fg='red')}"
                click.echo(output)
                computed += 1
        if not computed:
            click.echo(f"No files matched the pattern: '{file}'")
    elif check:
        pass
    else:
        pass

# @cli.command()  # type: ignore
# @click.option("-p", "--progress", is_flag=True, help="Display hashing progress.")
# @click.argument("path", required=True, type=click.Path(exists=True, dir_okay=False))
# def verify(path: str, progress: bool) -> None:
#     """Verify multiple hashes with a checksum file."""
#     good = 0
#     bad = 0
#     skip = 0
#     for algorithm, filepath, digest in hb.parse(path):
#         output = f"{algorithm} ({filepath}) = {digest} "
#         try:
#             computed = hb.compute(algorithm, filepath, show_progress=progress)
#         except FileNotFoundError:
#             click.echo(output + "SKIP: File not found")
#             skip += 1
#         except OSError:
#             click.echo(output + "SKIP: Unable to read file")
#             skip += 1
#         except ValueError as err:
#             click.echo(output + f"SKIP: {err}")
#             skip += 1
#         else:
#             if digest == computed:
#                 good += 1
#             else:
#                 click.echo(output + "BAD")
#                 bad += 1
#     click.echo(f"GOOD: {good}, BAD: {bad}, SKIP: {skip}")

if __name__ == "__main__":
    cli()
