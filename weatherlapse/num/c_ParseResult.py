__all__ = [ 'ParseResult' ]

from typing import Generic as _Generic, TypeVar as _TypeVar

from .c_ParseError import ParseError as _ParseError

T = _TypeVar('T')

class ParseResult(_Generic[T]):
    """ Represents a parse result """

    #region init

    def __init__(self, value:T, error:None|_ParseError):
        """
        Initializer for ParseResult

        :param value: Result value
        :param error: Error raised while parsing
        """
        self.__value = value
        self.__error = error
        self.__success = self.__error is None

    #endregion

    #region operator

    def __bool__(self): return self.__success

    #endregion

    #region properties

    @property
    def value(self):
        """ Result value """
        return self.__value
    
    @property
    def error(self):
        """ Error raised while parsing """
        return self.__error
    
    @property
    def success(self):
        """ Whether or not successful """
        return self.__success

    #endregion