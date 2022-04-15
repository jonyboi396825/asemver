import pytest
import re
from semver.version import Version, VersionNumber, Pre, Build, parse_version
from semver.constants import (
    VPos,
    VRm,
)
from semver.exc import (
    InvalidOperationException,
    InvalidPositionException,
    NegativeValueException,
    ParseException,
    NoValueException,
)


class TestConstructor:
    @pytest.mark.parametrize(
        "major, minor, patch", [(-1, 0, 5), (0, -4, 6), (0, 0, -3)]
    )
    def test_error_on_negative(self, major, minor, patch):
        with pytest.raises(
            NegativeValueException, match=r"Number must be positive: [\d]*"
        ):
            Version(major, minor, patch)

    @pytest.mark.parametrize("bad", ["01", 3.6, 2 + 5j, -2.5, object])
    def test_error_number_on_non_int(self, bad):
        with pytest.raises(
            TypeError, match=r"Value must be a\(n\) int, not {}".format(type(bad))
        ):
            Version(bad, 0, 0)

        with pytest.raises(
            TypeError, match=r"Value must be a\(n\) int, not {}".format(type(bad))
        ):
            Version(0, bad, 0)

        with pytest.raises(
            TypeError, match=r"Value must be a\(n\) int, not {}".format(type(bad))
        ):
            Version(0, 0, bad)

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
    def test_error_bad_pre(self, bad):
        with pytest.raises(
            ParseException,
            match=re.escape("Invalid pre-release string: {}".format(bad)),
        ):
            Version(0, 0, 0, pre=bad)

    @pytest.mark.parametrize(
        "bad", ["meta+meta", "", "+", "+meta", "meta_bad", " ", "."]
    )
    def test_error_bad_build(self, bad):
        with pytest.raises(
            ParseException,
            match=re.escape("Invalid build/metadata string: {}".format(bad)),
        ):
            Version(0, 0, 0, build=bad)

    def test_bad_pre_and_build(self):
        """Pre should come first"""

        with pytest.raises(
            ParseException, match=re.escape("Invalid pre-release string: alpha..11")
        ):
            Version(0, 0, 0, build="meta+meta", pre="alpha..11")

    def test_bad_num_pre_and_build(self):
        with pytest.raises(
            NegativeValueException, match=re.escape("Number must be positive: -1")
        ):
            Version(0, -1, 2, build="meta+meta", pre="alpha..11")

        with pytest.raises(
            TypeError,
            match=re.escape("Value must be a(n) int, not {}".format(type(1j))),
        ):
            Version(2 + 5j, -1, 2, build="meta+meta", pre="alpha..11")

    @pytest.mark.parametrize(
        "pre, build, digit",
        [
            ("prerelease", "meta", None),
            ("alpha.5", "meta-valid", 5),
            ("beta.6", "build.1-aef.1-its-okay", 6),
            ("beta.c.s.d.ab.c.3", None, 3),
            ("alpha0.valid", "788", None),
            ("alpha.0valid", "0.build.1-rc.10000aaa-kk-0.1", None),
            ("1.0.0", "1ac93c", 0),
            ("---RC-SNAPSHOT.12.9.1--.12", "build.123", 12),
            ("--RC--------1.0.0-0A.is.legal", None, None),
        ],
    )
    def test_valid(self, pre, build, digit):
        v = Version(0, 1, 2, pre=pre, build=build)

        assert v.pre == pre
        assert v.pre_digit == digit
        assert v.build == build


@pytest.mark.parametrize(
    "args, string",
    [
        ((1, 5, 2, "alpha.5", "meta-valid"), "1.5.2-alpha.5+meta-valid"),
        ((4, 23, 66, None, "1ac93c"), "4.23.66+1ac93c"),
        ((2, 5, 1, None, None), "2.5.1"),
        ((4, 3, 6, "alpha.6", None), "4.3.6-alpha.6"),
    ],
)
def test_str(args, string):
    v = Version(*args)

    assert str(v) == string


