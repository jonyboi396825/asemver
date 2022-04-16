"""
bump()
"""

import re

import pytest
from semver.constants import VPos, VRm
from semver.exc import InvalidPositionException, NoValueException
from semver.operations import bump


@pytest.mark.parametrize("bad", [5, "str", 4.2, object, 2 + 1j, VRm.BUILD, VRm.PRE])
def test_bad_bump_pos(bad):
    with pytest.raises(
        InvalidPositionException,
        match=re.escape("Unrecognized version position: {}".format(bad)),
    ):
        bump("1.2.3", bad)


def test_error_bump_no_pre():
    with pytest.raises(
        NoValueException,
        match=re.escape(
            "Object has no pre-release label: "
            "Version(major=1, minor=2, patch=3, pre=None, build=None)"
        ),
    ):
        bump("1.2.3", VPos.PRE)


def test_error_bump_no_pre_digit():
    with pytest.raises(
        NoValueException,
        match=re.escape(
            (
                "No digit to increment/decrement. Make sure the last "
                "dot-separated identifier is a numeric value: alpha6"
            )
        ),
    ):
        bump("1.2.5-alpha6", VPos.PRE)


@pytest.mark.parametrize(
    "orig, pos, amt, res",
    [
        ("2.5.3-alpha.52+meta34", VPos.MAJOR, 1, "3.5.3-alpha.52+meta34"),
        ("2.5.3-alpha.52+meta34", VPos.MINOR, 1, "2.6.3-alpha.52+meta34"),
        ("2.5.3+meta34", VPos.PATCH, 1, "2.5.4+meta34"),
        ("2.5.3-alpha.52+meta34", VPos.PRE, 1, "2.5.3-alpha.53+meta34"),
        ("2.5.3-alpha.52+meta34", VPos.MAJOR, 4, "6.5.3-alpha.52+meta34"),
        ("2.5.3-alpha.52+meta34", VPos.MINOR, 2, "2.7.3-alpha.52+meta34"),
        ("2.5.3-alpha.52+meta34", VPos.PATCH, 9, "2.5.12-alpha.52+meta34"),
        ("2.5.3-alpha.52+meta34", VPos.PRE, 3, "2.5.3-alpha.55+meta34"),
    ],
)
def test_bump_no_carry(orig, pos, amt, res):
    assert res == bump(orig, pos, amt, False)


@pytest.mark.parametrize(
    "orig, pos, amt, res",
    [
        ("2.5.3-alpha.52+meta34", VPos.MAJOR, 1, "3.0.0+meta34"),
        ("2.5.3-alpha.52+meta34", VPos.MINOR, 1, "2.6.0+meta34"),
        ("2.5.3+meta34", VPos.PATCH, 1, "2.5.4+meta34"),
        ("2.5.3-alpha.52+meta34", VPos.PRE, 1, "2.5.3-alpha.53+meta34"),
        ("2.5.3-alpha.52+meta34", VPos.MAJOR, 4, "6.0.0+meta34"),
        ("2.5.3-alpha.52+meta34", VPos.MINOR, 2, "2.7.0+meta34"),
        ("2.5.3-alpha.52+meta34", VPos.PATCH, 9, "2.5.12+meta34"),
        ("2.5.3-alpha.52+meta34", VPos.PRE, 3, "2.5.3-alpha.55+meta34"),
    ],
)
def test_bump_carry(orig, pos, amt, res):
    assert res == bump(orig, pos, amt, True)
