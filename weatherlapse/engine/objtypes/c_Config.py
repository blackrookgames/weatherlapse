__all__ = [ 'Config' ]

import re as _re
import xml.etree.ElementTree as _ET

from datetime import\
    datetime as _datetime,\
    timedelta as _timedelta
from pathlib import\
    Path as _Path

import engine.xml2 as _xml2

from engine.num import\
    Parse as _Parse

from .c_ConfigDateTime import ConfigDateTime as _ConfigDateTime
from .c_ConfigLayer import ConfigLayer as _ConfigLayer
from .c_ConfigRegion import ConfigRegion as _ConfigRegion

class Config(_xml2.XmlLoadable, _xml2.XmlSavable):
    """ Represents a configuration """

    #region init
    
    def __init__(self):
        self.__apikey:str = ""
        self.__region:_ConfigRegion = _ConfigRegion()
        self.__layer:_ConfigLayer = self.__DEF_LAYER
        self.__datetime:_ConfigDateTime = _ConfigDateTime()
        self.__output:_Path = self.__DEF_OUTPUT

    #endregion

    #region load/save

    def _load_from_xml(self, element:_ET.Element):
        # apikey
        x_apikey = _xml2.XmlUtil.find_element(element, "apikey")
        if x_apikey is not None:
            self.__apikey = "" if (x_apikey.text is None) else x_apikey.text
        else:
            self.__apikey = ""
        # #region (leave the hash or else vscode will think it's the start of a region of code)
        x_region = _xml2.XmlUtil.find_element(element, "region")
        if x_region is not None:
            self.__region.load_from_xml(x_region)
        else:
            self.__region.reset()
        # layer
        x_layer = _xml2.XmlUtil.find_element(element, "layer")
        if x_layer is not None:
            self.__layer = _xml2.XmlUtil.parse_element_text(x_layer, lambda s: _Parse.try_enum(_ConfigLayer, s))
        else:
            self.__layer = self.__DEF_LAYER
        # datetime
        x_datetime = _xml2.XmlUtil.find_element(element, "datetime")
        if x_datetime is not None:
            self.__datetime.load_from_xml(x_datetime)
        else:
            self.__datetime.reset()
        # output
        x_output = _xml2.XmlUtil.find_element(element, "output")
        if x_output is not None:
            self.__output = self.__DEF_OUTPUT if (x_output.text is None) else _Path(x_output.text)
        else:
            self.__output = self.__DEF_OUTPUT
        
    def _save_to_xml(self, element:_ET.Element):
        element.tag = "weatherlapse"
        # apikey
        x_apikey = _xml2.XmlUtil.create_element(tag = "apikey", text = self.__apikey)
        element.append(x_apikey)
        # #region (leave the hash or else vscode will think it's the start of a region of code)
        x_region = _xml2.XmlUtil.create_element(tag = "region")
        self.__region.save_to_xml(x_region)
        element.append(x_region)
        # layer
        x_layer = _xml2.XmlUtil.create_element(tag = "layer", text = self.__layer.name)
        element.append(x_layer)
        # datetime
        x_datetime = _xml2.XmlUtil.create_element(tag = "datetime")
        self.__datetime.save_to_xml(x_datetime)
        element.append(x_datetime)
        # output
        x_output = _xml2.XmlUtil.create_element(tag = "output", text = str(self.__output))
        element.append(x_output)

    #endregion

    #region const

    __DEF_LAYER = _ConfigLayer.CLOUDS
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

    @property
    def layer(self):
        """ Observation visual layer """
        return self.__layer
    @layer.setter
    def layer(self, value:_ConfigLayer):
        self.__layer = value

    @property
    def datetime(self):
        """ Date/time configuration """
        return self.__datetime

    @property
    def output(self):
        """ Output directory """
        return self.__output
    @output.setter
    def output(self, value:_Path):
        self.__output = value

    #endregion

    #region methods

    def reset(self):
        """
        Resets the configuration
        """
        self.__apikey = ""
        self.__region.reset()
        self.__layer = self.__DEF_LAYER
        self.__datetime.reset()
        self.__output = self.__DEF_OUTPUT

    #endregion