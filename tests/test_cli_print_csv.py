"""
print command with -f csv
"""

from click.testing import CliRunner
import pytest
from semver.cli import cli


@pytest.mark.parametrize(
    "bad",
    [
        "alpha.beta.1",
        "alpha.1",
        "alpha+beta",
        "alpha_beta",
        "alpha.",
        "alpha..",
        "beta",
        "1.0.0-alpha_beta",
    ],
)
def test_invalid_str(bad):
    runner = CliRunner()
    result = runner.invoke(cli, [bad, "print"])

    assert result.exit_code == 1
    assert result.output == "Invalid semantic version string: {}\n".format(bad)


@pytest.mark.parametrize(
    "string, exclude, res",
    [
        ("4.7.2", ["--no-major", "--no-pre"], ",7,2,,,"),
        ("4.7.2-alpha", ["--no-minor", "--no-pre"], "4,,2,,,"),
        (
            "9.8.12-beta+abcmeta.25",
            ["--no-patch", "--no-pre-digit"],
            "9,8,,beta,,abcmeta.25",
        ),
        ("5.2.32-alpha.66+meta.12", ["--no-build"], "5,2,32,alpha.66,66,"),
        ("1.2.3-rc.0+build1234", [], "1,2,3,rc.0,0,build1234"),
        ("1.2.3-rc+build1234", [], "1,2,3,rc,,build1234"),
        (
            "2.6.9-alpha+build",
            [
                "--no-major",
                "--no-minor",
                "--no-patch",
                "--no-pre",
                "--no-pre-digit",
                "--no-build",
            ],
            ",,,,,",
        ),
    ],
)
def test_options(string, exclude, res):
    runner = CliRunner()
    result = runner.invoke(cli, [string, "print"] + exclude + ["-f", "csv"])

    assert result.exit_code == 0
    assert result.output == res + "\n"
