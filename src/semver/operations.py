"""
Version operations on string objects
"""

import re
import typing as t

from .constants import EXC_INVALID_POS, EXC_PRE_NO_VALUE_2, RE_FULL, VPos, VRm
from .exc import InvalidPositionException, NoValueException
from .version import Version, parse_version


def add(version: str, *operations: t.Union[VPos, str]) -> str:
    """The Version + operator on a string representing a version

    Args:
        version (str): A version string; must not include 'v' in beginning
        *operations (Union[VPos, str]): Operations to perform on \
        the version string; should be the same as the rhs of the + \
        operator

    Returns:
        str: The version string after adding args from *operations
    """

    v = parse_version(version)
    for operation in operations:
        v + operation

    return str(v)


def bump(version: str, pos: VPos, amt: int = 1, carry: bool = True) -> str:
    """Bumps version position given in pos by amt

    Args:
        version (str): A version string; must not include 'v' in beginning
        pos (VPos): The position (MAJOR, MINOR, PATCH, PRE) to bump (Note that bumping \
        PRE is more ineffecient.)
        amt (int, optional): The amount to bump the position by. Defaults to 1.
        carry (bool, optional): If bumping the position should reset the positions \
        to the right of it (setting minor or patch version to 0, removing pre-release \
        label). Note that calling bump(pos=VPos.PRE, carry=True) is the same as if \
        carry is False. Defaults to True.

    Returns:
        str: A string representing the bumped version
    """

    ret = parse_version(version)

    if pos == VPos.PRE:
        if not ret.has_pre:
            raise NoValueException(EXC_PRE_NO_VALUE_2.format(repr(ret)))

        for _ in range(amt):
            ret.inc(VPos.PRE)

        return str(ret)

    # order of positions
    order = (VPos.MAJOR, VPos.MINOR, VPos.PATCH, VPos.PRE)

    # increment pos by amount
    if pos == VPos.MAJOR:
        ret.major += amt
    elif pos == VPos.MINOR:
        ret.minor += amt
    elif pos == VPos.PATCH:
        ret.patch += amt
    else:
        raise InvalidPositionException(EXC_INVALID_POS.format(pos))

    if not carry:
        return str(ret)

    # reset positions to right if carry is True
    ind = order.index(pos)
    for i in order[ind + 1 :]:
        if i == VPos.MINOR:
            ret.minor = 0
        elif i == VPos.PATCH:
            ret.patch = 0
        else:
            ret.pre = None

    return str(ret)


def clean(version: str) -> str:
    """Cleans version string by stripping whitespaces and \
        removing 'v' or '=' characters at the beginning of the string.

    Note that this does not check for errors in the cleaned up string. \
    It is recommended to check that the string is valid using the valid() \
    function.

    Args:
        version (str): Version string to clean up

    Returns:
        str: Cleaned up version string
    """

    version = version.strip()
    version = re.sub(r"^[v=]+", r"", version)
    return version


def clean_and_parse(version: str) -> Version:
    """Cleans version string by stripping whitespaces and \
        removing 'v' or '=' characters at the beginning of the string, \
        then parses the string into a Version class.

    Args:
        version (str): Version string to clean up and parse

    Returns:
        Version: parsed Version object of cleaned up string (if it is valid)
    """

    string = clean(version)
    return parse_version(string)


def compare(lhs: str, rhs: str) -> int:
    """Compares lhs are rhs version strings

    * If lhs == rhs (in terms of versioning), returns 0
    * If lhs < rhs (in terms of versioning), returns -1
    * If lhs > rhs (in terms of versioning), returns 1

    Args:
        lhs (str): A version string; must not include 'v' in beginning
        rhs (str): A version string; must not include 'v' in beginning

    Returns:
        int: The result of the comparison
    """

    vlhs = parse_version(lhs)
    vrhs = parse_version(rhs)

    if vlhs == vrhs:
        return 0
    elif vlhs < vrhs:
        return -1
    else:
        return 1


def get_build(version: str) -> t.Optional[str]:
    """Gets the build label from the version string

    Args:
        version (str): A version string; must not include 'v' in beginning

    Returns:
        t.Optional[str]: The build label, or None if it does not have one
    """

    v = parse_version(version)
    return v.build


def get_major(version: str) -> int:
    """Gets the major version number from the version string

    Args:
        version (str): A version string; must not include 'v' in beginning

    Returns:
        int: The major version number
    """

    v = parse_version(version)
    return v.major