@pytest.mark.parametrize(
    "args, string",
    [
        (
            (1, 5, 2, "alpha.5", "meta-valid"),
            (
                "Version(major=1, minor=5, patch=2, pre=Pre(string='alpha.5'), "
                "build=Build(string='meta-valid'))"
            ),
        ),
        (
            (4, 23, 66, None, "1ac93c"),
            (
                "Version(major=4, minor=23, patch=66, pre=None, "
                "build=Build(string='1ac93c'))"
            ),
        ),
        (
            (2, 5, 1, None, None),
            "Version(major=2, minor=5, patch=1, pre=None, build=None)",
        ),
        (
            (4, 3, 6, "alpha.6", None),
            "Version(major=4, minor=3, patch=6, pre=Pre(string='alpha.6'), build=None)",
        ),
    ],
)
def test_repr(args, string):
    v = Version(*args)

    assert repr(v) == string


class TestProperties:
    def test_get_major_minor_patch(self):
        v = Version(2, 5, 6)

        assert v.major == 2
        assert v.minor == 5
        assert v.patch == 6

    @pytest.mark.parametrize(
        "v, has_pre, has_build",
        [
            (Version(2, 5, 2), False, False),
            (Version(2, 6, 1, build="meta"), False, True),
            (Version(2, 5, 1, pre="alpha.5"), True, False),
            (Version(1, 1, 1, build="31b2", pre="beta"), True, True),
        ],
    )
    def test_has_pre_build(self, v, has_pre, has_build):
        assert v.has_pre == has_pre
        assert v.has_build == has_build

    def test_major_minor_patch_setter(self):
        v = Version(0, 0, 0, pre="alpha", build="build")

        v.major = VersionNumber(6)
        v.minor = 2
        v.patch = 9

        assert v.major == 6 and v.minor == 2 and v.patch == 9

        # should not delete pre and build versions
        assert v.pre == "alpha" and v.build == "build"

    def test_pre_setter(self):
        v = Version(0, 0, 0, pre="alpha", build="build")
        v.pre = Pre("beta")
        assert v.pre == "beta"

        # should work for strings
        v.pre = "beta"
        assert v.pre == "beta"

        # should not delete major, patch, or build versions
        assert v.major == 0 and v.minor == 0 and v.patch == 0

    def test_build_setter(self):
        v = Version(0, 0, 0, pre="alpha", build="build")
        v.build = Build("meta")
        assert v.build == "meta"

        # should work for strings
        v.build = "build"
        assert v.build == "build"

        # should not delete major, patch, or build versions
        assert v.major == 0 and v.minor == 0 and v.patch == 0

    @pytest.mark.parametrize(
        "v, true",
        [
            (Version(0, 0, 0, "4.6.x"), False),
            (Version(0, 0, 0, "beta.56"), False),
            (Version(0, 0, 0, "alpha"), True),
            (Version(0, 0, 0, "alphab"), False),
            (Version(0, 0, 0, "alpha.5"), True),
            (Version(0, 0, 0, "alpha.x.4.x"), True),
            (Version(0, 0, 0, "alpha0.x"), True),
            (Version(0, 0, 0, "a0"), True),
            (Version(0, 0, 0, "ab"), False),
            (Version(0, 0, 0, "ab2"), False),
        ],
    )
    def test_is_alpha(self, v, true):
        assert v.is_alpha == true

    @pytest.mark.parametrize(
        "v, true",
        [
            (Version(0, 0, 0, "4.6.x"), False),
            (Version(0, 0, 0, "beta.56"), True),
            (Version(0, 0, 0, "beta"), True),
            (Version(0, 0, 0, "beta0"), True),
            (Version(0, 0, 0, "alpha.5"), False),
            (Version(0, 0, 0, "beta.x.4.x"), True),
            (Version(0, 0, 0, "alpha0.x"), False),
            (Version(0, 0, 0, "rc.x"), False),
            (Version(0, 0, 0, "b24"), True),
            (Version(0, 0, 0, "betab"), False),
            (Version(0, 0, 0, "bb8"), False),
        ],
    )
    def test_is_beta(self, v, true):
        assert v.is_beta == true

    @pytest.mark.parametrize(
        "v, true",
        [
            (Version(0, 0, 0, "4.6.x"), False),
            (Version(0, 0, 0, "beta.56"), False),
            (Version(0, 0, 0, "beta"), False),
            (Version(0, 0, 0, "alpha.5"), False),
            (Version(0, 0, 0, "beta.x.4.x"), False),
            (Version(0, 0, 0, "rc.x"), True),
            (Version(0, 0, 0, "rc.2.x.4"), True),
            (Version(0, 0, 0, "rc"), True),
            (Version(0, 0, 0, "rc6.2"), True),
            (Version(0, 0, 0, "rcd"), False),
        ],
    )
    def test_is_rc(self, v, true):
        assert v.is_rc == true

    @pytest.mark.parametrize(
        "v, true",
        [
            (Version(0, 0, 0, "4.6.x"), False),
            (Version(0, 0, 0, "beta.56"), False),
            (Version(0, 0, 0, "beta"), False),
            (Version(0, 0, 0, "alpha.5"), False),
            (Version(0, 0, 0, "beta.x.4.x"), False),
            (Version(0, 0, 0, "rc.x"), False),
            (Version(0, 0, 0, "rc.2.x.4", build="meta2xb2"), False),
            (Version(0, 0, 0, "rc"), False),
            (Version(0, 0, 0, "rc6.2"), False),
            (Version(0, 0, 0, "rcd"), False),
            (Version(0, 0, 0, "betab"), False),
            (Version(0, 0, 0, "bb8"), False),
            (Version(0, 0, 0, "alpha.x.4.x", build="meta"), False),
            (Version(0, 0, 0, "alpha0.x"), False),
            (Version(0, 0, 0, "a0"), False),
            (Version(0, 0, 0, "ab"), False),
            (Version(0, 0, 0, "ab2"), False),
            (Version(0, 2, 3, build="build293"), False),
            (Version(0, 1, 5), True),
            (Version(2, 1, 1), True),
        ],
    )
    def test_is_final(self, v, true):
        assert v.is_final == true

    @pytest.mark.parametrize(
        "v, true",
        [
            (Version(0, 0, 0, "4.6.x"), False),
            (Version(0, 0, 0, "beta.56"), False),
            (Version(1, 0, 0, "beta"), False),
            (Version(1, 0, 0, "alpha.5"), False),
            (Version(1, 0, 0, "beta.x.4.x"), False),
            (Version(0, 0, 0, "rc.x"), False),
            (Version(1, 0, 0, "rc.2.x.4", build="meta2xb2"), False),
            (Version(0, 0, 0, "rc"), False),
            (Version(1, 0, 0, "rc6.2"), False),
            (Version(1, 0, 0, "rcd"), False),
            (Version(0, 0, 0, "betab"), False),
            (Version(0, 0, 0, "bb8"), False),
            (Version(0, 0, 0, "alpha.x.4.x", build="meta"), False),
            (Version(1, 0, 0, "alpha0.x"), False),
            (Version(1, 0, 0, "a0"), False),
            (Version(1, 0, 0, "ab"), False),
            (Version(1, 0, 0, "ab2"), False),
            (Version(0, 2, 3, build="build293"), False),
            (Version(0, 1, 5), False),
            (Version(1, 0, 0, build="abcd2"), False),
            (Version(2, 1, 1), True),
            (Version(1, 0, 0), True),
        ],
    )
    def test_is_stable(self, v, true):
        assert v.is_stable == true


