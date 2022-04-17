"""
compare command
"""

from click.testing import CliRunner
import pytest
from semver.cli import cli


@pytest.mark.parametrize(
    "lhs, rhs",
    [
        ("a", "bc"),
        ("23.02.3", "1.2.3"),
        ("23.02", "2.1b9"),
    ],
)
def test_invalid_lstr(lhs, rhs):
    runner = CliRunner()
    result = runner.invoke(cli, [lhs, "compare", rhs])

    assert result.exit_code == 1
    assert result.output == "Invalid semantic version string: {}\n".format(lhs)


@pytest.mark.parametrize(
    "lhs, rhs",
    [
        ("2.5.2", "bc"),
        ("23.32.11", "1-2.3"),
        ("23.202.6", "2.1b9+meta+e"),
    ],
)
def test_invalid_rstr(lhs, rhs):
    runner = CliRunner()
    result = runner.invoke(cli, [lhs, "compare", rhs])

    assert result.exit_code == 1
    assert result.output == "Invalid semantic version string: {}\n".format(rhs)


@pytest.mark.parametrize(
    "lhs, rhs",
    [
        ("4.5.6", "4.5.6"),
        ("4.5.6-alpha.1", "4.5.6-alpha.1"),
        ("4.5.6+meta1", "4.5.6+meta2"),
        ("4.5.6-alpha.1+meta1", "4.5.6-alpha.1+meta2"),
    ],
)
def test_eq(lhs, rhs):
    runner = CliRunner()
    result = runner.invoke(cli, [lhs, "compare", rhs])

    assert result.exit_code == 0
    assert result.output == "0\n"


@pytest.mark.parametrize(
    "lhs, rhs",
    [
        ("1.0.0-alpha", "1.0.0-alpha.1"),
        ("1.0.0-alpha.1", "1.0.0-alpha.beta"),
        ("1.0.0-alpha.beta", "1.0.0-beta"),
        ("1.0.0-beta", "1.0.0-beta.11"),
        ("1.0.0-beta.11", "1.0.0-rc.1"),
        ("1.0.0-rc.1", "1.0.0"),
        ("1.0.0", "1.0.1-beta.1"),
        ("1.0.1-beta.1", "1.0.1-rc.6"),
        ("1.0.1-rc.6", "1.0.1"),
        ("1.0.1", "1.2.0"),
        ("1.2.0", "2.0.0"),
    ],
)
def test_lt(lhs, rhs):
    runner = CliRunner()
    result = runner.invoke(cli, [lhs, "compare", rhs])

    assert result.exit_code == 0
    assert result.output == "-1\n"


@pytest.mark.parametrize(
    "rhs, lhs",
    [
        ("1.0.0-alpha", "1.0.0-alpha.1"),
        ("1.0.0-alpha.1", "1.0.0-alpha.beta"),
        ("1.0.0-alpha.beta", "1.0.0-beta"),
        ("1.0.0-beta", "1.0.0-beta.11"),
        ("1.0.0-beta.11", "1.0.0-rc.1"),
        ("1.0.0-rc.1", "1.0.0"),
        ("1.0.0", "1.0.1-beta.1"),
        ("1.0.1-beta.1", "1.0.1-rc.6"),
        ("1.0.1-rc.6", "1.0.1"),
        ("1.0.1", "1.2.0"),
        ("1.2.0", "2.0.0"),
    ],
)
def test_gt(lhs, rhs):
    runner = CliRunner()
    result = runner.invoke(cli, [lhs, "compare", rhs])

    assert result.exit_code == 0
    assert result.output == "1\n"