def get_minor(version: str) -> int:
    """Gets the minor version number from the version string

    Args:
        version(str): A version string; must not include 'v' in beginning

    Returns:
        int: The minor version number
    """

    v = parse_version(version)
    return v.minor


def get_patch(version: str) -> int:
    """Gets the patch version number from the version string

    Args:
        version(str): A version string; must not include 'v' in beginning

    Returns:
        int: The patch version number
    """

    v = parse_version(version)
    return v.patch


def get_pre(version: str) -> t.Optional[str]:
    """Gets the pre-release label from the version string

    Args:
        version (str): A version string; must not include 'v' in beginning

    Returns:
        t.Optional[str]: The pre-release label, or None if it does not have one
    """

    v = parse_version(version)
    return v.pre


def get_pre_digit(version: str) -> t.Optional[int]:
    """Gets the number in the rightmost dot-separated identifier in the pre-release

    Args:
        version (str): A version string; must not include 'v' in beginning

    Returns:
        t.Optional[str]: The pre-release digit, or None if it does not have one
    """

    v = parse_version(version)
    return v.pre_digit


def set_build(version: str, build: str) -> str:
    """Sets the build label in the version string

    Args:
        version (str): A version string; must not include 'v' in beginning
        build (str): The build label to set in the string \
                (must not include '+' in beginning)

    Returns:
        str: The string with the build label set
    """

    v = parse_version(version)
    v.build = build
    return str(v)


def set_major(version: str, major: int) -> str:
    """Sets the major version in the version string

    Args:
        version (str): A version string; must not include 'v' in beginning
        major (int): The major version to set

    Returns:
        str: The version string with the new major version
    """

    v = parse_version(version)
    v.major = major
    return str(v)


def set_minor(version: str, minor: int) -> str:
    """Sets the minor version in the version string

    Args:
        version (str): A version string; must not include 'v' in beginning
        minor (int): The minor version to set

    Returns:
        str: The version string with the new minor version
    """

    v = parse_version(version)
    v.minor = minor
    return str(v)


def set_patch(version: str, patch: int) -> str:
    """Sets the patch version in the version string

    Args:
        version (str): A version string; must not include 'v' in beginning
        patch (int): The patch version to set

    Returns:
        str: The version string with the new patch version
    """

    v = parse_version(version)
    v.patch = patch
    return str(v)


def set_pre(version: str, pre: str) -> str:
    """Sets the pre-release label in the version string

    Args:
        version (str): A version string; must not include 'v' in beginning
        pre (str): The pre-release label to set in the string \
                (must not include '-' in beginning)

    Returns:
        str: The string with the pre-release label set
    """

    v = parse_version(version)
    v.pre = pre
    return str(v)


def sub(version: str, *operations: t.Union[VPos, VRm]) -> str:
    """The Version - operator on a string representing a version

    Args:
        version (str): A version string; must not include 'v' in beginning
        *operations (Union[VPos, str]): Operations to perform on \
        the version string; should be the same as the rhs of the - \
        operator

    Returns:
        str: The version string after subtracting args from *operations
    """

    v = parse_version(version)
    for operation in operations:
        v - operation

    return str(v)


def update(version: str, *operations: t.Union[VPos, VRm, str]) -> str:
    """Performs a series of operations on given version string

    Allowed operations are:

    * Bumping major, minor, patch, or pre-release numbers (if a pre-release exists \
    and it has a number)
    * Adding a pre-release or build label if they don't exist already
    * Removing a pre-release or build label if they exist

    Decrementing a release number is not supported.

    Args:
        version (str): A version string; must not include 'v' in beginning
        *operations(Union[VPos, VRm, str]): The series of operations to perform on \
        the version string, from left to right. If VPos or str, should be equivalent \
        to the rhs of the + operator. If VRm, should be equivalent to the rhs of the \
        - operator.

    Returns:
        str: The version string after performing the operations
    """

    v = parse_version(version)
    for operation in operations:
        if isinstance(operation, (VPos, str)):
            # bumping or adding string; use + operator
            v + operation
        else:
            # VRm; use - operator
            v - operation

    return str(v)


def valid(version: str) -> bool:
    """If the given version string is a valid semantic version

    Args:
        version (str): Any string

    Returns:
        bool: If the string is a valid semantic version
    """

    if not isinstance(version, str):
        return False

    parsed = re.match(RE_FULL, version)

    return parsed is not None
