__all__ = [ 'ConfigRegion' ]

import xml.etree.ElementTree as _ET

from engine.col import ROList as _ROList
from dataclasses import dataclass as _dataclass

@_dataclass(frozen = True)
class ConfigRegion:
    """ Represents a region configuration """

    #region const

    MAXZOOM = int(9)
    """ Maximum zoom level """

    MAXCOORD = _ROList([ 2 ** _i for _i in range(MAXZOOM + 1) ])
    """ Maximum coordinate value by zoom level """

    #endregion

    #region fields
    
    zoom: int
    """ Zoom level """

    min_x: int
    """ Minimum X-coordinate """

    min_y: int
    """ Minimum Y-coordinate """

    max_x: int
    """ Maximum X-coordinate """

    max_y: int
    """ Maximum Y-coordinate """

    #endregion