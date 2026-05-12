__all__ = ['Anchor']

from enum import\
    auto as _auto,\
    Enum as _Enum

class Anchor(_Enum):
    """ Represents an anchor setting """

    NW = _auto()
    """ Northwest """

    N = _auto()
    """ North """

    NE = _auto()
    """ Northeast """

    W = _auto()
    """ West """

    CENTER = _auto()
    """ Center """

    E = _auto()
    """ East """

    SW = _auto()
    """ Southwest """

    S = _auto()
    """ South """

    SE = _auto()
    """ Southeast """