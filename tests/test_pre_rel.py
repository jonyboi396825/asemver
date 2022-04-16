"""
Pre class
"""

import pytest
import re
from semver.components import Pre
from semver.exc import NegativeValueException, ParseException, NoValueException


class TestParse:
    """From

    https://regex101.com/r/vkijKf/1/
    """

    @pytest.mark.parametrize(
        "bad",
        [
            "0123",
            "0123.0123",
            "d.05",
            "alpha_beta",
            "alpha..",
            "alpha..1",
            "-alpha....1",
            ".",
            "alpha..........1",
            "afd..23",
            "中文",
            "---RC-SNAPSHOT.12.9.1--.09",
            "-23.\2",
            (
                "99999999999999999999999.999999999999999999.99999999999999999----"
                "RC-SNAPSHOT.12.09.1--------------------------------..12"
            ),
            "",
            " ",
            " .     ",
        ],
    )
    def test_bad_parse(self, bad):
        with pytest.raises(
            ParseException,
            match=re.escape("Invalid pre-release string: {}".format(bad)),
        ):
            Pre(bad)

        # tests setter
        with pytest.raises(
            ParseException,
            match=re.escape("Invalid pre-release string: {}".format(bad)),
        ):
            p = Pre("-")
            p.string = bad

    @pytest.mark.parametrize(
        "good, digit, rep",
        [
            ("prerelease", None, "Pre(string='prerelease')"),
            ("alpha", None, "Pre(string='alpha')"),
            ("alpha.5", 5, "Pre(string='alpha.5')"),
            ("alpha.2.b.6.1.c", None, "Pre(string='alpha.2.b.6.1.c')"),
            ("beta", None, "Pre(string='beta')"),
            ("beta.6", 6, "Pre(string='beta.6')"),
            ("beta.c.s.d.a.b.c.3", 3, "Pre(string='beta.c.s.d.a.b.c.3')"),
            (
                "alpha.beta.release-candidate.56",
                56,
                "Pre(string='alpha.beta.release-candidate.56')",
            ),
            ("alpha0.valid", None, "Pre(string='alpha0.valid')"),
            ("alpha.0valid", None, "Pre(string='alpha.0valid')"),
            (
                "alpha-a.b-c-something-long",
                None,
                "Pre(string='alpha-a.b-c-something-long')",
            ),
            ("rc.1", 1, "Pre(string='rc.1')"),
            ("1.0.0", 0, "Pre(string='1.0.0')"),
            ("DEV-SNAPSHOT", None, "Pre(string='DEV-SNAPSHOT')"),
            ("SNAPSHOT-123", None, "Pre(string='SNAPSHOT-123')"),
            ("alpha.1227", 1227, "Pre(string='alpha.1227')"),
            (
                "---RC-SNAPSHOT.12.9.1--.12",
                12,
                "Pre(string='---RC-SNAPSHOT.12.9.1--.12')",
            ),
            ("---R-S.12.9.1--.122", 122, "Pre(string='---R-S.12.9.1--.122')"),
            (
                "---RC-SNAPSHOT.12.9.1--.90",
                90,
                "Pre(string='---RC-SNAPSHOT.12.9.1--.90')",
            ),
            (
                "--RC--------1.0.0-0A.is.legal",
                None,
                "Pre(string='--RC--------1.0.0-0A.is.legal')",
            ),
            ("--RC--------1.0.0", 0, "Pre(string='--RC--------1.0.0')"),
        ],
    )
    def test_good_parse_and_digit(self, good, digit, rep):
        p = Pre(good)

        assert p.string == good
        assert p.digit == digit

        assert repr(p) == rep
        assert str(p) == "-" + good

    @pytest.mark.parametrize(
        "good, digit, rep",
        [
            ("prerelease", None, "Pre(string='prerelease')"),
            ("alpha", None, "Pre(string='alpha')"),
            ("alpha.5", 5, "Pre(string='alpha.5')"),
            ("alpha.2.b.6.1.c", None, "Pre(string='alpha.2.b.6.1.c')"),
            ("beta", None, "Pre(string='beta')"),
            ("beta.6", 6, "Pre(string='beta.6')"),
            ("beta.c.s.d.a.b.c.3", 3, "Pre(string='beta.c.s.d.a.b.c.3')"),
            (
                "alpha.beta.release-candidate.56",
                56,
                "Pre(string='alpha.beta.release-candidate.56')",
            ),
            ("alpha0.valid", None, "Pre(string='alpha0.valid')"),
            ("alpha.0valid", None, "Pre(string='alpha.0valid')"),
            (
                "alpha-a.b-c-something-long",
                None,
                "Pre(string='alpha-a.b-c-something-long')",
            ),
            ("rc.1", 1, "Pre(string='rc.1')"),
            ("1.0.0", 0, "Pre(string='1.0.0')"),
            ("DEV-SNAPSHOT", None, "Pre(string='DEV-SNAPSHOT')"),
            ("SNAPSHOT-123", None, "Pre(string='SNAPSHOT-123')"),
            ("alpha.1227", 1227, "Pre(string='alpha.1227')"),
            (
                "---RC-SNAPSHOT.12.9.1--.12",
                12,
                "Pre(string='---RC-SNAPSHOT.12.9.1--.12')",
            ),
            ("---R-S.12.9.1--.122", 122, "Pre(string='---R-S.12.9.1--.122')"),
            (
                "---RC-SNAPSHOT.12.9.1--.90",
                90,
                "Pre(string='---RC-SNAPSHOT.12.9.1--.90')",
            ),
            (
                "--RC--------1.0.0-0A.is.legal",
                None,
                "Pre(string='--RC--------1.0.0-0A.is.legal')",
            ),
            ("--RC--------1.0.0", 0, "Pre(string='--RC--------1.0.0')"),
        ],
    )
    def test_setter(self, good, digit, rep):
        # tests setter
        p = Pre("-")
        p.string = good

        assert p.string == good
        assert p.digit == digit

        assert str(p) == "-" + good
        assert repr(p) == rep