def test_reset():
    v = Version(6, 11, 23, pre="rc.6", build="meta")
    v.reset()

    assert (
        v.major == 0
        and v.minor == 0
        and v.patch == 0
        and v.pre is None
        and v.build is None
    )


class TestOperators:
    @pytest.mark.parametrize("bad", [0.2, 4 + 3j, "abc", object])
    def test_wrong_type(self, bad):
        v = Version(2, 3, 1, pre="alpha", build="meta")

        with pytest.raises(
            TypeError,
            match="Must be compared with another Version object, not {}".format(
                type(bad)
            ),
        ):
            v < bad

        with pytest.raises(
            TypeError,
            match="Must be compared with another Version object, not {}".format(
                type(bad)
            ),
        ):
            v > bad

        with pytest.raises(
            TypeError,
            match="Must be compared with another Version object, not {}".format(
                type(bad)
            ),
        ):
            v == bad

        with pytest.raises(
            TypeError,
            match="Must be compared with another Version object, not {}".format(
                type(bad)
            ),
        ):
            v != bad

        with pytest.raises(
            TypeError,
            match="Must be compared with another Version object, not {}".format(
                type(bad)
            ),
        ):
            v <= bad

        with pytest.raises(
            TypeError,
            match="Must be compared with another Version object, not {}".format(
                type(bad)
            ),
        ):
            v >= bad

    @pytest.mark.parametrize(
        "lhs, rhs",
        [
            (Version(4, 5, 6), Version(4, 5, 6)),
            (Version(1, 4, 5, pre="alpha.1"), Version(1, 4, 5, pre="alpha.1")),
            (
                Version(6, 2, 4, build="meta2"),
                Version(6, 2, 4, build="meta3"),
            ),  # build should be ignored
            (
                Version(4, 5, 1, pre="beta.5", build="meta1"),
                Version(4, 5, 1, pre="beta.5", build="meta2"),
            ),
        ],
    )
    def test_eq(self, lhs, rhs):
        assert lhs == rhs

    @pytest.mark.parametrize(
        "lhs, rhs",
        [
            (Version(4, 4, 6), Version(4, 5, 6)),
            (Version(1, 4, 5, pre="beta.1"), Version(1, 4, 5, pre="alpha.1")),
            (
                Version(6, 2, 4, build="meta2"),
                Version(6, 2, 5, build="meta3"),
            ),  # build should be ignored
            (
                Version(4, 5, 1, pre="beta.5", build="meta1"),
                Version(4, 5, 1, pre="beta.7", build="meta2"),
            ),
        ],
    )
    def test_ne(self, lhs, rhs):
        assert lhs != rhs

    def test_lt_chain(self):
        assert (
            Version(1, 0, 0, "alpha")
            < Version(1, 0, 0, "alpha.1")
            < Version(1, 0, 0, "alpha.beta")
            < Version(1, 0, 0, "beta")
            < Version(1, 0, 0, "beta.2")
            < Version(1, 0, 0, "beta.11")
            < Version(1, 0, 0, "rc.1")
            < Version(1, 0, 0)
            < Version(1, 0, 1, "beta.1")
            < Version(1, 0, 1, "rc.6")
            < Version(1, 0, 1)
            < Version(1, 2, 0)
            < Version(2, 0, 0)
        )

    def test_le_chain(self):
        assert (
            Version(1, 0, 0, "alpha")
            <= Version(1, 0, 0, "alpha.1")
            <= Version(1, 0, 0, "alpha.beta")
            <= Version(1, 0, 0, "alpha.beta")
            <= Version(1, 0, 0, "beta")
            <= Version(1, 0, 0, "beta.2")
            <= Version(1, 0, 0, "beta.2", build="meta22")
            <= Version(1, 0, 0, "beta.2", build="meta69")
            <= Version(1, 0, 0, "beta.11")
            <= Version(1, 0, 0, "rc.1")
            <= Version(1, 0, 0, build="5ad891")
            <= Version(1, 0, 0)
            <= Version(1, 0, 1, "beta.1")
            <= Version(1, 0, 1, "rc.6")
            <= Version(1, 0, 1)
            <= Version(1, 2, 0)
            <= Version(2, 0, 0)
        )

    def test_gt_chain(self):
        assert (
            Version(2, 0, 0)
            > Version(1, 2, 0)
            > Version(1, 0, 1)
            > Version(1, 0, 1, "rc.6")
            > Version(1, 0, 1, "beta.1")
            > Version(1, 0, 0)
            > Version(1, 0, 0, "rc.1")
            > Version(1, 0, 0, "beta.11")
            > Version(1, 0, 0, "beta.2")
            > Version(1, 0, 0, "beta")
            > Version(1, 0, 0, "alpha.beta")
            > Version(1, 0, 0, "alpha.1")
            > Version(1, 0, 0, "alpha")
        )

    def test_ge_chain(self):
        assert (
            Version(2, 0, 0)
            >= Version(1, 2, 0)
            >= Version(1, 0, 1)
            >= Version(1, 0, 1, "rc.6")
            >= Version(1, 0, 1, "beta.1")
            >= Version(1, 0, 0)
            >= Version(1, 0, 0, build="5ad891")
            >= Version(1, 0, 0, "rc.1")
            >= Version(1, 0, 0, "beta.11")
            >= Version(1, 0, 0, "beta.2", build="meta22")
            >= Version(1, 0, 0, "beta.2")
            >= Version(1, 0, 0, "beta.2", build="meta69")
            >= Version(1, 0, 0, "beta")
            >= Version(1, 0, 0, "alpha.beta")
            >= Version(1, 0, 0, "alpha.1")
            >= Version(1, 0, 0, "alpha")
        )


