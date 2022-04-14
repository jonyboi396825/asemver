import re

import pytest
from semver.components import Build
from semver.constants import EXC_INVALID_STR
from semver.exc import ParseException


@pytest.mark.parametrize("bad", ["meta+meta", "", "+", "+meta", "meta_bad", " ", "."])
def test_bad_parse(bad):
    with pytest.raises(
        ParseException, match=re.escape(EXC_INVALID_STR.format("build/metadata"))
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

    assert repr(b) == good
    assert str(b) == "+" + good
    assert b.string == good


@pytest.mark.parametrize("bad", ["meta+meta", "", "+", "+meta", "meta_bad", " ", "."])
def test_bad_setter(bad):
    b = Build("meta")
    with pytest.raises(
        ParseException, match=re.escape(EXC_INVALID_STR.format("build/metadata"))
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

    assert repr(b) == good
    assert str(b) == "+" + good
    assert b.string == good
