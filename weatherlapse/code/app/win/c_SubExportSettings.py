__all__ = ['SubExportSettings']

from io import\
    BytesIO as _BytesIO

from pathlib import Path as _Path

import code.engine.data as _data

class SubExportSettings:
    """ Represents a export settings """

    #region pickle/unpickle

    @classmethod
    def unpickle(cls, data:bytes):
        try:
            f = _BytesIO(data)
            cls.output = _Path(_data.DataUtil.read_string16_l(f))
            cls.options_landbg = _data.DataUtil.read_U8(f) != 0
            cls.options_landout = _data.DataUtil.read_U8(f) != 0
            cls.options_alpha = _data.DataUtil.read_U8(f) != 0
        except:
            cls.output = _Path()
            cls.options_landbg = True
            cls.options_landout = True
            cls.options_alpha = False

    @classmethod
    def pickle(cls):
        f = _BytesIO()
        _data.DataUtil.write_string16_l(f, str(cls.output))
        _data.DataUtil.write_U8(f, 1 if cls.options_landbg else 0)
        _data.DataUtil.write_U8(f, 1 if cls.options_landout else 0)
        _data.DataUtil.write_U8(f, 1 if cls.options_alpha else 0)
        return f.getvalue()

    #endregion

    #region fields

    output:_Path = _Path()
    """ Output directory """

    options_landbg:bool = True
    """ Whether or not to show land background visual """

    options_landout:bool = True
    """ Whether or not to show land outline visual """

    options_alpha:bool = False
    """ Whether or not to normalize alpha """

    #endregion