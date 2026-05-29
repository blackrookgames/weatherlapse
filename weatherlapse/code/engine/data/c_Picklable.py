__all__ = [ 'Picklable' ]

from typing import\
    Generic as _Generic,\
    TypeVar as _TypeVar

T = _TypeVar('T')

class Picklable(_Generic[T]):
    """ Represents an object with picklable data """

    @classmethod
    def unpickle(cls, data:bytes) -> T:
        """
        Creates an instance by unpickling data

        :param data: Pickled data
        :return: Created instance
        :raises BadDataError: Pickled data is invalid
        """
        raise NotImplementedError("unpickle has not been implemented")
    
    def pickle(self) -> bytes:
        """
        Pickles the data within the instance

        :return: Pickled data
        """
        raise NotImplementedError("pickle has not been implemented")