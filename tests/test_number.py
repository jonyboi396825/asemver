import pytest
import re
from semver.components import VersionNumber
from semver.exc import NegativeValueException


@pytest.mark.parametrize("bad_param", ["01", 3.6, 2 + 5j, -2.5, object])
def test_error_number_non_int(bad_param):
    with pytest.raises(
        TypeError,
        match=re.escape("Value must be a(n) int, not {}".format(type(bad_param))),
    ):
        VersionNumber(bad_param)


def test_error_when_neg_int():
    with pytest.raises(
        NegativeValueException, match=re.escape("Number must be positive: -5")
    ):
        VersionNumber(-5)


class TestOperators:
    @pytest.mark.parametrize("bad", [0.2, 4 + 3j, "abc", object])
    def test_wrong_type(self, bad):
        vn = VersionNumber(0)

        with pytest.raises(
            TypeError,
            match=(
                "Must be compared with another VersionNumber object,"
                " not {}".format(type(bad))
            ),
        ):
            vn < bad

        with pytest.raises(
            TypeError,
            match=(
                "Must be compared with another VersionNumber object,"
                " not {}".format(type(bad))
            ),
        ):
            vn > bad

        with pytest.raises(
            TypeError,
            match=(
                "Must be compared with another VersionNumber object,"
                " not {}".format(type(bad))
            ),
        ):
            vn == bad

        with pytest.raises(
            TypeError,
            match=(
                "Must be compared with another VersionNumber object,"
                " not {}".format(type(bad))
            ),
        ):
            vn != bad

        with pytest.raises(
            TypeError,
            match=(
                "Must be compared with another VersionNumber object,"
                " not {}".format(type(bad))
            ),
        ):
            vn <= bad

        with pytest.raises(
            TypeError,
            match=(
                "Must be compared with another VersionNumber object,"
                " not {}".format(type(bad))
            ),
        ):
            vn >= bad

    @pytest.mark.parametrize("n1, n2", [(0, 0), (56, 56), (2, 2)])
    def test_eq(self, n1, n2):
        assert VersionNumber(n1) == VersionNumber(n2)
        assert not VersionNumber(n1) < VersionNumber(n2)
        assert not VersionNumber(n1) > VersionNumber(n2)

    @pytest.mark.parametrize("n1, n2", [(0, 27), (16, 22), (55, 34)])
    def test_neq(self, n1, n2):
        assert VersionNumber(n1) != VersionNumber(n2)

    @pytest.mark.parametrize("n1, n2", [(0, 27), (16, 22), (34, 55)])
    def test_lt(self, n1, n2):
        assert VersionNumber(n1) < VersionNumber(n2)

    @pytest.mark.parametrize(
        "n1, n2", [(0, 27), (16, 22), (34, 55), (0, 0), (56, 56), (2, 2)]
    )
    def test_le(self, n1, n2):
        assert VersionNumber(n1) <= VersionNumber(n2)

    @pytest.mark.parametrize("n2, n1", [(0, 27), (16, 22), (34, 55)])
    def test_gt(self, n1, n2):
        assert VersionNumber(n1) > VersionNumber(n2)

    @pytest.mark.parametrize(
        "n2, n1", [(0, 27), (16, 22), (34, 55), (0, 0), (56, 56), (2, 2)]
    )
    def test_ge(self, n1, n2):
        assert VersionNumber(n1) >= VersionNumber(n2)


@pytest.mark.parametrize("orig, res", [(0, 1), (44, 45), (23, 24), (77, 78)])
def test_inc(orig, res):
    num = VersionNumber(orig)
    num.inc()
    assert num == VersionNumber(res)


@pytest.mark.parametrize("res, orig", [(0, 1), (44, 45), (23, 24), (77, 78)])
def test_dec(orig, res):
    num = VersionNumber(orig)
    num.dec()
    assert num == VersionNumber(res)


def test_dec_err():
    num = VersionNumber(0)
    with pytest.raises(
        NegativeValueException,
        match=re.escape("Cannot decrement number to a negative value"),
    ):
        num.dec()


@pytest.mark.parametrize(
    "first, res, seq",
    [
        (1, 6, [1, 1, 1, -1, 1, -1, 1, -1, 1, 1, 1]),
        (3, 3, [1, -1, 1, -1, 1, -1]),
        (3, 4, [1, -1, 1, -1, 1]),
    ],
)
def test_seq(first, res, seq):
    num = VersionNumber(first)

    for i in seq:
        if i > 0:
            num.inc()
        else:
            num.dec()

    assert num == VersionNumber(res)


@pytest.mark.parametrize("num", [0, 22, 4, 66])
def test_str(num):
    vnum = VersionNumber(num)

    assert str(vnum) == str(num)


@pytest.mark.parametrize(
    "num, rep",
    [
        (0, "VersionNumber(number=0)"),
        (22, "VersionNumber(number=22)"),
        (4, "VersionNumber(number=4)"),
        (66, "VersionNumber(number=66)"),
    ],
)
def test_repr(num, rep):
    vnum = VersionNumber(num)

    assert repr(vnum) == rep


@pytest.mark.parametrize("num", [0, 22, 4, 66])
def test_property(num):
    vnum = VersionNumber(num)

    assert vnum.number == num

    vnum.inc()
    assert vnum.number == num + 1

    vnum.dec()
    assert vnum.number == num


@pytest.mark.parametrize("num", [0, 22, 4, 66])
def test_setter(num):
    vnum = VersionNumber()

    assert vnum.number == 0

    vnum.number = num

    assert vnum.number == num


@pytest.mark.parametrize("bad_num", ["0", "aa", 3 + 5j, 4.4, -1.2, "fff"])
def test_setter_bad_type(bad_num):
    num = VersionNumber()

    with pytest.raises(
        TypeError,
        match=re.escape("Value must be a(n) int, not {}".format(type(bad_num))),
    ):
        num.number = bad_num


@pytest.mark.parametrize("bad_num", [-2, -55, -1, -3])
def test_setter_negative(bad_num):
    num = VersionNumber()

    with pytest.raises(
        NegativeValueException,
        match=re.escape("Number must be positive: {}".format(bad_num)),
    ):
        num.number = bad_num


@pytest.mark.parametrize("number", [0, 6])
def test_reset(number):
    num = VersionNumber(number)
    num.reset()

    assert num.number == 0
