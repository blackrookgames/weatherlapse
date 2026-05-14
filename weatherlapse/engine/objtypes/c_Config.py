__all__ = [ 'Config' ]

import re as _re
import xml.etree.ElementTree as _ET

from datetime import\
    datetime as _datetime,\
    timedelta as _timedelta
from pathlib import\
    Path as _Path

from engine.num import\
    Parse as _Parse,\
    ParseError as _ParseError,\
    ParseResult as _ParseResult
from engine.xml2 import\
    XmlLoadable as _XmlLoadable,\
    XmlSavable as _XmlSavable

from .c_ConfigLayer import ConfigLayer as _ConfigLayer
from .c_ConfigRegion import ConfigRegion as _ConfigRegion

class Config(_XmlLoadable, _XmlSavable):
    """ Represents a configuration """

    #region init
    
    def __init__(self):
        self.__apikey:str = ""
        self.__region:_ConfigRegion = self.__DEF_REGION
        self.__layer:_ConfigLayer = self.__DEF_LAYER
        self.__start:None|_datetime = None
        self.__stop:None|_datetime = None
        self.__interval:_timedelta = self.__DEF_INTERVAL
        self.__output:_Path = self.__DEF_OUTPUT

    #endregion

    #region load/save

    def _load_from_xml(self, element:_ET.Element):
        # apikey
        x_apikey = self._find_element(element, "apikey")
        if x_apikey is not None:
            self.__apikey = "" if (x_apikey.text is None) else x_apikey.text
        else:
            self.__apikey = ""
        # #region (leave the hash or else vscode will think it's the start of a region of code)
        x_region = self._find_element(element, "region")
        if x_region is not None:
            region_zoom = int(self._parse_text(\
                self._get_element(x_region, "zoom"),\
                _Parse.try_U16))
            region_min_x = int(self._parse_text(\
                self._get_element(x_region, "min_x"),\
                _Parse.try_U16))
            region_min_y = int(self._parse_text(\
                self._get_element(x_region, "min_y"),\
                _Parse.try_U16))
            region_max_x = int(self._parse_text(\
                self._get_element(x_region, "max_x"),\
                _Parse.try_U16))
            region_max_y = int(self._parse_text(\
                self._get_element(x_region, "max_y"),\
                _Parse.try_U16))
            self.__region = _ConfigRegion(region_zoom, region_min_x, region_min_y, region_max_x, region_max_y)
        else:
            self.__region = self.__DEF_REGION
        # layer
        x_layer = self._find_element(element, "layer")
        if x_layer is not None:
            self.__layer = self._parse_text(x_layer, lambda s: _Parse.try_enum(_ConfigLayer, s))
        else:
            self.__layer = self.__DEF_LAYER
        # start
        x_start = self._find_element(element, "start")
        if x_start is not None:
            self.__start = self._parse_text(x_start, self.__dt_from_str)
        else:
            self.__start = None
        # stop
        x_stop = self._find_element(element, "stop")
        if x_stop is not None:
            self.__stop = self._parse_text(x_stop, self.__dt_from_str)
        else:
            self.__stop = None
        # interval
        x_interval = self._find_element(element, "interval")
        if x_interval is not None:
            self.__interval = self._parse_text(x_interval, self.__td_from_str)
        else:
            self.__interval = self.__DEF_INTERVAL
        # output
        x_output = self._find_element(element, "output")
        if x_output is not None:
            self.__output = self.__DEF_OUTPUT if (x_output.text is None) else _Path(x_output.text)
        else:
            self.__output = self.__DEF_OUTPUT
        
    def _save_to_xml(self, element:_ET.Element):
        element.tag = "weatherlapse"
        # apikey
        x_apikey = self._create_element(tag = "apikey", text = self.__apikey)
        element.append(x_apikey)
        # #region (leave the hash or else vscode will think it's the start of a region of code)
        x_region = self._create_element(tag = "region")
        element.append(x_region)
        x_region_zoom = self._create_element(tag = "zoom", text = str(self.__region.zoom))
        x_region.append(x_region_zoom)
        x_region_min_x = self._create_element(tag = "min_x", text = str(self.__region.min_x))
        x_region.append(x_region_min_x)
        x_region_min_y = self._create_element(tag = "min_y", text = str(self.__region.min_y))
        x_region.append(x_region_min_y)
        x_region_max_x = self._create_element(tag = "max_x", text = str(self.__region.max_x))
        x_region.append(x_region_max_x)
        x_region_max_y = self._create_element(tag = "max_y", text = str(self.__region.max_y))
        x_region.append(x_region_max_y)
        # layer
        x_layer = self._create_element(tag = "layer", text = self.__layer.name)
        element.append(x_layer)
        # start
        if self.__start is not None:
            x_start = self._create_element(tag = "start", text = self.__dt_to_str(self.__start))
            element.append(x_start)
        # stop
        if self.__stop is not None:
            x_stop = self._create_element(tag = "stop", text = self.__dt_to_str(self.__stop))
            element.append(x_stop)
        # interval
        x_interval = self._create_element(tag = "interval", text = self.__td_to_str(self.__interval))
        element.append(x_interval)
        # output
        x_output = self._create_element(tag = "output", text = str(self.__output))
        element.append(x_output)

    #endregion

    #region const

    __DEF_REGION = _ConfigRegion(0, 0, 0, 0, 0)
    __DEF_LAYER = _ConfigLayer.CLOUDS
    __DEF_INTERVAL = _timedelta(minutes = 30)
    __DEF_OUTPUT = _Path('.')

    #endregion

    #region properties

    @property
    def apikey(self):
        """ API Key """
        return self.__apikey
    @apikey.setter
    def apikey(self, value:str):
        self.__apikey = value

    @property
    def region(self):
        """ Observation region """
        return self.__region
    @region.setter
    def region(self, value:_ConfigRegion):
        self.__region = value

    @property
    def layer(self):
        """ Observation visual layer """
        return self.__layer
    @layer.setter
    def layer(self, value:_ConfigLayer):
        self.__layer = value

    @property
    def start(self):
        """ Date/time to start collecting data """
        return self.__start
    @start.setter
    def start(self, value:_datetime):
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

    @property
    def output(self):
        """ Output directory """
        return self.__output
    @output.setter
    def output(self, value:_Path):
        self.__output = value

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