@pytest.mark.parametrize(
    "pre",
    [
        ("prerelease"),
        ("alpha"),
        ("alpha.5"),
        ("alpha.2.b.6.1.c"),
        ("beta"),
        ("beta.6"),
        ("beta.c.s.d.a.b.c.3"),
        ("alpha.beta.release-candidate.56"),
        ("alpha0.valid"),
        ("alpha.0valid"),
        ("alpha-a.b-c-something-long"),
        ("rc.1"),
        ("beta"),
        ("DEV-SNAPSHOT"),
        ("SNAPSHOT-123"),
        ("alpha.1227"),
        ("---RC-SNAPSHOT.12.9.1--.12"),
        ("---R-S.12.9.1--.122"),
        ("---RC-SNAPSHOT.12.9.1--.90"),
        ("--RC--------1.0.0-0A.is.legal"),
        ("--RC--------1.0.0"),
    ],
)
def test_reset(pre):
    p = Pre(pre)
    p.reset()

    assert p.string == "-"


class TestOperators:
    @pytest.mark.parametrize("bad", [0.2, 4 + 3j, "abc", object])
    def test_wrong_type(self, bad):
        pre = Pre("alpha")

        with pytest.raises(
            TypeError, match="Must be compared with another pre-release object"
        ):
            pre < bad

        with pytest.raises(
            TypeError, match="Must be compared with another pre-release object"
        ):
            pre > bad

        with pytest.raises(
            TypeError, match="Must be compared with another pre-release object"
        ):
            pre == bad

        with pytest.raises(
            TypeError, match="Must be compared with another pre-release object"
        ):
            pre != bad

        with pytest.raises(
            TypeError, match="Must be compared with another pre-release object"
        ):
            pre <= bad

        with pytest.raises(
            TypeError, match="Must be compared with another pre-release object"
        ):
            pre >= bad

    @pytest.mark.parametrize(
        "lhs, rhs",
        [
            ("prerelease", "prerelease"),
            ("alpha", "alpha"),
            ("beta", "beta"),
            ("---DEV-SNAPSHOT", "---DEV-SNAPSHOT"),
            ("0.3.6", "0.3.6"),
            ("x.7.z.92", "x.7.z.92"),
        ],
    )
    def test_eq(self, lhs, rhs):
        assert Pre(lhs) == Pre(rhs)

    @pytest.mark.parametrize(
        "lhs, rhs",
        [
            ("prerelease", "alpha"),
            ("alpha", "beta"),
            ("beta", "beta.8"),
            ("---DEV-SNAPSHOT", "---DEV-SNAPSHOT.6"),
            ("0.3.6", "0.3.8"),
            ("x.7.z.92", "x.7.z.94"),
            ("-", "--"),
        ],
    )
    def test_ne(self, lhs, rhs):
        assert Pre(lhs) != Pre(rhs)

    @pytest.mark.parametrize(
        "lhs, rhs",
        [
            ("alpha", "alpha.1"),
            ("alpha.1", "alpha.beta"),
            ("alpha", "beta"),
            ("beta.1", "beta.2"),
            ("rc.1", "rc.2"),
        ],
    )
    def test_lt_gt(self, lhs, rhs):
        assert Pre(lhs) < Pre(rhs)
        assert Pre(rhs) > Pre(lhs)

    def test_chain(self):
        assert (
            Pre("alpha")
            < Pre("alpha.1")
            < Pre("alpha.beta")
            < Pre("beta")
            < Pre("beta.2")
            < Pre("beta.11")
            < Pre("rc.1")
        )

    @pytest.mark.parametrize(
        "lhs, rhs",
        [
            ("alpha", "alpha.1"),
            ("alpha.1", "alpha.beta"),
            ("alpha", "beta"),
            ("beta.1", "beta.2"),
            ("rc.1", "rc.2"),
        ],
    )
    def test_le_ge(self, lhs, rhs):
        assert Pre(lhs) <= Pre(rhs)
        assert Pre(rhs) >= Pre(lhs)


