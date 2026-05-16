__all__ = [ 'ConfigRegion' ]

import xml.etree.ElementTree as _ET

import engine.col as _col
import engine.num as _num
import engine.xml2 as _xml2

class ConfigRegion(_xml2.XmlLoadable, _xml2.XmlSavable):
    """ Represents a region configuration """

    #region init

    def __init__(self):
        """ Initializer for ConfigRegion """
        self.__zoom:int = self.__DEF_ZOOM
        self.__min_x:int = self.__DEF_MIN_X
        self.__min_y:int = self.__DEF_MIN_Y
        self.__max_x:int = self.__DEF_MAX_X
        self.__max_y:int = self.__DEF_MAX_Y

    #endregion

    #region load/save

    def _load_from_xml(self, element:_ET.Element):
        self.__zoom = int(_xml2.XmlUtil.parse_element_text(\
            _xml2.XmlUtil.get_element(element, "zoom"),\
            _num.Parse.try_U16))
        self.__min_x = int(_xml2.XmlUtil.parse_element_text(\
            _xml2.XmlUtil.get_element(element, "min_x"),\
            _num.Parse.try_U16))
        self.__min_y = int(_xml2.XmlUtil.parse_element_text(\
            _xml2.XmlUtil.get_element(element, "min_y"),\
            _num.Parse.try_U16))
        self.__max_x = int(_xml2.XmlUtil.parse_element_text(\
            _xml2.XmlUtil.get_element(element, "max_x"),\
            _num.Parse.try_U16))
        self.__max_y = int(_xml2.XmlUtil.parse_element_text(\
            _xml2.XmlUtil.get_element(element, "max_y"),\
            _num.Parse.try_U16))
        
    def _save_to_xml(self, element:_ET.Element):
        element.tag = "region"
        x_zoom = _xml2.XmlUtil.create_element(tag = "zoom", text = str(self.__zoom))
        element.append(x_zoom)
        x_min_x = _xml2.XmlUtil.create_element(tag = "min_x", text = str(self.__min_x))
        element.append(x_min_x)
        x_min_y = _xml2.XmlUtil.create_element(tag = "min_y", text = str(self.__min_y))
        element.append(x_min_y)
        x_max_x = _xml2.XmlUtil.create_element(tag = "max_x", text = str(self.__max_x))
        element.append(x_max_x)
        x_max_y = _xml2.XmlUtil.create_element(tag = "max_y", text = str(self.__max_y))
        element.append(x_max_y)

    #endregion

    #region const
    
    __DEF_ZOOM = 0
    __DEF_MIN_X = 0
    __DEF_MIN_Y = 0
    __DEF_MAX_X = 1
    __DEF_MAX_Y = 1

    MAXZOOM = int(9)
    """ Maximum zoom level """

    MAXCOORD = _col.ROList([ 2 ** _i for _i in range(MAXZOOM + 1) ])
    """ Maximum coordinate value by zoom level """

    #endregion

    #region properties
    
    @property
    def zoom(self):
        """ Zoom level """
        return self.__zoom
    @zoom.setter
    def zoom(self, value:int):
        self.__zoom = value

    @property
    def min_x(self):
        """ Minimum X-coordinate """
        return self.__min_x
    @min_x.setter
    def min_x(self, value:int):
        self.__min_x = value

    @property
    def min_y(self):
        """ Minimum Y-coordinate """
        return self.__min_y
    @min_y.setter
    def min_y(self, value:int):
        self.__min_y = value

    @property
    def max_x(self):
        """ Maximum X-coordinate """
        return self.__max_x
    @max_x.setter
    def max_x(self, value:int):
        self.__max_x = value

    @property
    def max_y(self):
        """ Maximum Y-coordinate """
        return self.__max_y
    @max_y.setter
    def max_y(self, value:int):
        self.__max_y = value

    #endregion

    #region methods

    def reset(self):
        """ Resets the configuration """
        self.__zoom = self.__DEF_ZOOM
        self.__min_x = self.__DEF_MIN_X
        self.__min_y = self.__DEF_MIN_Y
        self.__max_x = self.__DEF_MAX_X
        self.__max_y = self.__DEF_MAX_Y

    #endregion