# Auto-generated
__all__ = [ 'U16', 'U16_MIN', 'U16_MAX', 'U16_SIZE' ]
from typing import SupportsInt as _SupportsInt
from .c_Integer import Integer as _Integer
class U16(_Integer):
    _BITS = 16
    _MASK = 65535
    _NEGFIX = 65536
    def __init__(self, value:'int|_SupportsInt' = 0):
        self.__value = self._unsigned(value, self._MASK, self._BITS, self._NEGFIX)
    def __int__(self): return self.__value
    def __repr__(self): return f"U8(value = self.__value)"
    def __index__(self): return self._unsigned(self.__value, self._MASK, self._BITS, self._NEGFIX)
    @classmethod
    def clamp(cls, value:int):
        """ Creates an U16 by clamping a value """
        return cls(value = max(0, min(65535, value)))
U16_MIN = U16(0)
U16_MAX = U16(65535)
U16_SIZE = 2