class TestInc:
    @pytest.mark.parametrize(
        "bad", ["alpha5.x", "beta54", "5.1.x", "-", "DEV-SNAPSHOT.-"]
    )
    def test_cannot_inc(self, bad):
        p = Pre(bad)
        with pytest.raises(
            NoValueException,
            match=re.escape(
                (
                    "No digit to increment/decrement. Make sure the last dot-separated"
                    " identifier is a numeric value: {}"
                ).format(bad)
            ),
        ):
            p.inc()

    @pytest.mark.parametrize(
        "orig, res",
        [
            ("4.5", "4.6"),
            ("alpha.4.5.x.2", "alpha.4.5.x.3"),
            ("rc.3", "rc.4"),
            ("DEV-SNAPSHOT-----.2", "DEV-SNAPSHOT-----.3"),
            ("e.10", "e.11"),
            ("r.2010102", "r.2010103"),
        ],
    )
    def test_inc(self, orig, res):
        p = Pre(orig)
        p.inc()
        assert p == Pre(res)


class TestDec:
    @pytest.mark.parametrize(
        "bad", ["alpha5.x", "beta54", "5.1.x", "-", "DEV-SNAPSHOT.-"]
    )
    def test_cannot_dec(self, bad):
        p = Pre(bad)
        with pytest.raises(
            NoValueException,
            match=re.escape(
                (
                    "No digit to increment/decrement. Make sure the last dot-separated"
                    " identifier is a numeric value: {}"
                ).format(bad)
            ),
        ):
            p.dec()

    @pytest.mark.parametrize(
        "orig, res",
        [
            ("4.5", "4.4"),
            ("alpha.4.5.x.2", "alpha.4.5.x.1"),
            ("rc.3", "rc.2"),
            ("e.10", "e.9"),
            ("r.2010102", "r.2010101"),
        ],
    )
    def test_dec(self, orig, res):
        p = Pre(orig)
        p.dec()
        assert p == Pre(res)

    @pytest.mark.parametrize(
        "zeroed", ["4.0", "alpha.4.5.x.0", "DEV-SNAPSHOT.0", "rc.0", "r.---.0"]
    )
    def test_dec_zeroed(self, zeroed):
        p = Pre(zeroed)
        with pytest.raises(
            NegativeValueException,
            match=re.escape("Cannot decrement number to a negative value"),
        ):
            p.dec()


@pytest.mark.parametrize(
    "pre, true",
    [
        ("4.6.x", False),
        ("beta.56", False),
        ("alpha", True),
        ("alphab", False),
        ("alpha.5", True),
        ("alpha.x.4.x", True),
        ("alpha0.x", True),
        ("a0", True),
        ("ab", False),
        ("ab0", False),
    ],
)
def test_is_alpha(pre, true):
    assert Pre(pre).is_alpha == true


@pytest.mark.parametrize(
    "pre, true",
    [
        ("4.6.x", False),
        ("beta.56", True),
        ("beta", True),
        ("beta0", True),
        ("alpha.5", False),
        ("beta.x.4.x", True),
        ("alpha0.x", False),
        ("rc.x", False),
        ("b24", True),
        ("betab", False),
        ("bb8", False),
    ],
)
def test_is_beta(pre, true):
    assert Pre(pre).is_beta == true


@pytest.mark.parametrize(
    "pre, true",
    [
        ("4.6.x", False),
        ("beta.56", False),
        ("beta", False),
        ("alpha.5", False),
        ("beta.x.4.x", False),
        ("rc.x", True),
        ("rc.2.x.4", True),
        ("rc", True),
        ("rc6.2", True),
        ("rcd", False),
    ],
)
def test_is_rc(pre, true):
    assert Pre(pre).is_rc == true
