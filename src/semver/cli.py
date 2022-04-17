import sys

import click

from .exc import ParseException
from .operations import clean_and_parse
from .operations import compare as o_compare


@click.group()
@click.pass_context
@click.argument("version", type=str)
def cli(ctx: click.Context, version: str) -> None:
    """Asemver CLI

    Basic manipulation of semantic versions on the command line.
    Note that unless you are using the "clean" or "valid" command,
    passed versions should not have "v" in the beginning.

    Semver 2.0.0: https://semver.org/
    """

    # click ctx should be version string
    ctx.obj = version


@cli.command()
@click.pass_context
def clean(ctx: click.Context) -> None:
    """Cleans the given version string

    Removes any "v" or "=" character from the beginning of the string.
    """

    uncleaned: str = ctx.obj

    try:
        cleaned_obj = clean_and_parse(uncleaned)
        click.echo(str(cleaned_obj))
    except ParseException as exc:
        click.echo(exc)
        sys.exit(1)


@cli.command()
@click.argument("rhs", type=str)
@click.pass_context
def compare(ctx: click.Context, rhs: str) -> None:
    """Compares two version strings

    Outputs 0 if VERSION is equal to RHS, 1 if VERSION is greater than RHS,
    and -1 if VERSION is less than RHS. Note that build labels are not taken
    into account when comparing.
    """

    lhs: str = ctx.obj

    try:
        cmp = o_compare(lhs, rhs)
        click.echo(cmp)
    except ParseException as exc:
        click.echo(exc)
        sys.exit(1)


def main() -> None:
    cli(prog_name="aversioner")


if __name__ == "__main__":
    main()
