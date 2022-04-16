"""
get_build(), get_major(), get_minor(), get_patch(), get_pre(), get_pre_digit()
"""

import pytest
from semver.operations import (
    get_build,
    get_major,
    get_minor,
    get_patch,
    get_pre,
    get_pre_digit,
)


@pytest.mark.parametrize(
    "v, expect",
    [
        ("2.5.2-alpha.6", None),
        ("2.5.2", None),
        ("2.5.2-alpha.6+meta", "meta"),
        ("2.5.2+meta2395", "meta2395"),
    ],
)
def test_get_build(v, expect):
    assert get_build(v) == expect


@pytest.mark.parametrize(
    "v, expect",
    [
        ("2.5.2-alpha.6", "alpha.6"),
        ("2.5.2", None),
        ("2.5.2-alpha.6+meta", "alpha.6"),
        ("2.5.2+meta2395", None),
    ],
)
def test_get_pre(v, expect):
    assert get_pre(v) == expect


@pytest.mark.parametrize(
    "v, expect",
    [
        ("2.5.2-alpha.63", 63),
        ("2.5.2", None),
        ("2.5.2-alpha.6+meta", 6),
        ("2.5.2+meta2395", None),
        ("2.5.2-beta5", None),
    ],
)
def test_get_pre_digit(v, expect):
    assert get_pre_digit(v) == expect


def test_get_major():
    v = "3.56.2"
    assert get_major(v) == 3


def test_get_minor():
    v = "3.56.2"
    assert get_minor(v) == 56


def test_get_patch():
    v = "3.56.2"
    assert get_patch(v) == 2
