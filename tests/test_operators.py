import pytest
from semver.operations import compare

"""
compare()
"""


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
    assert compare(lhs, rhs) == 0


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
    assert compare(lhs, rhs) < 0


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
    assert compare(lhs, rhs) > 0
