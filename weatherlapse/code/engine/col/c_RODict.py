__all__ = ['RODict']

from typing import \
    Generic as _Generic,\
    TypeVar as _TypeVar

TKey = _TypeVar('TKey')
TValue = _TypeVar('TValue')

class RODict(_Generic[TKey, TValue]):
    """ Represents read-only access to a dictionary """

    #region init

    def __init__(self, src:dict[TKey, TValue]):
        """
        Initializer for RODict

        :param src: Source list
        """
        self.__src = src

    #endregion

    #region operators

    def __len__(self):
        return len(self.__src)

    def __getitem__(self, key:TKey):
        try: return self.__src[key]
        except:
            if key in self.__src: raise
        raise KeyError("Could not find the specified key.")
    
    def __iter__(self):
        for _name in self.__src: yield _name

    def __contains__(self, key:TKey):
        return key in self.__src

    #endregion

    #region properties

    def iter_items(self):
        """ Iterates thru all items in the dictionary """
        for _item in self.__src.items(): yield _item

    def iter_keys(self):
        """ Iterates thru all keys in the dictionary """
        for _key in self.__src.keys(): yield _key

    def iter_values(self):
        """ Iterates thru all values in the dictionary """
        for _value in self.__src.values(): yield _value

    def items(self):
        """
        Retrieves a copy of all items in the dictionary
        
        :return: List of all items in the dictionary
        """
        return [_item for _item in self.iter_items()]

    def keys(self):
        """
        Retrieves a copy of all keys in the dictionary
        
        :return: List of all keys in the dictionary
        """
        return [_key for _key in self.iter_keys()]

    def values(self):
        """
        Retrieves a copy of all values in the dictionary
        
        :return: List of all values in the dictionary
        """
        return [_value for _value in self.iter_values()]
        
    def find_value(self, key:TKey):
        """
        Searches the dictionary for the value of the specified key

        :param key: Key
        :return: Value of found key (or None if key could not be found)
        """
        if key in self.__src:
            return self.__src[key]
        return None
    
    def find_key(self, value:TValue):
        """
        Searches the dictionary for the key with the specified value

        :param value: Value
        :return: Key with the specified value (or None if no key has the specified value)
        """
        for _k, _v in self.__src.items():
            if _v == value: return _k
        return None

    #endregion