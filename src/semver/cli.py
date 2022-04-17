import csv
import json
import sys
import typing as t

import click

from . import __version__
from .constants import EXC_INVALID_STR
from .exc import ParseException
from .operations import clean_and_parse
from .operations import compare as o_compare
from .operations import (
    get_build,
    get_major,
    get_minor,
    get_patch,
    get_pre,
    get_pre_digit,
)
from .operations import valid as o_valid


@click.group()
@click.pass_context
@click.argument("semver", type=str)
@click.version_option(__version__)
def cli(ctx: click.Context, semver: str) -> None:
    """Asemver CLI

    Basic manipulation of semantic versions on the command line.
    Note that unless you are using the "clean" or "valid" command,
    passed versions should not have "v" in the beginning.

    Semver 2.0.0: https://semver.org/
    """

    # click ctx should be version string
    ctx.obj = semver


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


@cli.command("print")
@click.pass_context
@click.option("--no-major", is_flag=True, help="Leave out major version")
@click.option("--no-minor", is_flag=True, help="Leave out minor version")
@click.option("--no-patch", is_flag=True, help="Leave out patch version")
@click.option("--no-build", is_flag=True, help="Leave out build label")
@click.option("--no-pre", is_flag=True, help="Leave out pre-release label")
@click.option("--no-pre-digit", is_flag=True, help="Leave out pre-release digit")
@click.option(
    "-f",
    "--format",
    type=click.Choice(["csv", "json"], case_sensitive=False),
    default="json",
    show_default=True,
    help="Format of output",
)
def print_version(
    ctx: click.Context,
    no_major: bool,
    no_minor: bool,
    no_patch: bool,
    no_build: bool,
    no_pre: bool,
    no_pre_digit: bool,
    format: str,
):
    """Prints version components in a specified way

    Prints out version components (i.e. major, minor, and patch version numbers,
    build and pre-release labels, and the pre-release digit). By default all components
    are printed out, but certain components can be selected to be left out and not
    be printed (see options below).

    The only supported output formats are JSON and CSV.

    Comma-separated values are in this order: major, minor, patch, pre, pre_digit,
    build (There will be no spaces after the comma; the spaces above are only
    shown for clarity). Excluded and None values will be blank values when printing.

    The JSON keys are "major", "minor", "patch", "pre", "pre_digit", "build", and the
    values are the corresponding values in the version string. The keys will not
    be in the JSON object if it is excluded and it will be null if it does not
    have a value.
    """

    version: str = ctx.obj
    if not o_valid(version):
        click.echo(EXC_INVALID_STR.format("semantic version", version))
        sys.exit(1)

    # order: major, minor, patch, pre, pre digit, build
    exclude_list = (no_major, no_minor, no_patch, no_pre, no_pre_digit, no_build)
    to_print_list = (
        get_major(version),
        get_minor(version),
        get_patch(version),
        get_pre(version),
        get_pre_digit(version),
        get_build(version),
    )

    if format == "json":
        json_dict = dict()
        keys = ("major", "minor", "patch", "pre", "pre_digit", "build")

        # fill dict with non-excluded keys and their values
        for key, excluded, to_print in zip(keys, exclude_list, to_print_list):
            if not excluded:
                json_dict[key] = to_print

        json_obj = json.dumps(json_dict)
        click.echo(json_obj)
    elif format == "csv":
        writer = csv.writer(sys.stdout)
        to_write: t.List[str] = []

        # fill list with non-excluded keys. Excluded keys are filled with None
        for excluded, to_print in zip(exclude_list, to_print_list):
            if not excluded:
                to_write.append(to_print)
            else:
                to_write.append(None)

        writer.writerow(to_write)


@cli.command()
@click.pass_context
def valid(ctx: click.Context) -> None:
    """Checks if given string is a valid semver string"""

    version: str = ctx.obj
    is_valid = o_valid(version)

    if is_valid:
        click.echo("Valid")
    else:
        click.echo("Invalid")
        sys.exit(1)


def main() -> None:
    cli(prog_name="asemver")


if __name__ == "__main__":
    main()
