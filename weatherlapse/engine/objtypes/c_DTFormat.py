__all__ = ['DTFormat']

import datetime as _dt

from dataclasses import\
    dataclass as _dataclass

from .c_DTFormatDate import\
    DTFormatDate as _DTFormatDate

@_dataclass(frozen = True)
class DTFormat:
    """ Represents a date/time display format """

    #region fields

    use12hr:bool
    """ Whether or not to display time in 12-hour format """

    date:_DTFormatDate
    """ Date display format """

    #endregion

    #region methods

    def make_str(self, datetime:_dt.datetime):
        """
        Creates a string representation of a date/time

        :param datetime: Date/Time
        :return: Created string
        """
        match self.date:
            case _DTFormatDate.YEAR_MONTH_DAY: format_date = "%Y/%m/%d"
            case _DTFormatDate.DAY_MONTH_YEAR: format_date = "%d/%m/%Y"
            case _DTFormatDate.MONTH_DAY_YEAR: format_date = "%m/%d/%Y"
            case _: format_date = ""
        format_time = "%I:%M:%S %p" if self.use12hr else "%H:%M:%S"
        return datetime.strftime(f"{format_date} {format_time}")

    #endregion