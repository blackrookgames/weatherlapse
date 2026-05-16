__all__ = ['DTFormat']

from dataclasses import\
    dataclass as _dataclass

from .c_DTFormatDate import\
    DTFormatDate as _DTFormatDate

@_dataclass(frozen = True)
class DTFormat:
    """ Represents a date/time display format """

    use12hr:bool
    """ Whether or not to display time in 12-hour format """

    date:_DTFormatDate
    """ Date display format """