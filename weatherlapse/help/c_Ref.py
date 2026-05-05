__all__ = [ 'Ref' ]

from typing import Generic as _Generic, TypeVar as _TypeVar

T = _TypeVar('T')

class Ref(_Generic[T]):
    """ Represents a reference to an object or value """

    #region init

    def __init__(self, initial:T):
        """
        Initializer for Ref

        :param initial: Initial referenced object or value
        """
        self.__value = initial

    #endregion

    #region properties

    @property
    def value(self) -> T:
        """ Referenced object or value """
        return self.__value
    @value.setter
    def value(self, _value:T):
        self.__value = _value
    
    #endregion