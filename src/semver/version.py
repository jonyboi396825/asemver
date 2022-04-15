"""
Version class
"""

from __future__ import annotations

import re
import typing as t

from .common import Core
from .components import Build, Pre, VersionNumber
from .constants import (
    EXC_BAD_TYPE,
    EXC_CANNOT_ADD,
    EXC_CANNOT_RM,
    EXC_INVALID_POS,
    EXC_INVALID_STR,
    EXC_INVALID_STR_2,
    EXC_MUST_CMP,
    EXC_PRE_NO_VALUE_2,
    RE_FULL,
    VPos,
    VRm,
)
from .exc import (
    InvalidOperationException,
    InvalidPositionException,
    NoValueException,
    ParseException,
)


class Version(Core):
    """Objects of this class represent version numbers that follow the \
        semantic versioning scheme.

    The versions follow Semantic Versioning 2.0: https://semver.org/spec/v2.0.0.html

    Given a version number MAJOR.MINOR.PATCH, increment the:

    1. MAJOR version when you make incompatible API changes,
    2. MINOR version when you add functionality in a backwards compatible manner, and
    3. PATCH version when you make backwards compatible bug fixes.

    Additional labels for pre-release and build metadata are available as extensions \
    to the MAJOR.MINOR.PATCH format.

    Note that pre-releases in semantic versions are not compatible with \
    pre-releases in Python projects (See https://peps.python.org/pep-0440/)
    """

    def __init__(
        self,
        major: t.Union[int, VersionNumber],
        minor: t.Union[int, VersionNumber],
        patch: t.Union[int, VersionNumber],
        pre: t.Optional[t.Union[str, Pre]] = None,
        build: t.Optional[t.Union[str, Build]] = None,
    ) -> None:
        """Constructor

        Args:
            major (Union[int, VersionNumber]): Major version number, must be positive
            minor (Union[int, VersionNumber]): Minor version number, must be positive
            patch (Union[int, VersionNumber]): Patch version number, must be positive
            pre (Optional[Union[str, Pre]], optional): Prefix string; should be the \
                                        string AFTER the hyphen. Defaults to None.
            build (Optional[Union[str, Build]], optional): Build string; must be the \
                                        string AFTER the plus sign. Defaults to None.
        """

        self._major: VersionNumber = self._conv_type(major, VersionNumber)
        self._minor: VersionNumber = self._conv_type(minor, VersionNumber)
        self._patch: VersionNumber = self._conv_type(patch, VersionNumber)

        # pre-release and build labels are set to None if they don't exist
        self._pre: t.Optional[Pre] = self._conv_type(pre, Pre)
        self._build: t.Optional[Build] = self._conv_type(build, Build)

        # for incrementing, decrementing (lookups)
        self._id_ref: t.Dict[VPos, t.Union[VersionNumber, Pre, None]] = {
            VPos.MAJOR: self._major,
            VPos.MINOR: self._minor,
            VPos.PATCH: self._patch,
            VPos.PRE: None,
        }
        self._id_order = [VPos.MAJOR, VPos.MINOR, VPos.PATCH]

    def __repr__(self) -> str:
        """repr of Version"""

        return "Version(major={}, minor={}, patch={}, pre={}, build={})".format(
            self._major, self._minor, self._patch, repr(self._pre), repr(self._build)
        )

    def __str__(self) -> str:
        """{MAJOR}.{MINOR}.{PATCH}-{PRE}+{BUILD}"""

        pre_str = "" if self._pre is None else str(self._pre)
        build_str = "" if self._build is None else str(self._build)

        return "{}.{}.{}{}{}".format(
            str(self._major), str(self._minor), str(self._patch), pre_str, build_str
        )

    def __lt__(self, other: t.Any) -> bool:
        """Compares less than

        https://semver.org/spec/v2.0.0.html#spec-item-11
        """

        if not isinstance(other, Version):
            raise TypeError(EXC_MUST_CMP.format("Version", type(other)))

        def cmp(lhs: t.Any, rhs: t.Any) -> bool:
            if lhs is None and rhs is not None:
                # if rhs does have a pre-release (and lhs does not), then lhs > rhs
                return False
            elif lhs is not None and rhs is None:
                # if rhs does not have a pre-release (and lhs does), then lhs < rhs
                return True
            elif isinstance(lhs, VersionNumber) and isinstance(rhs, Pre):
                # ints < strs
                return True
            else:
                return bool(lhs < rhs)

        l1 = [self._major, self._minor, self._patch, self._pre]
        l2 = [other._major, other._minor, other._patch, other._pre]

        return self._calc_lt(l1, l2, cmp)

    def __eq__(self, other: t.Any) -> bool:
        """Compares equality (excluding build versions)"""

        if not isinstance(other, Version):
            raise TypeError(EXC_MUST_CMP.format("Version", type(other)))

        l1 = [self._major, self._minor, self._patch, self._pre]
        l2 = [other._major, other._minor, other._patch, other._pre]

        return self._calc_eq(l1, l2)

    def __add__(self, other: t.Any) -> Version:
        """Multi-use operator to add things

        * If added to a VPos enum, increments version at that position \
        (including pre-release versions, if they exist).
        * If added to a string that represents a pre-release label \
        (i.e. starts with a hyphen '-'), then adds the pre-release \
        label only if there is no pre-release label already and the \
        label is valid. Otherwise, the program will raise an exception.
        * If added to a string that represents a build/metadata label \
        (i.e. starts with a plus sign '+'), then adds the build/metadata \
        label only if there is no build/metadata label already and the \
        label is valid. Otherwise, the program will raise an exception.
        * If added to anything else, raises an exception.
        """

        if isinstance(other, VPos):
            # increment
            self.inc(other)
        elif isinstance(other, str):
            if other[0] == "-":
                # set pre if it doesn't exist
                if self.has_pre:
                    raise InvalidOperationException(
                        EXC_CANNOT_ADD.format("pre-release", repr(self))
                    )
                self._pre = self._conv_type(other[1:], Pre)
            elif other[0] == "+":
                # set build if it doesn't exist
                if self.has_build:
                    raise InvalidOperationException(
                        EXC_CANNOT_ADD.format("build metadata", repr(self))
                    )
                self._build = self._conv_type(other[1:], Build)
            else:
                # unknown string
                raise InvalidOperationException(EXC_INVALID_STR_2.format("add", other))
        else:
            # unknown type
            raise TypeError(EXC_BAD_TYPE.format("+", type(other)))

        return self

    def __sub__(self, other: t.Any) -> Version:
        """Multi-use operator to subtract/remove things

        * If added to a VPos enum, decrements version at that position \
        (including pre-release versions, if they exist), only if their \
        version number is not 0.
        * If added to a VRm enum, removes the label indicated by the enum \
        only if the label exists. Otherwise, raises an exception.
        * If operator is used for anything else, raises an exception.
        """

        if isinstance(other, VPos):
            # decrement
            self.dec(other)
        elif isinstance(other, VRm):
            if other == VRm.PRE:
                # remove pre if it exists
                if not self.has_pre:
                    raise InvalidOperationException(
                        EXC_CANNOT_RM.format("pre-release", repr(self))
                    )
                self.remove_pre()
            else:
                # remove pre if it exists
                if not self.has_build:
                    raise InvalidOperationException(
                        EXC_CANNOT_RM.format("build metadata", repr(self))
                    )
                self.remove_build()
        else:
            # unknown type
            raise TypeError(EXC_BAD_TYPE.format("-", type(other)))

        return self

    def inc(self, pos: t.Optional[VPos] = None) -> None:
        """Increments/bumps given position by 1

        Increments are based on:

        * https://semver.org/spec/v2.0.0.html#spec-item-6,
        * https://semver.org/spec/v2.0.0.html#spec-item-7,
        * https://semver.org/spec/v2.0.0.html#spec-item-8

        Note that incrementing a major, minor, or patch version will \
        not affect the build or pre-release labels. (Example: incrementing \
        the major version of 2.3.5-alpha.1+a93eb2 will result in \
        3.0.0-alpha.1+a93nb2) This means that the pre-release and build labels \
        will have to be manually reset.

        Note that if pos is PRE and there is no pre-release label for a certain \
        object, then an exception will be thrown.

        Args:
            pos (Optional[VPos], optional): Which part of the version to increment \
            (values should come from the VPos enum). Defaults to None (which \
            will evaluate to VPos.PRE).
        """

        if pos is None:
            pos = VPos.PRE

        if not isinstance(pos, VPos) or pos not in self._id_ref:
            raise InvalidPositionException(EXC_INVALID_POS.format(pos))

        if pos == VPos.PRE:
            if self._pre is None:
                raise NoValueException(EXC_PRE_NO_VALUE_2.format(repr(self)))

            self._pre.inc()
            return

        # make mypy happy
        cur = self._id_ref[pos]
        assert cur is not None, "lookup pos is None"

        # increase current version and reset ones to the right of it
        # (except pre-release)
        cur.inc()
        ind = self._id_order.index(pos)
        for v in self._id_order[ind + 1 :]:
            to_reset = self._id_ref[v]
            assert to_reset is not None, "one of major, minor, micro is None"

            to_reset.reset()

    def dec(self, pos: t.Optional[VPos] = None) -> None:
        """Decrements a given position by 1

        Note that decrementing any parts of a version will not affect any \
        other parts of a version. (Example: decrementing the major version of \
        2.6.12-beta.5+meta will result in 1.6.12-beta.5+meta)

        An exception will be raised if the digit that is to be decremented is 0.

        Args:
            pos (Optional[VPos], optional): Which part of the version to decrement \
            (values should come from the VPos enum). Defaults to None (which will \
            evaluate to VPos.PRE)
        """

        if pos is None:
            pos = VPos.PRE

        if not isinstance(pos, VPos):
            raise InvalidPositionException(EXC_INVALID_POS.format(pos))

        if pos == VPos.PRE:
            # not decrementing from lookup dict because
            # self._pre can be None on initialization
            if self._pre is None:
                raise NoValueException(EXC_PRE_NO_VALUE_2.format(repr(self)))

            self._pre.dec()
            return

        # make mypy happy
        cur = self._id_ref[pos]
        assert cur is not None, "lookup pos is None"

        # decrease version position and ignore all other ones
        cur.dec()

    def remove_pre(self) -> None:
        """Removes the pre-release label

        For example, 1.4.5-alpha.4+meta will become 1.4.5+meta

        Does the same thing as setting the pre property to None.
        """

        self._pre = None

    def remove_build(self) -> None:
        """Removes the build label

        For example, 1.4.5-alpha.4+meta will become 1.4.5-alpha.4

        Does the same thing as setting the build property to None.
        """

        self._build = None

    def reset(self) -> None:
        """Resets version to 0.0.0"""

        self._major = VersionNumber(0)
        self._minor = VersionNumber(0)
        self._patch = VersionNumber(0)
        self._pre = None
        self._build = None

    @property
    def major(self) -> int:
        """Major version number

        Setter:

        Sets major version number if positive
        """

        return self._major.number

    @major.setter
    def major(self, num: t.Union[int, VersionNumber]) -> None:
        self._major = self._conv_type(num, VersionNumber)

    @property
    def minor(self) -> int:
        """Minor version number

        Setter:

        Sets minor version number if positive
        """

        return self._minor.number

    @minor.setter
    def minor(self, num: t.Union[int, VersionNumber]) -> None:
        self._minor = self._conv_type(num, VersionNumber)

    @property
    def patch(self) -> int:
        """Patch version number

        Setter:

        Sets patch version number if positive
        """

        return self._patch.number

    @patch.setter
    def patch(self, num: t.Union[int, VersionNumber]) -> None:
        self._patch = self._conv_type(num, VersionNumber)

    @property
    def pre(self) -> t.Optional[str]:
        """Pre-release string, without the first hyphen. \
        If there is no pre-release string, then returns None.

        Setter:

        Sets the pre-release string (should be the string after the hyphen; \
        should not include the hyphen)
        """

        if self._pre is None:
            return None

        return self._pre.string

    @pre.setter
    def pre(self, pre: t.Optional[t.Union[str, Pre]]) -> None:
        self._pre = self._conv_type(pre, Pre)

    @property
    def pre_digit(self) -> t.Optional[int]:
        """Returns the pre-release digit (if the pre-release string exists or the \
            rightmost dot-separated identifier in the pre-release string is a number, \
            otherwise returns None)
        """

        if self._pre is None:
            return None

        return self._pre.digit

    @property
    def has_pre(self) -> bool:
        """If a pre-release label exists for the current version object"""

        return self._pre is not None

    @property
    def build(self) -> t.Optional[str]:
        """Build/metadata string, without the first plus-sign \
        If there is no build/metadata string, then returns None.

        Setter:

        Sets the build/metadata string (must be the string after the plus-sign; \
        must not include the plus-sign)
        """

        if self._build is None:
            return None

        return self._build.string

    @build.setter
    def build(self, build: t.Optional[t.Union[str, Pre]]) -> None:
        self._build = self._conv_type(build, Build)

    @property
    def has_build(self) -> bool:
        """If a build label exists for the current version object"""

        return self._build is not None

    @property
    def is_alpha(self) -> bool:
        """If current version is an alpha release

        Checks if it is an alpha release by seeing if the first dot-separated \
        identifier starts with 'a' or 'alpha', followed by an empty string or \
        a digit.

        Example: 2.5.1-alpha0 and 2.5.1-alpha.4.1.4 are alpha releases.

        If there is no pre-release, returns False.
        """

        if self._pre is None:
            return False

        return self._pre.is_alpha

    @property
    def is_beta(self) -> bool:
        """If current version is a beta release

        Checks if it is a beta release by seeing if the first dot-separated \
        identifier starts with 'b' or 'beta', followed by an empty string or \
        a digit.

        Example: 1.4.5-beta0 and 1.4.5-beta.2.x.5 are beta releases.

        If there is no pre-release, returns False.
        """

        if self._pre is None:
            return False

        return self._pre.is_beta

    @property
    def is_rc(self) -> bool:
        """If current version is a release candidate

        Checks if it is a release candidate by seeing if the first dot-separated \
        identifier starts with 'rc', followed by an empty string or a digit.

        Example: 1.4.5-beta0 and 1.4.5-beta.2.x.5 are beta releases.

        If there is no pre-release, returns False.
        """

        if self._pre is None:
            return False

        return self._pre.is_rc

    @property
    def is_final(self) -> bool:
        """If current version is a final release

        Checks if there is any pre-release label or build label. A final release \
        is a release that has no pre-release or build labels.

        Example: 2.6.2 is a pre-release but 2.1.2+build3201b3 is not
        """

        return not self.has_build and not self.has_pre

    def _conv_type(self, val: t.Any, cls: t.Type) -> t.Any:
        """If val is of type cls, then returns. Otherwise converts to cls type"""

        if val is None:
            return None

        if isinstance(val, cls):
            return val

        return cls(val)


def parse_version(version: str) -> Version:
    """Parses a semantic version string into a Version class

    Args:
        version (str): Semantic verion string

    Returns:
        Version: Version class that represents the string
    """

    parsed = re.match(RE_FULL, version)

    # is not valid string
    if not parsed:
        raise ParseException(EXC_INVALID_STR.format("semantic version", version))

    # get versions from groups
    major, minor, patch, pre, build = parsed.groups()
    major, minor, patch = int(major), int(minor), int(patch)

    return Version(major, minor, patch, pre, build)
