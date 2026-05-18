__all__ = [ 'DateUtil' ]

import calendar as _cal
import datetime as _dt

from .c_Weekday import Weekday as _Weekday

class DateUtil:
    """ Utility for date-related operations """

    YEAR_MIN = 1
    """ Minimum year value """

    YEAR_MAX = 9999
    """ Maximum year value """

    DATE_MIN = _dt.date(YEAR_MIN, 1, 1)
    """ Minimum date value """

    DATE_MAX = _dt.date(YEAR_MAX, 12, 31)
    """ Maximum date value """

    @classmethod
    def month_range(cls, date:_dt.date):
        """
        Returns the weekday of the first day of the month\n
        and number of the days in the month of the specified date
        """
        start, numdays = _cal.monthrange(date.year, date.month)
        return _Weekday((start + 1) % 7), numdays
    
    @classmethod
    def month_start(cls, date:_dt.date):
        """
        Returns the weekday of the first day of the month of the specified date
        """
        start, _ = cls.month_range(date)
        return start

    @classmethod
    def month_numdays(cls, date:_dt.date):
        """
        Returns the number of the days in the month of the specified date
        """
        _, numdays = _cal.monthrange(date.year, date.month)
        return numdays

    @classmethod
    def change_year(cls, date:_dt.date, year:int):
        """
        Changes the year of the date, adjusting the day if necessary

        :param date: Source date
        :param year: New year value (1 - 9999)
        :return: Modified date
        :raises ValueError: year is out of range
        """
        if year < cls.YEAR_MIN or year > cls.YEAR_MAX: raise ValueError("year is out of range.")
        new = _dt.date(year, date.month, 1)
        return _dt.date(new.year, new.month, min(cls.month_numdays(new), date.day))
    
    @classmethod
    def change_month(cls, date:_dt.date, month:int):
        """
        Changes the month of the date, adjusting the day if necessary

        :param date: Source date
        :param month: New month value (1 - 12)
        :return: Modified date
        :raises ValueError: month is out of range
        """
        if month < 1 or month > 12: raise ValueError("month is out of range.")
        new = _dt.date(date.year, month, 1)
        return _dt.date(new.year, new.month, min(cls.month_numdays(new), date.day))
