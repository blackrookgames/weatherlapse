__all__ = [ 'AppInfo' ]

from pathlib import\
    Path as _Path

class AppInfo:
    """ Represents information about the app """

    #region init

    def __init__(self, directory:_Path):
        """
        Initializer for AppInfo

        :param directory:
            Application directory
        """
        self.__directory = directory.resolve()
        self.__configpath = _Path(f"{self.__directory}.config")

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

    #endregion