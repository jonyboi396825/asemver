"""
clean command
"""

from click.testing import CliRunner
import pytest
from semver.cli import cli
from semver.operations import clean


@pytest.mark.parametrize(
    "v",
    [
        "1.45.3.2",
        "2.a.5",
        "v=e3.4.01",
    ],
)
def test_clean_error(v):
    runner = CliRunner()
    res = runner.invoke(cli, [v, "clean"])
    assert res.exit_code == 1
    assert res.output == "Invalid semantic version string: {}\n".format(clean(v))


@pytest.mark.parametrize(
    "v, res",
    [
        ("1.2.3", "1.2.3\n"),
        ("v1.2.3", "1.2.3\n"),
        ("=1.2.3", "1.2.3\n"),
        ("v=1.2.3", "1.2.3\n"),
        ("=v1.2.3", "1.2.3\n"),
    ],
)
def test_clean(v, res):
    runner = CliRunner()
    result = runner.invoke(cli, [v, "clean"])
    assert result.exit_code == 0
    assert result.output == res