@pytest.mark.parametrize("bad", [5, "str", 4.2, object, 2 + 1j, VRm.BUILD, VRm.PRE])
def test_bad_inc_dec_pos(bad):
    v = Version(2, 5, 3, pre="beta.45", build="meta")
    with pytest.raises(
        InvalidPositionException,
        match=re.escape("Unrecognized version position: {}".format(bad)),
    ):
        v.inc(bad)


class TestInc:
    def test_major(self):
        v = Version(2, 5, 3, pre="beta.5", build="meta")
        v.inc(VPos.MAJOR)

        assert v.major == 3
        assert v.minor == 0
        assert v.patch == 0
        assert v.pre == "beta.5"
        assert v.build == "meta"

    def test_minor(self):
        v = Version(2, 5, 3, pre="beta.5", build="meta")
        v.inc(VPos.MINOR)

        assert v.major == 2
        assert v.minor == 6
        assert v.patch == 0
        assert v.pre == "beta.5"
        assert v.build == "meta"

    def test_patch(self):
        v = Version(2, 5, 3, pre="beta.5", build="meta")
        v.inc(VPos.PATCH)

        assert v.major == 2
        assert v.minor == 5
        assert v.patch == 4
        assert v.pre == "beta.5"
        assert v.build == "meta"

    @pytest.mark.parametrize("v", [Version(2, 5, 3, build="meta"), Version(2, 5, 3)])
    def test_pre_error_if_no_pre(self, v):
        with pytest.raises(
            NoValueException,
            match=re.escape("Object has no pre-release label: {}".format(repr(v))),
        ):
            v.inc(VPos.PRE)

    @pytest.mark.parametrize(
        "v",
        [
            Version(2, 5, 3, build="meta", pre="alpha1"),
            Version(2, 5, 3, pre="0-alpha-0"),
        ],
    )
    def test_pre_error_if_no_pre_digit(self, v):
        with pytest.raises(
            NoValueException,
            match=re.escape(
                (
                    "No digit to increment/decrement. Make sure the last "
                    "dot-separated identifier is a numeric value: {}".format(v.pre)
                )
            ),
        ):
            v.inc(VPos.PRE)

    def test_pre(self):
        v = Version(2, 5, 3, pre="beta.5", build="meta")
        v.inc(VPos.PRE)

        assert v.major == 2
        assert v.minor == 5
        assert v.patch == 3
        assert v.pre == "beta.6"
        assert v.build == "meta"


