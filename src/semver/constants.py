"""
Regex strings, enums, exception messages, etc
"""

import enum

# -------------------- REGEX STRINGS --------------------

RE_PRE = (
    r"^(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*$"
)

RE_BUILD = r"^[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*$"
RE_FULL = (
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*"
    r"|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-]"
    r"[0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)

# -------------------- EXCEPTION MSGS --------------------

EXC_BAD_TYPE = "Unsupported rhs type for {}: '{}'"
EXC_CANNOT_ADD = "Cannot add {} that already exists."
EXC_CANNOT_DEC = "Cannot decrement number to a negative value."
EXC_CANNOT_RM = "Cannot remove {} that does not exist."
EXC_INVALID_POS = "Unrecognized version position"
EXC_INVALID_STR = "Invalid {} string."
EXC_INVALID_STR_2 = "Cannot {} an invalid string."
EXC_MUST_POSITIVE = "Number must be positive."
EXC_MUST_TYPE = "Value must be a(n) {}."
EXC_MUST_CMP = "Must be compared with another {} object."
EXC_PRE_NO_VALUE = "No digit to increment/decrement. Make sure the last dot-separated \
                    identifier is a numeric value."
EXC_PRE_NO_VALUE_2 = "Object has no pre-release label."

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
