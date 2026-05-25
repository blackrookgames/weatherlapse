__all__ = ['ROList']

from typing import \
    Generic as _Generic,\
    TypeVar as _TypeVar

T = _TypeVar('T')

class ROList(_Generic[T]):
    """ Represents read-only access to a list """

    #region init

    def __init__(self, src:list[T]):
        """

        Initializer for ROList

        :param src:
            Source list

        """
        self.__src = src

    #endregion

    #region operators

    def __len__(self):
        return len(self.__src)

    def __getitem__(self, index:int):
        try: return self.__src[index]
        except:
            if index >= 0 and index < len(self.__src):
                raise
        raise IndexError("Index is out of range.")
    
    def __iter__(self):
        for _item in self.__src:
            yield _item

    def __contains__(self, item):
        return item in self.__src

    #endregion