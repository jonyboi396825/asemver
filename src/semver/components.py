"""
Component classes that form the final class

Includes:

* Version number class
* Pre-release class
* Build class
"""

import re
import typing as t

from .common import Core
from .constants import (
    EXC_CANNOT_DEC,
    EXC_INVALID_STR,
    EXC_MUST_CMP,
    EXC_MUST_POSITIVE,
    EXC_MUST_TYPE,
    EXC_PRE_NO_VALUE,
    RE_BUILD,
    RE_PRE,
)
from .exc import NegativeValueException, NoValueException, ParseException


class VersionNumber(Core):
    """A mutable wrapper of Python's int to represent a version number
    Objects of this class will raise an exception when decrementing the object \
    to a number below 0.
    """

    def __init__(self, number: int = 0) -> None:
        """Constructor

        Args:
            number (int, optional): The int to wrap. Defaults to 0.
        Raises:
            TypeError: If the number given is not of type int
            NegativeValueException: If the number given is negative
        """

        if not isinstance(number, int):
            raise TypeError(EXC_MUST_TYPE.format("int", type(number)))

        if number < 0:
            raise NegativeValueException(EXC_MUST_POSITIVE.format(number))

        self._number = number

    def __repr__(self) -> str:
        """repr of number"""

        return "VersionNumber(number={})".format(self._number)

    def __str__(self) -> str:
        """Prints number"""

        return str(self.number)

    def __eq__(self, other: object) -> bool:
        """Returns if numbers are equal"""

        if other is None:
            return False

        if not isinstance(other, VersionNumber):
            raise TypeError(EXC_MUST_CMP.format("VersionNumber", type(other)))

        return self.number == other.number

    def __lt__(self, other: object) -> bool:
        """Returns if current number is less than other"""

        if not isinstance(other, VersionNumber):
            raise TypeError(EXC_MUST_CMP.format("VersionNumber", type(other)))

        return self.number < other.number

    def inc(self) -> None:
        """Increments number by 1"""

        self._number += 1

    def dec(self) -> None:
        """Decrements number by 1

        Raises:
            NegativeValueException: If the number is 0 \
            (cannot decrement to a negative value)
        """

        if self._number == 0:
            raise NegativeValueException(EXC_CANNOT_DEC)

        self._number -= 1

    def reset(self) -> None:
        """Resets number to 0"""

        self._number = 0

    @property
    def number(self) -> int:
        """Returns the version number

        Setter:

        Sets the version number as long as it is an integer and it is positive
        """

        return self._number

    @number.setter
    def number(self, number: int) -> None:
        if not isinstance(number, int):
            raise TypeError(EXC_MUST_TYPE.format("int", type(number)))

        if number < 0:
            raise NegativeValueException(EXC_MUST_POSITIVE.format(number))

        self._number = number


