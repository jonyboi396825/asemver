"""
Base classes with common functionality
"""

import abc
import typing as t


class Base(abc.ABC):  # pragma: no cover
    """
    Abstract base class with common methods that need to be implemented.
    """

    @abc.abstractmethod
    def __repr__(self) -> str:
        ...

    @abc.abstractmethod
    def __str__(self) -> str:
        ...

    @abc.abstractmethod
    def __lt__(self, other: t.Any) -> bool:
        ...

    @abc.abstractmethod
    def __eq__(self, other: t.Any) -> bool:
        ...

    @abc.abstractmethod
    def inc(self) -> None:
        ...

    @abc.abstractmethod
    def dec(self) -> None:
        ...

    @abc.abstractmethod
    def reset(self) -> None:
        ...


class Core(Base):
    """
    A class with commonly implemented methods across version classes.
    """

    def __ne__(self, other: t.Any) -> bool:
        return not self == other

    def __le__(self, other: t.Any) -> bool:
        return bool(self == other or self < other)

    def __gt__(self, other: t.Any) -> bool:
        return self != other and not self < other

    def __ge__(self, other: t.Any) -> bool:
        return bool(self == other or self > other)

    def _calc_lt(
        self,
        l1: t.List[t.Any],
        l2: t.List[t.Any],
        lt_func: t.Callable[[t.Any, t.Any], bool] = lambda lhs, rhs: bool(lhs < rhs),
    ) -> bool:
        """Compares less than

        Args:
            l1 (List[Any]): List of self objects to compare
            l2 (List[Any]): List of other objects to compare
            lt_func (Callable): Callable that takes in two arguments \
            and returns a boolean that is True if the first argument \
            is considered to be less than the second argument.
        Returns:
            bool: If less than or not
        """

        for _self, _other in zip(l1, l2):
            if _self is _other or _self == _other:
                continue
            elif lt_func(_self, _other):
                return True
            else:
                return False

        # https://semver.org/spec/v2.0.0.html#spec-item-11 number 4
        return len(l1) < len(l2)

    def _calc_eq(self, l1: t.List[t.Any], l2: t.List[t.Any]) -> bool:
        """Compares equality

        Args:
            l1 (List[Any]): List of self objects to compare
            l2 (List[Any]): List of other objects to compare
        Returns:
            bool: If equal or not
        """

        if len(l1) != len(l2):
            # if different lengths, cannot be equal
            return False

        for _self, _other in zip(l1, l2):
            if _self != _other:
                # if any inequality, not equal
                return False

        # means all equal
        return True
