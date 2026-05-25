__all__ = [ 'Weekday' ]

from enum import\
    Enum as _Enum

class Weekday(_Enum):
    """ Represents a day of the week """

    SUNDAY = 0
    """ Sunday """

    MONDAY = 1
    """ Monday """

    TUESDAY = 2
    """ Tuesday """

    WEDNESDAY = 3
    """ Wednesday """

    THURSDAY = 4
    """ Thrusday """

    FRIDAY = 5
    """ Friday """

    SATURDAY = 6
    """ Saturday """