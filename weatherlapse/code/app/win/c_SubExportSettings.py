__all__ = ['SubExportSettings']

from pathlib import Path as _Path

class SubExportSettings:
    """ Represents a export settings """

    output:_Path = _Path()
    """ Output directory """

    options_landbg:bool = True
    """ Whether or not to show land background visual """

    options_landout:bool = True
    """ Whether or not to show land outline visual """

    options_alpha:bool = False
    """ Whether or not to normalize alpha """