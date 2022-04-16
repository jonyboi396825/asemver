import pytest
from semver.constants import VPos, VRm
from semver.operations import add, sub, update

"""
add(), sub(), update(), bump()
"""


@pytest.mark.parametrize(
    "v, res, op",
    [
        ("2.5.5", "2.6.1", (VPos.MINOR, VPos.PATCH)),
        (
            "4.2.9",
            "5.2.1-alpha.5",
            (VPos.MAJOR, "-alpha.4", VPos.MINOR, VPos.PRE, VPos.MINOR, VPos.PATCH),
        ),
        ("5.2.6-alpha.6", "6.0.1-alpha.6+meta", (VPos.MAJOR, "+meta", VPos.PATCH)),
        ("2.3.4", "2.3.4-beta.2+meta49", ("+meta49", "-beta.2")),
    ],
)
def test_add(v, res, op):
    assert res == add(v, *op)


@pytest.mark.parametrize(
    "v, res, op",
    [
        ("2.5.5", "1.3.4", (VPos.PATCH, VPos.MINOR, VPos.MAJOR, VPos.MINOR)),
        (
            "2.5.5-alpha.6",
            "1.3.4",
            (VPos.PATCH, VPos.MINOR, VPos.MAJOR, VRm.PRE, VPos.MINOR),
        ),
        (
            "2.5.5+meta.6",
            "1.3.4",
            (VPos.PATCH, VPos.MINOR, VPos.MAJOR, VRm.BUILD, VPos.MINOR),
        ),
        (
            "2.5.5-alpha.6+meta.6",
            "1.3.4",
            (VPos.PATCH, VPos.MINOR, VRm.PRE, VPos.MAJOR, VRm.BUILD, VPos.MINOR),
        ),
    ],
)
def test_sub(v, res, op):
    assert res == sub(v, *op)


@pytest.mark.parametrize(
    "v, res, op",
    [
        ("2.5.5", "2.6.1", (VPos.MINOR, VPos.PATCH)),
        (
            "2.5.5",
            "2.6.1-alpha.56+meta",
            ("+meta", VPos.MINOR, VPos.PATCH, "-alpha.56"),
        ),
        ("2.5.5-alpha.56+meta", "2.6.1", (VRm.BUILD, VPos.MINOR, VPos.PATCH, VRm.PRE)),
        (
            "2.5.7-alpha.65+meta.22",
            "3.3.1-beta.1",
            (
                VPos.MAJOR,
                VRm.PRE,
                VPos.MINOR,
                VRm.BUILD,
                VPos.MINOR,
                "-beta.0",
                VPos.PRE,
                VPos.MINOR,
                VPos.PATCH,
            ),
        ),
    ],
)
def test_update(v, res, op):
    assert res == update(v, *op)
