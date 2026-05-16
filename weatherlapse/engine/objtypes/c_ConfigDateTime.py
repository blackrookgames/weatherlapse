__all__ = [ 'ConfigDateTime' ]

import re as _re
import xml.etree.ElementTree as _ET

from datetime import\
    datetime as _datetime,\
    timedelta as _timedelta

import engine.xml2 as _xml2

from engine.num import\
    Parse as _Parse,\
    ParseError as _ParseError,\
    ParseResult as _ParseResult

from .c_DTFormat import DTFormat as _DTFormat
from .c_DTFormatDate import DTFormatDate as _DTFormatDate

class ConfigDateTime(_xml2.XmlLoadable, _xml2.XmlSavable):
    """ Represents a date/time configuration """

    #region init
    
    def __init__(self):
        self.__format:_DTFormat = self.__DEF_FORMAT
        self.__start:None|_datetime = None
        self.__stop:None|_datetime = None
        self.__interval:_timedelta = self.__DEF_INTERVAL

    #endregion

    #region load/save

    def _load_from_xml(self, element:_ET.Element):
        # format
        x_format = _xml2.XmlUtil.find_element(element, "format")
        if x_format is not None:
            # format_use12hr
            x_format_use12hr = _xml2.XmlUtil.find_element(x_format, "use12hr")
            if x_format_use12hr is not None:
                format_use12hr = _xml2.XmlUtil.parse_element_text(x_format_use12hr, _Parse.try_bool)
            else:
                format_use12hr = self.__DEF_FORMAT.use12hr
            # format_date
            x_format_date = _xml2.XmlUtil.find_element(x_format, "date")
            if x_format_date is not None:
                format_date = _xml2.XmlUtil.parse_element_text(x_format_date, lambda s: _Parse.try_enum(_DTFormatDate, s))
            else:
                format_date = self.__DEF_FORMAT.date
            # format
            self.__format = _DTFormat(format_use12hr, format_date)
        else:
            self.__format = self.__DEF_FORMAT
        # start
        x_start = _xml2.XmlUtil.find_element(element, "start")
        if x_start is not None:
            self.__start = _xml2.XmlUtil.parse_element_text(x_start, self.__dt_from_str)
        else:
            self.__start = None
        # stop
        x_stop = _xml2.XmlUtil.find_element(element, "stop")
        if x_stop is not None:
            self.__stop = _xml2.XmlUtil.parse_element_text(x_stop, self.__dt_from_str)
        else:
            self.__stop = None
        # interval
        x_interval = _xml2.XmlUtil.find_element(element, "interval")
        if x_interval is not None:
            self.__interval = _xml2.XmlUtil.parse_element_text(x_interval, self.__td_from_str)
        else:
            self.__interval = self.__DEF_INTERVAL
        
    def _save_to_xml(self, element:_ET.Element):
        element.tag = "datetime"
        # format
        x_format = _xml2.XmlUtil.create_element(tag = "format")
        element.append(x_format)
        # format_use12hr
        x_format_use12hr = _xml2.XmlUtil.create_element(tag = "use12hr", text = str(self.__format.use12hr))
        x_format.append(x_format_use12hr)
        # format_date
        x_format_date = _xml2.XmlUtil.create_element(tag = "date", text = self.__format.date.name)
        x_format.append(x_format_date)
        # start
        if self.__start is not None:
            x_start = _xml2.XmlUtil.create_element(tag = "start", text = self.__dt_to_str(self.__start))
            element.append(x_start)
        # stop
        if self.__stop is not None:
            x_stop = _xml2.XmlUtil.create_element(tag = "stop", text = self.__dt_to_str(self.__stop))
            element.append(x_stop)
        # interval
        x_interval = _xml2.XmlUtil.create_element(tag = "interval", text = self.__td_to_str(self.__interval))
        element.append(x_interval)

    #endregion

    #region const

    __DEF_FORMAT = _DTFormat(True, _DTFormatDate.MONTH_DAY_YEAR)
    __DEF_INTERVAL = _timedelta(minutes = 30)

    #endregion

    #region properties

    @property
    def format(self):
        """ Display format """
        return self.__format
    @format.setter
    def format(self, value:_DTFormat):
        self.__format = value

    @property
    def start(self):
        """ Date/time to start collecting data """
        return self.__start
    @start.setter
    def start(self, value:None|_datetime):
        self.__start = value

    @property
    def stop(self):
        """ Date/time to stop collecting data (None means continue indefinitely) """
        return self.__stop
    @stop.setter
    def stop(self, value:None|_datetime):
        self.__stop = value

    @property
    def interval(self):
        """ Interval between data collections """
        return self.__interval
    @interval.setter
    def interval(self, value:_timedelta):
        self.__interval = value

    #endregion

    #region helper methods

    @classmethod
    def __dt_to_str(cls, dt:_datetime):
        return f"{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute}:{dt.second}:{dt.microsecond}"
    
    @classmethod
    def __dt_from_str(cls, s:str):
        def _invalid(): 
            nonlocal s
            return _ParseResult[_datetime](_datetime.now(), _ParseError(f"\"{s}\" is not a valid date/time."))
        # Parse each value
        input = _re.split(r'[ /:]', s)
        values:list[int] = []
        for _item in input:
            _result = _Parse.try_U32(_item)
            if not _result.success: return _ParseResult[_datetime](_datetime.now(), _result.error)
            values.append(int(_result.value))
        # Make sure there are exactly 7 values
        if len(values) != 7: return _invalid()
        # Parse as datetime
        try: return _ParseResult[_datetime](
            _datetime(values[0], values[1], values[2], values[3],  values[4], values[5], values[6]), None)
        except: return _invalid()

    @classmethod
    def __td_to_str(cls, td:_timedelta):
        return f"{td.days} {td.seconds} {td.microseconds}"
    
    @classmethod
    def __td_from_str(cls, s:str):
        def _invalid(): 
            nonlocal s
            return _ParseResult[_timedelta](_timedelta(), _ParseError(f"\"{s}\" is not a valid time delta."))
        # Parse each value
        input = _re.split(r'[ ]', s)
        values:list[int] = []
        for _item in input:
            _result = _Parse.try_U32(_item)
            if not _result.success: return _ParseResult[_timedelta](_timedelta(), _result.error)
            values.append(int(_result.value))
        # Make sure there are exactly 3 values
        if len(values) != 3: return _invalid()
        # Parse as timedelta
        try: return _ParseResult[_timedelta](
            _timedelta(values[0], values[1], values[2]), None)
        except: return _invalid()

    #endregion

    #region methods

    def reset(self):
        """
        Resets the configuration
        """
        self.__format = self.__DEF_FORMAT
        self.__start = None
        self.__stop = None
        self.__interval = self.__DEF_INTERVAL

    #endregion