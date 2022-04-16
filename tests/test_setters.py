"""
set_build(), set_major(), set_minor(), set_micro(), set_pre()
"""

import pytest
from semver.operations import set_build, set_major, set_minor, set_patch, set_pre


@pytest.mark.parametrize(
    "orig, build, res",
    [
        ("2.6.2", "meta1", "2.6.2+meta1"),
        ("2.6.2-alpha.6", "meta23", "2.6.2-alpha.6+meta23"),
        ("2.6.2-alpha.6+meta12", "meta5", "2.6.2-alpha.6+meta5"),
        ("2.6.2+meta2", "meta5", "2.6.2+meta5"),
    ],
)
def test_set_build(orig, build, res):
    assert res == set_build(orig, build)


@pytest.mark.parametrize(
    "orig, pre, res",
    [
        ("2.6.2", "alpha.3", "2.6.2-alpha.3"),
        ("2.6.2-alpha.6", "beta.56", "2.6.2-beta.56"),
        ("2.6.2-alpha.6+meta12", "rc.123", "2.6.2-rc.123+meta12"),
        ("2.6.2+meta2", "alpha.0", "2.6.2-alpha.0+meta2"),
    ],
)
def test_set_pre(orig, pre, res):
    assert res == set_pre(orig, pre)


@pytest.mark.parametrize(
    "orig, major, res",
    [
        ("2.6.2", 3, "3.6.2"),
        ("2.6.2-alpha.6", 223, "223.6.2-alpha.6"),
        ("2.6.2-alpha.6+meta12", 45, "45.6.2-alpha.6+meta12"),
        ("2.6.2+meta2", 0, "0.6.2+meta2"),
    ],
)
def test_set_major(orig, major, res):
    assert res == set_major(orig, major)


@pytest.mark.parametrize(
    "orig, minor, res",
    [
        ("2.6.2", 3, "2.3.2"),
        ("2.6.2-alpha.6", 223, "2.223.2-alpha.6"),
        ("2.6.2-alpha.6+meta12", 45, "2.45.2-alpha.6+meta12"),
        ("2.6.2+meta2", 0, "2.0.2+meta2"),
    ],
)
def test_set_minor(orig, minor, res):
    assert res == set_minor(orig, minor)


@pytest.mark.parametrize(
    "orig, patch, res",
    [
        ("2.6.2", 3, "2.6.3"),
        ("2.6.2-alpha.6", 223, "2.6.223-alpha.6"),
        ("2.6.2-alpha.6+meta12", 45, "2.6.45-alpha.6+meta12"),
        ("2.6.2+meta2", 0, "2.6.0+meta2"),
    ],
)
def test_set_patch(orig, patch, res):
    assert res == set_patch(orig, patch)