class Pre(Core):
    """Represents a pre-release"""

    def __init__(self, string: str) -> None:
        """Constructor

        https://semver.org/spec/v2.0.0.html#spec-item-9

        The string does not need to start with a hyphen. If it does, then \
        the final version will add an extra hyphen when printing.

        Args:
            string (str): Pre-release string

        Raises:
            ParseException: If the pre-release string is invalid
        """

        self._string = self._check_then_set(string)

        # comparer list
        self._cmp = self._get_cmp_list(string)
        # digit to increment/decrement when inc() or dec() is called
        self._digit = self._cmp[-1] if isinstance(self._cmp[-1], int) else None

    def __repr__(self) -> str:
        """repr of Pre"""

        return "Pre(string='{}')".format(self._string)

    def __str__(self) -> str:
        """Returns string with hyphen at beginning"""

        return "-{}".format(self._string)

    def __eq__(self, other: t.Any) -> bool:
        """Compares if strings are equal"""

        if other is None:
            return False

        if not isinstance(other, Pre):
            raise TypeError(EXC_MUST_CMP.format("pre-release", type(other)))

        return self.string == other.string

    def __lt__(self, other: t.Any) -> bool:
        """Compares less than

        https://semver.org/spec/v2.0.0.html#spec-item-11
        """

        if not isinstance(other, Pre):
            raise TypeError(EXC_MUST_CMP.format("pre-release", type(other)))

        def cmp(lhs: t.Union[str, int], rhs: t.Union[str, int]) -> bool:
            if isinstance(lhs, int) and isinstance(rhs, int):
                return lhs < rhs
            elif isinstance(lhs, str) and isinstance(rhs, str):
                # separated because mypy
                return lhs < rhs
            elif isinstance(lhs, int):
                return True
            else:
                return False

        return self._calc_lt(self._cmp, other._cmp, cmp)

    def inc(self) -> None:
        """Increments digit by 1 if exists"""

        if self._digit is None:
            raise NoValueException(EXC_PRE_NO_VALUE.format(self._string))

        # make mypy happy
        assert isinstance(self._cmp[-1], int), "Last element of cmp is not int"

        # need to update comparison list along with digit and string
        self._digit += 1
        self._cmp[-1] += 1
        self._string = ".".join(map(str, self._cmp))

    def dec(self) -> None:
        """Decrements digits by 1 if exists and not 0"""

        if self._digit is None:
            raise NoValueException(EXC_PRE_NO_VALUE.format(self._string))

        if self._digit == 0:
            # cannot decrement into a negative value
            raise NegativeValueException(EXC_CANNOT_DEC)

        # make mypy happy
        assert isinstance(self._cmp[-1], int), "Last element of cmp is not int"

        # need to update comparison list along with digit and string
        self._digit -= 1
        self._cmp[-1] -= 1
        self._string = ".".join(map(str, self._cmp))

    def reset(self) -> None:
        """Resets to dash"""

        self._string = "-"
        self._cmp = ["-"]
        self._digit = None

    @property
    def string(self) -> str:
        """Returns the identifier string

        Setter:

        Sets the identifier string if valid, otherwise raises ParseException
        """

        return self._string

    @string.setter
    def string(self, string: str) -> None:
        # set string
        self._string = self._check_then_set(string)
        # comparer list
        self._cmp = self._get_cmp_list(string)
        # digit to increment/decrement when inc() or dec() is called
        self._digit = self._cmp[-1] if isinstance(self._cmp[-1], int) else None

    @property
    def digit(self) -> t.Optional[int]:
        """Returns the digit, if any, otherwise returns None"""

        return self._digit

    @property
    def is_alpha(self) -> bool:
        """Returns if first dot-separated identifier starts with 'alpha' or 'a' \
            (case insensitive), followed by an empty string or a digit
        """

        if not isinstance(self._cmp[0], str):
            return False

        if self._cmp[0].lower().startswith("alpha"):
            s = self._cmp[0][len("alpha") :]
            return s == "" or s.isdigit()

        if self._cmp[0].lower().startswith("a"):
            s = self._cmp[0][len("a") :]
            return s == "" or s.isdigit()

        return False

    @property
    def is_beta(self) -> bool:
        """Returns if first dot-separated identifier starts with 'beta' or 'b' \
            (case insensitive), followed by an empty string or a digit
        """

        if not isinstance(self._cmp[0], str):
            return False

        if self._cmp[0].lower().startswith("beta"):
            s = self._cmp[0][len("beta") :]
            return s == "" or s.isdigit()

        if self._cmp[0].lower().startswith("b"):
            s = self._cmp[0][len("b") :]
            return s == "" or s.isdigit()

        return False

    @property
    def is_rc(self) -> bool:
        """Returns if first dot-separated identifier starts with 'rc' \
            (case insensitive), followed by an empty string or a digit"""

        if not isinstance(self._cmp[0], str):
            return False

        if self._cmp[0].lower().startswith("rc"):
            s = self._cmp[0][len("rc") :]
            return s == "" or s.isdigit()

        return False

    def _get_cmp_list(self, string: str) -> t.List[t.Union[int, str]]:
        """Comparison list"""

        ret: t.List[t.Union[int, str]] = []
        tmp = string.split(".")  # identifiers are dot-separated
        for i in tmp:
            if i.isdigit():
                ret.append(int(i))
            else:
                ret.append(i)

        return ret

    def _check_then_set(self, string: str) -> str:
        """Raises error if invalid string"""

        if not re.match(RE_PRE, string):
            raise ParseException(EXC_INVALID_STR.format("pre-release", string))

        return string


class Build:
    """Represents a build string"""

    def __init__(self, string: str) -> None:
        """Constructor

        https://semver.org/spec/v2.0.0.html#spec-item-10

        The string passed in should be the string that follows the plus sign. \
        It must not include the plus sign itself.

        Args:
            string (str): The build string, excluding the plus sign

        Raises:
            ParseException: If the build string is invalid
        """

        self._string = self._check_then_set(string)

    def __repr__(self) -> str:
        """repr of Build"""

        return "Build(string='{}')".format(self._string)

    def __str__(self) -> str:
        """Returns string with plus sign at beginning"""

        return "+{}".format(self._string)

    @property
    def string(self) -> str:
        """Returns the build string

        Setter:

        Sets the build string if valid, otherwise raises ParseException
        """

        return self._string

    @string.setter
    def string(self, string: str) -> None:
        self._string = self._check_then_set(string)

    def _check_then_set(self, string: str) -> str:
        """Raises error if invalid string"""

        if not re.match(RE_BUILD, string):
            raise ParseException(EXC_INVALID_STR.format("build/metadata", string))

        return string