class TestDec:
    def test_major(self):
        v = Version(2, 5, 3, pre="beta.5", build="meta")
        v.dec(VPos.MAJOR)

        assert v.major == 1
        assert v.minor == 5
        assert v.patch == 3
        assert v.pre == "beta.5"
        assert v.build == "meta"

    def test_minor(self):
        v = Version(2, 5, 3, pre="beta.5", build="meta")
        v.dec(VPos.MINOR)

        assert v.major == 2
        assert v.minor == 4
        assert v.patch == 3
        assert v.pre == "beta.5"
        assert v.build == "meta"

    def test_patch(self):
        v = Version(2, 5, 3, pre="beta.5", build="meta")
        v.dec(VPos.PATCH)

        assert v.major == 2
        assert v.minor == 5
        assert v.patch == 2
        assert v.pre == "beta.5"
        assert v.build == "meta"

    @pytest.mark.parametrize("v", [Version(2, 5, 3, build="meta"), Version(2, 5, 3)])
    def test_pre_error_if_no_pre(self, v):
        with pytest.raises(
            NoValueException,
            match=re.escape("Object has no pre-release label: {}".format(repr(v))),
        ):
            v.dec(VPos.PRE)

    @pytest.mark.parametrize(
        "v",
        [
            Version(2, 5, 3, build="meta", pre="alpha1"),
            Version(2, 5, 3, pre="0-alpha-0"),
        ],
    )
    def test_pre_error_if_no_pre_digit(self, v):
        with pytest.raises(
            NoValueException,
            match=re.escape(
                (
                    "No digit to increment/decrement. Make sure the last "
                    "dot-separated identifier is a numeric value: {}".format(v.pre)
                )
            ),
        ):
            v.dec(VPos.PRE)

    def test_pre(self):
        v = Version(2, 5, 3, pre="beta.5", build="meta")
        v.dec(VPos.PRE)

        assert v.major == 2
        assert v.minor == 5
        assert v.patch == 3
        assert v.pre == "beta.4"
        assert v.build == "meta"

    @pytest.mark.parametrize(
        "v, dec",
        [
            (Version(0, 1, 5, pre="alpha", build="meta"), VPos.MAJOR),
            (Version(2, 0, 3, pre="alpha", build="meta"), VPos.MINOR),
            (Version(2, 4, 0, pre="alpha", build="meta"), VPos.PATCH),
            (Version(2, 4, 0, pre="alpha.0", build="meta"), VPos.PRE),
        ],
    )
    def test_dec_neg_error(self, v, dec):
        with pytest.raises(
            NegativeValueException,
            match=re.escape("Cannot decrement number to a negative value"),
        ):
            v.dec(dec)


