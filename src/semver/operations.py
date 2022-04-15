"""
Version operations on string objects
"""

import typing as t

from .constants import VPos, VRm
from .version import parse_version


def add(version: str, *operations: t.Union[VPos, str]) -> str:
    """The Version + operator on a string representing a version

    Args:
        version (str): A version string
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


def sub(version: str, *operations: t.Union[VPos, VRm]) -> str:
    """The Version - operator on a string representing a version

    Args:
        version (str): A version string
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
        version (str): A version string
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


def compare(lhs: str, rhs: str) -> int:
    """Compares lhs are rhs version strings

    * If lhs == rhs (in terms of versioning), returns 0
    * If lhs < rhs (in terms of versioning), returns -1
    * If lhs > rhs (in terms of versioning), returns 1

    Args:
        lhs (str): A version string
        rhs (str): A version string

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
