__all__ = [ 'Info' ]

from io import\
    BytesIO as _BytesIO,\
    StringIO as _StringIO
from pathlib import\
    Path as _Path

import code.engine.data as _data
import code.engine.num as _num
import code.engine.objtypes as _objtypes

class Info(_data.Picklable['Info']):
    """ Represents information about the app """

    #region init

    def __init__(self, appdir:_Path, iswindows:bool):
        """
        Initializer for Info

        :param directory: Application directory
        :param iswindows: Whether or not this is running under Windows
        """
        self.__app_dir = appdir.resolve()
        self.__app_name = self.__app_dir.name
        self.__parent_dir = self.__app_dir.parent
        self.__config_path = self.__app_dir.joinpath("config.xml")
        self.__assets_dir = self.__app_dir.joinpath("assets")
        self.__cache_dir = self.__app_dir.joinpath(".cache")
        self.__iswindows = iswindows
        self.__icon_path = self.__assets_dir.joinpath(f"icon{(".ico" if self.__iswindows else ".png")}")

    #endregion

    #region pickle

    def pickle(self):
        f = _BytesIO()
        # appdir
        appdir = str(self.__app_dir)
        f.write(_num.Pickle.pickle_I32_l(len(appdir)))
        for _c in appdir: f.write(_num.Pickle.pickle_U16_l(ord(_c)))
        # iswindows
        f.write(_num.Pickle.pickle_U8(0x01 if self.__iswindows else 0x00))
        # Return
        return f.getvalue()

    @classmethod
    def unpickle(cls, data: bytes):
        try:
            f = _BytesIO(data)
            # appdir
            appdir_length = _num.Pickle.unpickle_I32_l(f.read(4))
            with _StringIO() as _appdir:
                for _ in range(appdir_length):
                    _appdir.write(chr(_num.Pickle.unpickle_U16_l(f.read(2))))
                appdir = _appdir.getvalue()
            # iswindows
            iswindows = _num.Pickle.unpickle_U8(f.read(1)) != 0
            # Return
            return cls(_Path(appdir), iswindows)
        except: return cls(_Path(), False)

    #endregion

    #region properties

    @property
    def app_dir(self):
        """ Application directory """
        return self.__app_dir

    @property
    def app_name(self):
        """ Application name """
        return self.__app_name

    @property
    def parent_dir(self):
        """ Application parent directory """
        return self.__parent_dir
    
    @property
    def config_path(self):
        """ Path of configuration file """
        return self.__config_path
    
    @property
    def assets_dir(self):
        """ Assets directory """
        return self.__assets_dir
    
    @property
    def cache_dir(self):
        """ Cache directory """
        return self.__cache_dir
    
    @property
    def iswindows(self):
        """ Whether or not this is running under Windows """
        return self.__iswindows
    
    @property
    def icon_path(self):
        """ Path of window icon """
        return self.__icon_path

    #endregion

    #region methods

    def cache_world_bg_path(self, region:_objtypes.ConfigRegion, fill:bool):
        """
        Computes a path for a cached background image

        :param region: Region coordinates
        :param fill: Whether or not background to made of filled polygons
        """
        zoom, min_x, min_y, max_x, max_y = region.normalize()
        return self.__cache_dir.joinpath(f"{zoom}_{min_x}_{min_y}_{max_x}_{max_y}_{('f' if fill else 'o')}.png")
    
    #endregion