def test_remove_pre():
    v = Version(2, 1, 5, pre="alpha.2.5", build="build")
    v.remove_pre()
    assert str(v) == "2.1.5+build"


def test_remove_build():
    v = Version(2, 1, 5, pre="alpha.2.5", build="build")
    v.remove_build()
    assert str(v) == "2.1.5-alpha.2.5"


def test_remove_pre_build():
    v = Version(2, 1, 5, pre="alpha.2.5", build="build")
    v.remove_build()
    v.remove_pre()
    assert str(v) == "2.1.5"


@pytest.mark.parametrize(
    "other",
    [
        VRm.BUILD,
        5,
        3 + 2j,
        3.6,
    ],
)
def test_bad_add(other):
    v = Version(0, 0, 0)
    with pytest.raises(
        TypeError,
        match=re.escape("Unsupported rhs type for +: '{}'".format(type(other))),
    ):
        v + other


@pytest.mark.parametrize(
    "other",
    [
        5,
        3 + 2j,
        3.6,
    ],
)
def test_bad_sub(other):
    v = Version(0, 0, 0)
    with pytest.raises(
        TypeError,
        match=re.escape("Unsupported rhs type for -: '{}'".format(type(other))),
    ):
        v - other


class TestAdd:
    @pytest.mark.parametrize("string", ["asdf", "52", "*dd"])
    def test_error_unknown_string(self, string):
        v = Version(0, 0, 0)
        with pytest.raises(
            InvalidOperationException,
            match=re.escape("Cannot add an invalid string"),
        ):
            v + string

    def test_error_adding_pre_release_exist(self):
        v = Version(0, 0, 0, pre="d2319c")
        with pytest.raises(
            InvalidOperationException,
            match=re.escape("Cannot add pre-release that already exists"),
        ):
            v + "-dea92c"

        v = Version(0, 0, 0, pre="d2319c", build="meta")
        with pytest.raises(
            InvalidOperationException,
            match=re.escape("Cannot add pre-release that already exists"),
        ):
            v + "-dea92c"

    def test_error_adding_meta_exist(self):
        v = Version(0, 0, 0, build="d2319c")
        with pytest.raises(
            InvalidOperationException,
            match=re.escape("Cannot add build metadata that already exists"),
        ):
            v + "+dea92c"

        v = Version(0, 0, 0, pre="d2319c", build="meta")
        with pytest.raises(
            InvalidOperationException,
            match=re.escape("Cannot add build metadata that already exists"),
        ):
            v + "+dea92c"

    @pytest.mark.parametrize(
        "orig, res, pos",
        [
            (
                Version(1, 1, 1, pre="alpha.3", build="meta"),
                "2.0.0-alpha.3+meta",
                VPos.MAJOR,
            ),
            (
                Version(1, 1, 1, pre="alpha.3", build="meta"),
                "1.2.0-alpha.3+meta",
                VPos.MINOR,
            ),
            (
                Version(1, 1, 1, pre="alpha.3", build="meta"),
                "1.1.2-alpha.3+meta",
                VPos.PATCH,
            ),
            (
                Version(1, 1, 1, pre="alpha.3", build="meta"),
                "1.1.1-alpha.4+meta",
                VPos.PRE,
            ),
        ],
    )
    def test_valid_inc(self, orig, res, pos):
        assert res == str(orig + pos)

    @pytest.mark.parametrize(
        "v, add, res",
        [
            (Version(1, 1, 1), "-alpha.1", "1.1.1-alpha.1"),
            (
                Version(1, 1, 1, build="meta"),
                "-alpha.1",
                "1.1.1-alpha.1+meta",
            ),
        ],
    )
    def test_valid_pre(self, v, add, res):
        assert res == str(v + add)
        assert v.pre == add[1:]

    @pytest.mark.parametrize(
        "v, add, res",
        [
            (Version(1, 1, 1), "+21bk8", "1.1.1+21bk8"),
            (
                Version(1, 1, 1, pre="alpha.1"),
                "+2.b92",
                "1.1.1-alpha.1+2.b92",
            ),
        ],
    )
    def test_valid_build(self, v, add, res):
        assert res == str(v + add)
        assert v.build == add[1:]


