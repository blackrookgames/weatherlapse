__all__ = ['ConfigLayer']

from enum import \
    auto as _auto,\
    Enum as _Enum

class ConfigLayer(_Enum):
    """ Represents a visual layer configuration """

    CLOUDS = _auto()
    """ Clouds """

    PRECIPITATION = _auto()
    """ Precipitation """

    PRESSURE = _auto()
    """ Sea level pressure """

    WIND = _auto()
    """ Wind speed """

    TEMP = _auto()
    """ Temperature """