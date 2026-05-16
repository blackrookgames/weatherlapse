__all__ = [ 'AppInfo' ]

from pathlib import\
    Path as _Path

class AppInfo:
    """ Represents information about the app """

    #region init

    def __init__(self, apppath:_Path, iswindows:bool):
        """
        Initializer for AppInfo

        :param directory: Application directory
        :param iswindows: Whether or not this is running under Windows
        """
        self.__apppath = apppath.resolve()
        self.__appdir = self.__apppath.parent
        self.__appname = self.__apppath.name
        self.__configpath = _Path(f"{apppath}.config")
        self.__iswindows = iswindows
        self.__iconpath = _Path(f"{apppath}.icon{(".ico" if self.__iswindows else ".png")}")

    #endregion

    #region properties

    @property
    def apppath(self):
        """ Application path """
        return self.__apppath

    @property
    def appdir(self):
        """ Application directory """
        return self.__appdir

    @property
    def appname(self):
        """ Application name """
        return self.__appname
    
    @property
    def configpath(self):
        """ Path of configuration file """
        return self.__configpath
    
    @property
    def iswindows(self):
        """ Whether or not this is running under Windows """
        return self.__iswindows
    
    @property
    def iconpath(self):
        """ Path of window icon """
        return self.__iconpath
    
    #endregion