class TestSub:
    def test_error_remove_non_existent_pre(self):
        v = Version(0, 0, 0)
        with pytest.raises(
            InvalidOperationException,
            match=re.escape(
                "Cannot remove pre-release that does not exist: {}".format(repr(v))
            ),
        ):
            v - VRm.PRE

        v = Version(0, 0, 0, build="abc")
        with pytest.raises(
            InvalidOperationException,
            match=re.escape(
                "Cannot remove pre-release that does not exist: {}".format(repr(v))
            ),
        ):
            v - VRm.PRE

    def test_error_remove_non_existent_meta(self):
        v = Version(0, 0, 0)
        with pytest.raises(
            InvalidOperationException,
            match=re.escape(
                "Cannot remove build metadata that does not exist: {}".format(repr(v))
            ),
        ):
            v - VRm.BUILD

        v = Version(0, 0, 0, pre="abc")
        with pytest.raises(
            InvalidOperationException,
            match=re.escape(
                "Cannot remove build metadata that does not exist: {}".format(repr(v))
            ),
        ):
            v - VRm.BUILD

    @pytest.mark.parametrize(
        "orig, res, pos",
        [
            (
                Version(1, 1, 1, pre="alpha.3", build="meta"),
                "0.1.1-alpha.3+meta",
                VPos.MAJOR,
            ),
            (
                Version(1, 1, 1, pre="alpha.3", build="meta"),
                "1.0.1-alpha.3+meta",
                VPos.MINOR,
            ),
            (
                Version(1, 1, 1, pre="alpha.3", build="meta"),
                "1.1.0-alpha.3+meta",
                VPos.PATCH,
            ),
            (
                Version(1, 1, 1, pre="alpha.3", build="meta"),
                "1.1.1-alpha.2+meta",
                VPos.PRE,
            ),
        ],
    )
    def test_valid_inc(self, orig, res, pos):
        assert res == str(orig - pos)

    @pytest.mark.parametrize(
        "rem, res",
        [
            (Version(1, 1, 1, pre="abc"), "1.1.1"),
            (Version(1, 1, 1, pre="alpha.6", build="meta"), "1.1.1+meta"),
        ],
    )
    def test_valid_rm_pre(self, rem, res):
        assert res == str(rem - VRm.PRE)
        assert rem.pre is None

    @pytest.mark.parametrize(
        "rem, res",
        [
            (Version(1, 1, 1, build="abc"), "1.1.1"),
            (
                Version(1, 1, 1, pre="alpha.6", build="meta"),
                "1.1.1-alpha.6",
            ),
        ],
    )
    def test_valid_rm_build(self, rem, res):
        assert res == str(rem - VRm.BUILD)
        assert rem.build is None


