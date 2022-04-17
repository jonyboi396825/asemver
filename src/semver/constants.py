"""
Regex strings, enums, exception messages, etc
"""

import enum

# -------------------- REGEX STRINGS --------------------

RE_PRE = (
    r"^(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*$"
)  # for parsing pre-releases
RE_BUILD = r"^[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*$"  # for parsing build metadata labels
RE_FULL = (
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*"
    r"|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-]"
    r"[0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)  # for parsing a full version string

# -------------------- EXCEPTION MSGS --------------------

EXC_BAD_TYPE = "Unsupported rhs type for {}: '{}'"
"""
When a Version object is added or subtracted (+, - operators) by \
an unknown type.

* In the + operator of Version, used when rhs is not a str or a VPos enum
* In the - operator of Version, used when rhs is not a VPos or VRm enum
"""


EXC_CANNOT_ADD = "Cannot add {} that already exists: {}"
"""
When trying to append a pre-release or build label to a version object \
that already has a pre-release or build label.

* In the + operator of Version, used when rhs is a str starting with a '+' and \
the has_build property is True, or when rhs is a str starting with a '-' and \
the has_pre property is True
"""


EXC_CANNOT_DEC = "Cannot decrement number to a negative value"
"""
When trying to decrement a VersionNumber object or the digit of a Pre object \
that is currently 0.

* In dec() of Pre, used when _digit attribute is 0
"""


EXC_CANNOT_RM = "Cannot remove {} that does not exist: {}"
"""
When trying to remove a pre-release or build label of a version object \
when the object currently does not have a pre-release or build label.

* In the - operator of Version, used when rhs is VRm.PRE and the has_pre \
property is False, or when rhs is VRm.BUILD and the has_build property is True
"""


EXC_INVALID_POS = "Unrecognized version position: {}"
"""
Used when incrementing or decrementing an invalid position of a Version object.

* In inc() of Version, used when the pos argument is not a VPos enum or not \
part of {VPos.MAJOR, VPos.MINOR, VPos.PATCH, VPos.PRE}
* In dec() of Version, used when the pos argument is not a VPos enum or not \
part of {VPos.MAJOR, VPos.MINOR, VPos.PATCH, VPos.PRE}
* In bump(), used when given position is not in {VPos.MAJOR, VPos.MINOR, \
VPos.PATCH, VPos.PRE}
"""


EXC_INVALID_STR = "Invalid {} string: {}"
"""
Used when there is an error when parsing the string.

* In the constructor of Pre and the string setter, used when the given pre-release \
string doesn't match the pre-release regex
* In the constructor of Build and the string setter, used when the build string \
doesn't match the build regex
* In parse_version(), used when the version string doesn't match the semantic \
versioning regex
"""


EXC_INVALID_STR_2 = "Cannot {} an invalid string: {}"
"""
Used when a Version object is added to an invalid string.

* In the + operator of Version, used when rhs is a string and the first character \
is not '+' or '-'
"""


EXC_MUST_POSITIVE = "Number must be positive: {}"
"""
Used when the user is trying to set a VersionNumber object to a negative number.

* In the VersionNumber constructor, used when the number argument is negative
* In the number setter of VersionNumber, used when the number argument is negative
"""


EXC_MUST_TYPE = "Value must be a(n) {}, not {}"
"""
Used in VersionNumber when trying to set a VersionNumber to anything outside of an int.

* In the VersionNumber constructor, used when the number argument not an int
* In the number setter of VersionNumber, used when the number argument is not an int
"""


EXC_MUST_CMP = "Must be compared with another {} object, not {}"
"""
Used in <, <=, >, >=, ==, != operators when comparing with another type.

* In the <, == operators of VersionNumber, used when type(other) != VersionNumber
* In the <, == operators of Pre, used when type(other) != Pre
* In the <, == operators of Version, used when type(other) != Version
"""


EXC_PRE_NO_VALUE = (
    "No digit to increment/decrement. Make sure the last dot-separated"
    " identifier is a numeric value: {}"
)
"""
Used in Pre when no digit exists to increment or decrement

* In inc() of Pre, used when _digit attribute is None
* In dec() of Pre, used when _digit attribute is None
"""


EXC_PRE_NO_VALUE_2 = "Object has no pre-release label: {}"
"""
Used in Version when trying to decrement a pre-release that doesn't exist.

* In inc() of Version, used when pos is VPos.PRE and _pre attribute is None
* In dec() of Version, used when pos is VPos.PRE and _pre attribute is None
* In bump(), used when pos is VPos.PRE and the given version has no pre-release label
"""


# -------------------- ENUMS --------------------


class VPos(enum.Enum):
    """Specifies which part of the version to increment/decrement

    * MAJOR increments/decrements major version
    * MINOR increments/decrements minor version
    * PATCH increments/decrements patch version
    * PRE increments/decrements the number of the rightmost dot-separated identifier \
        of the pre-release label only if a pre-release exists and the rightmost \
        dot-separated identifier is a number
    """

    MAJOR = enum.auto()
    MINOR = enum.auto()
    PATCH = enum.auto()
    PRE = enum.auto()


class VRm(enum.Enum):
    """Removable parts of a version object

    The only parts that are able to be removed are the pre-release labels \
    and build labels.

    For example, if the pre-release label of 2.4.2-alpha.6+52ab91 is removed, then \
    it will become 2.4.2+52ab91. If the build label of 2.4.2+52ab91 is removed, then \
    it will become 2.4.2.
    """

    PRE = enum.auto()
    BUILD = enum.auto()
