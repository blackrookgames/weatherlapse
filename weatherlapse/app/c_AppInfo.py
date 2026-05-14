__all__ = [ 'AppInfo' ]

from pathlib import\
    Path as _Path

class AppInfo:
    """ Represents information about the app """

    #region init

    def __init__(self, directory:_Path, iswindows:bool):
        """
        Initializer for AppInfo

        :param directory: Application directory
        :param iswindows: Whether or not this is running under Windows
        """
        self.__directory = directory.resolve()
        self.__configpath = _Path(f"{self.__directory}.config")
        self.__iswindows = iswindows
        self.__iconpath = _Path(f"{self.__directory}.icon{(".ico" if self.__iswindows else ".png")}")

    #endregion

    #region properties

    @property
    def directory(self):
        """ Application directory """
        return self.__directory
    
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