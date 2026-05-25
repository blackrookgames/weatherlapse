__all__ = ['RenderMeta']

import calendar as _cal
import datetime as _dt
import io as _io
import struct as _struct

import code.engine.data as _data

from .c_ConfigLayer import ConfigLayer as _ConfigLayer

class RenderMeta(_data.DataLoadable, _data.DataSavable):
    """ Represents metadata about a render """

    #region init

    def __init__(self):
        """ Initializer for RenderMeta """
        self.__date:_dt.datetime = _dt.datetime(2000, 1, 1)
        self.__layer:_ConfigLayer = _ConfigLayer.CLOUDS
        self.__zoom:int = 0
        self.__min_x:int = 0
        self.__min_y:int = 0
        self.__max_x:int = 0
        self.__max_y:int = 0

    #endregion

    #region load/save

    def _load(self, reader:_io.BufferedReader):
        # date
        date_year = max(1, min(9999, _struct.unpack('<h', reader.read(2))[0]))
        date_month = max(1, min(12, reader.read(1)[0]))
        _, date_month_ndays = _cal.monthrange(date_year, date_month)
        date_day = max(1, min(date_month_ndays, reader.read(1)[0]))
        date_hour = max(0, min(23, reader.read(1)[0]))
        date_minute = max(0, min(59, reader.read(1)[0]))
        date_second = max(0, min(59, reader.read(1)[0]))
        date_microsecond = max(0, min(999999, _struct.unpack('<i', reader.read(4))[0]))
        self.__date = _dt.datetime(date_year, date_month, date_day, date_hour, date_minute, date_second, date_microsecond)
        # layer
        try: self.__layer = _ConfigLayer(reader.read(1)[0])
        except: self.__layer = _ConfigLayer.CLOUDS
        # zoom
        self.__zoom = _struct.unpack('<i', reader.read(4))[0]
        # min_x
        self.__min_x = _struct.unpack('<i', reader.read(4))[0]
        # min_y
        self.__min_y = _struct.unpack('<i', reader.read(4))[0]
        # max_x
        self.__max_x = _struct.unpack('<i', reader.read(4))[0]
        # max_y
        self.__max_y = _struct.unpack('<i', reader.read(4))[0]

    def _save(self, writer:_io.BufferedWriter):
        # date
        writer.write(_struct.pack('<h', self.__date.year))
        writer.write(bytes([\
            self.__date.month,\
            self.__date.day,\
            self.__date.day,\
            self.__date.hour,\
            self.__date.minute,\
            self.__date.second]))
        writer.write(_struct.pack('<i', self.__date.microsecond))
        # layer
        writer.write(bytes([self.__layer.value]))
        # zoom
        writer.write(_struct.pack('<i', self.__zoom))
        # min_x
        writer.write(_struct.pack('<i', self.__min_x))
        # min_y
        writer.write(_struct.pack('<i', self.__min_y))
        # max_x
        writer.write(_struct.pack('<i', self.__max_x))
        # max_y
        writer.write(_struct.pack('<i', self.__max_y))

    #endregion

    #region properties
    
    @property
    def date(self):
        """ Date/time of rendering """
        return self.__date
    @date.setter
    def date(self, value:_dt.datetime):
        self.__date = value

    @property
    def layer(self):
        """ Layer """
        return self.__layer
    @layer.setter
    def layer(self, value:_ConfigLayer):
        self.__layer = value

    @property
    def zoom(self):
        """ Region zoom value """
        return self.__zoom
    @zoom.setter
    def zoom(self, value:int):
        self.__zoom = value

    @property
    def min_x(self):
        """ Region minimum X-coordinate """
        return self.__min_x
    @min_x.setter
    def min_x(self, value:int):
        self.__min_x = value

    @property
    def min_y(self):
        """ Region minimum Y-coordinate """
        return self.__min_y
    @min_y.setter
    def min_y(self, value:int):
        self.__min_y = value

    @property
    def max_x(self):
        """ Region maximum X-coordinate """
        return self.__max_x
    @max_x.setter
    def max_x(self, value:int):
        self.__max_x = value

    @property
    def max_y(self):
        """ Region maximum Y-coordinate """
        return self.__max_y
    @max_y.setter
    def max_y(self, value:int):
        self.__max_y = value

    #endregion