def test_chain():
    v = Version(10, 10, 10)
    (
        v
        + VPos.MAJOR  # 11.0.0
        + VPos.MAJOR  # 12.0.0
        + VPos.MINOR  # 12.1.0
        + VPos.MAJOR  # 13.0.0
        + VPos.PATCH  # 13.0.1
        + VPos.PATCH  # 13.0.2
        + "+build1"  # 13.0.2+build1
        + "-pre.12"  # 13.0.2-pre.12+build1
        + VPos.MINOR  # 13.1.0-pre.12+build1
        - VPos.MAJOR  # 12.1.0-pre.12+build1
        + VPos.PATCH  # 12.1.1-pre.12+build1
        - VPos.PRE  # 12.1.1-pre.11+build1
    )

    assert str(v) == "12.1.1-pre.11+build1"

    v - VRm.BUILD - VRm.PRE

    assert str(v) == "12.1.1"


def test_bad_chain():
    """
    Should raise first error
    """

    v = Version(10, 10, 10)
    with pytest.raises(
        InvalidOperationException,
        match=re.escape(
            (
                "Cannot remove build metadata that does not exist: "
                "Version(major=13, minor=0, patch=2, pre=None, build=None)"
            )
        ),
    ):
        (
            v
            + VPos.MAJOR  # 11.0.0
            + VPos.MAJOR  # 12.0.0
            + VPos.MINOR  # 12.1.0
            + VPos.MAJOR  # 13.0.0
            + VPos.PATCH  # 13.0.1
            + VPos.PATCH  # 13.0.2
            - VRm.BUILD  # first error - should stop here
            - "-pre.12"
            + VPos.MINOR
            - VPos.MAJOR
            + VPos.PATCH
            - VPos.PRE
        )


@pytest.mark.parametrize(
    "bad",
    [
        "1",
        "1.2",
        "1.2.3-0123",
        "1.2.3-0123.0123",
        "1.1.2+.123",
        "+invalid",
        "-invalid",
        "-invalid+invalid",
        "-invalid.01",
        "alpha",
        "alpha.beta",
        "alpha.beta.1",
        "alpha.1",
        "alpha+beta",
        "alpha_beta",
        "alpha.",
        "alpha..",
        "beta",
        "1.0.0-alpha_beta",
        "-alpha.",
        "1.0.0-alpha..",
        "1.0.0-alpha..1",
        "1.0.0-alpha...1",
        "1.0.0-alpha....1",
        "1.0.0-alpha.....1",
        "1.0.0-alpha......1",
        "1.0.0-alpha.......1",
        "01.1.1",
        "1.01.1",
        "1.1.01",
        "1.2",
        "1.2.3.DEV",
        "1.2-SNAPSHOT",
        "1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788",
        "1.2-RC-SNAPSHOT",
        "-1.0.3-gamma+b7718",
        "+justmeta",
        "9.8.7+meta+meta",
        "9.8.7-whatever+meta+meta",
        (
            "99999999999999999999999.999999999999999999.99999999999999999"
            "----RC-SNAPSHOT.12.09.1--------------------------------..12"
        ),
    ],
)
def test_bad_parse(bad):
    with pytest.raises(
        ParseException,
        match=re.escape("Invalid semantic version string: {}".format(bad)),
    ):
        parse_version(bad)


@pytest.mark.parametrize(
    "v",
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
        "1.0.0-alpha0.valid",
        "1.0.0-alpha.0valid",
        "1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay",
        "1.0.0-rc.1+build.1",
        "2.0.0-rc.1+build.123",
        "1.2.3-beta",
        "10.2.3-DEV-SNAPSHOT",
        "1.2.3-SNAPSHOT-123",
        "1.0.0",
        "2.0.0",
        "1.1.7",
        "2.0.0+build.1848",
        "2.0.1-alpha.1227",
        "1.0.0-alpha+beta",
        "1.2.3----RC-SNAPSHOT.12.9.1--.12+788",
        "1.2.3----R-S.12.9.1--.12+meta",
        "1.2.3----RC-SNAPSHOT.12.9.1--.12",
        "1.0.0+0.build.1-rc.10000aaa-kk-0.1",
        "99999999999999999999999.999999999999999999.99999999999999999",
        "1.0.0-0A.is.legal",
    ],
)
def test_parse(v):
    assert str(parse_version(v)) == v
