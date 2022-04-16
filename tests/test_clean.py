import pytest
from semver.exc import ParseException
from semver.operations import clean, clean_and_parse

"""
clean()
"""


@pytest.mark.parametrize(
    "good",
    [
        "0.0.4",
        "1.2.3",
        "10.20.30",
        "1.1.2-prerelease+meta",
        "1.1.2+meta",
        "1.1.2+meta-valid",
        "1.0.0-alpha",
        "1.0.0-beta",
        "1.0.0-alpha.beta",
        "1.0.0-alpha.beta.1",
        "1.0.0-alpha.1",
    ],
)
def test_good_str_stays_same(good):
    assert clean(good) == good


@pytest.mark.parametrize(
    "s, res",
    [
        ("  0.0.4", "0.0.4"),
        ("1.2.3   ", "1.2.3"),
        ("     10.20.30    \t", "10.20.30"),
        ("1.1.2-prerelease+meta    ", "1.1.2-prerelease+meta"),
        ("1.1.2+meta   ", "1.1.2+meta"),
        ("1.1.2+meta-valid   ", "1.1.2+meta-valid"),
        ("1.0.0-alpha   ", "1.0.0-alpha"),
        ("   1.0.0-beta  ", "1.0.0-beta"),
        ("   1.0.0-alpha.beta   ", "1.0.0-alpha.beta"),
        ("    1.0.0-alpha.beta.1   ", "1.0.0-alpha.beta.1"),
        ("  1.0.0-alpha.1", "1.0.0-alpha.1"),
    ],
)
def test_remove_whitespace(s, res):
    assert clean(s) == res


@pytest.mark.parametrize(
    "s, res",
    [
        ("  v0.0.4", "0.0.4"),
        ("=v1.2.3", "1.2.3"),
        ("v=10.20.30", "10.20.30"),
        ("=1.1.2-prerelease+meta  \t  ", "1.1.2-prerelease+meta"),
        ("=1.1.2+meta", "1.1.2+meta"),
        ("   =v1.1.2+meta-valid   ", "1.1.2+meta-valid"),
        ("    v=1.0.0-alpha   ", "1.0.0-alpha"),
        ("   =1.0.0-beta  ", "1.0.0-beta"),
        ("   v1.0.0-alpha.beta   ", "1.0.0-alpha.beta"),
        ("    =v1.0.0-alpha.beta.1   ", "1.0.0-alpha.beta.1"),
        ("  v=1.0.0-alpha.1", "1.0.0-alpha.1"),
    ],
)
def test_remove_whitespace_and_v_pref(s, res):
    assert clean(s) == res


@pytest.mark.parametrize(
    "s, res",
    [
        ("  v0.0.4", "0.0.4"),
        ("=v1.2.3", "1.2.3"),
        ("v=10.20.30", "10.20.30"),
        ("=1.1.2-prerelease+meta  \t  ", "1.1.2-prerelease+meta"),
        ("=1.1.2+meta", "1.1.2+meta"),
        ("   =v1.1.2+meta-valid   ", "1.1.2+meta-valid"),
        ("    v=1.0.0-alpha   ", "1.0.0-alpha"),
        ("   =1.0.0-beta  ", "1.0.0-beta"),
        ("   v1.0.0-alpha.beta   ", "1.0.0-alpha.beta"),
        ("    =v1.0.0-alpha.beta.1   ", "1.0.0-alpha.beta.1"),
        ("  v=1.0.0-alpha.1", "1.0.0-alpha.1"),
    ],
)
def test_clean_and_good_parse(s, res):
    v = clean_and_parse(s)

    assert str(v) == res


@pytest.mark.parametrize(
    "s",
    [
        ("  v00.4"),
        ("=v1..2.3"),
        ("v=10.20-30"),
        ("=1.1.02-prerelease+meta  \t  "),
    ],
)
def test_clean_and_bad_parse_error(s):
    with pytest.raises(ParseException):
        clean_and_parse(s)
