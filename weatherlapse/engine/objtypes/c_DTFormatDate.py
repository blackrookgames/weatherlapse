__all__ = ['DTFormatDate']

from enum import\
    auto as _auto,\
    Enum as _Enum

class DTFormatDate(_Enum):
    """ Represents a display format for dates """

    YEAR_MONTH_DAY = _auto()
    """ Year/Month/Day (ex: 2026/05/15) """

    DAY_MONTH_YEAR = _auto()
    """ Day/Month/Year (ex: 15/05/2026) """

    MONTH_DAY_YEAR = _auto()
    """ Month/Day/Year (ex: 05/15/2026) """
    