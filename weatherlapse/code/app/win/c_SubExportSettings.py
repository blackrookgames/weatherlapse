__all__ = ['SubExportSettings']

from io import\
    BytesIO as _BytesIO

from pathlib import Path as _Path

import code.engine.data as _data

class SubExportSettings(_data.Picklable['SubExportSettings']):
    """ Represents a export settings """

    #region init

    def __init__(self):
        self.__output:_Path = _Path()
        self.__options_landbg:bool = True
        self.__options_landout:bool = True
        self.__options_alpha:bool = False

    #endregion

    #region pickle/unpickle

    @classmethod
    def unpickle(cls, data:bytes):
        try:
            instance = cls()
            f = _BytesIO(data)
            instance.__output = _Path(_data.DataUtil.read_string16_l(f))
            instance.__options_landbg = _data.DataUtil.read_U8(f) != 0
            instance.__options_landout = _data.DataUtil.read_U8(f) != 0
            instance.__options_alpha = _data.DataUtil.read_U8(f) != 0
            return instance
        except: return cls()
    
    def pickle(self):
        f = _BytesIO()
        _data.DataUtil.write_string16_l(f, str(self.__output))
        _data.DataUtil.write_U8(f, 1 if self.__options_landbg else 0)
        _data.DataUtil.write_U8(f, 1 if self.__options_landout else 0)
        _data.DataUtil.write_U8(f, 1 if self.__options_alpha else 0)
        return f.getvalue()

    #endregion

    #region properties

    @property
    def output(self):
        """ Output directory """
        return self.__output
    @output.setter
    def output(self, value:_Path):
        self.__output = value

    @property
    def options_landbg(self):
        """ Whether or not to show land background visual """
        return self.__options_landbg
    @options_landbg.setter
    def options_landbg(self, value:bool):
        self.__options_landbg = value

    @property
    def options_landout(self):
        """ Whether or not to show land outline visual """
        return self.__options_landout
    @options_landout.setter
    def options_landout(self, value:bool):
        self.__options_landout = value

    @property
    def options_alpha(self):
        """ Whether or not to normalize alpha """
        return self.__options_alpha
    @options_alpha.setter
    def options_alpha(self, value:bool):
        self.__options_alpha = value

    #endregion