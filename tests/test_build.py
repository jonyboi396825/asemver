"""
Build class
"""

import re

import pytest
from semver.components import Build
from semver.exc import ParseException


@pytest.mark.parametrize("bad", ["meta+meta", "", "+", "+meta", "meta_bad", " ", "."])
def test_bad_parse(bad):
    with pytest.raises(
        ParseException, match=re.escape("Invalid build/metadata string: {}".format(bad))
    ):
        Build(bad)


@pytest.mark.parametrize(
    "good",
    [
        "meta",
        "meta-valid",
        "build.1-aef.1-its-okay",
        "build.1",
        "build.123",
        "788",
        "0.build.1-rc.10000aaa-kk-0.1",
        "1ac93c",
    ],
)
def test_good_parse(good):
    b = Build(good)

    assert str(b) == "+" + good
    assert b.string == good

    assert repr(b) == "Build(string='{}')".format(good)


@pytest.mark.parametrize(
    "good, rep",
    [
        ("meta", "Build(string='meta')"),
        ("meta-valid", "Build(string='meta-valid')"),
        ("build.1-aef.1-its-okay", "Build(string='build.1-aef.1-its-okay')"),
        ("build.1", "Build(string='build.1')"),
        ("build.123", "Build(string='build.123')"),
        ("788", "Build(string='788')"),
        (
            "0.build.1-rc.10000aaa-kk-0.1",
            "Build(string='0.build.1-rc.10000aaa-kk-0.1')",
        ),
        ("1ac93c", "Build(string='1ac93c')"),
    ],
)
def test_repr(good, rep):
    bd = Build(good)
    assert repr(bd) == rep


@pytest.mark.parametrize("bad", ["meta+meta", "", "+", "+meta", "meta_bad", " ", "."])
def test_bad_setter(bad):
    b = Build("meta")
    with pytest.raises(
        ParseException, match=re.escape("Invalid build/metadata string: {}".format(bad))
    ):
        b.string = bad


@pytest.mark.parametrize(
    "good",
    [
        "meta",
        "meta-valid",
        "build.1-aef.1-its-okay",
        "build.1",
        "build.123",
        "788",
        "0.build.1-rc.10000aaa-kk-0.1",
        "1ac93c",
    ],
)
def test_good_setter(good):
    b = Build("meta")
    b.string = good

    assert str(b) == "+" + good
    assert b.string == good
