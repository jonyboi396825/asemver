"""
print command with -f json
"""

import json

from click.testing import CliRunner
import pytest
from semver.cli import cli


@pytest.mark.parametrize(
    "bad",
    [
        "1.2.3.DEV",
        "1.2-SNAPSHOT",
        "1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788",
        "1.2-RC-SNAPSHOT",
        "+justmeta",
        "9.8.7+meta+meta",
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
        (
            "4.7.2",
            ["--no-major", "--no-pre"],
            {
                "minor": 7,
                "patch": 2,
                "pre_digit": None,
                "build": None,
            },
        ),
        (
            "4.7.2-alpha",
            ["--no-minor", "--no-pre"],
            {
                "major": 4,
                "patch": 2,
                "pre_digit": None,
                "build": None,
            },
        ),
        (
            "9.8.12-beta+abcmeta.25",
            ["--no-patch", "--no-pre-digit"],
            {"major": 9, "minor": 8, "pre": "beta", "build": "abcmeta.25"},
        ),
        (
            "5.2.32-alpha.66+meta.12",
            ["--no-build"],
            {
                "major": 5,
                "minor": 2,
                "patch": 32,
                "pre": "alpha.66",
                "pre_digit": 66,
            },
        ),
        (
            "1.2.3-rc.0+build1234",
            [],
            {
                "major": 1,
                "minor": 2,
                "patch": 3,
                "pre": "rc.0",
                "pre_digit": 0,
                "build": "build1234",
            },
        ),
        (
            "1.2.3-rc+build1234",
            [],
            {
                "major": 1,
                "minor": 2,
                "patch": 3,
                "pre": "rc",
                "pre_digit": None,
                "build": "build1234",
            },
        ),
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
            dict(),
        ),
    ],
)
def test_options(string, exclude, res):
    runner = CliRunner()
    result = runner.invoke(cli, [string, "print"] + exclude + ["-f", "json"])

    assert result.exit_code == 0
    assert result.output == json.dumps(res) + "\n"
