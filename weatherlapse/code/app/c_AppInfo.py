__all__ = [ 'AppInfo' ]

from pathlib import\
    Path as _Path

import code.engine.objtypes as _objtypes

class AppInfo:
    """ Represents information about the app """

    #region init

    def __init__(self, appdir:_Path, iswindows:bool):
        """
        Initializer for AppInfo

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