"""
Exception classes
"""


class NegativeValueException(Exception):
    """When version digit is set/decremented to negative value"""


class NoValueException(Exception):
    """When trying to increment/decrement a digit that is None"""


class ParseException(Exception):
    """Bad parse"""


class InvalidPositionException(Exception):
    """Unrecognized position to increment/decrement"""


class InvalidOperationException(Exception):
    """When the + or - operator is used wrong"""
