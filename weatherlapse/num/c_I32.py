# Auto-generated
__all__ = [ 'I32', 'I32_MIN', 'I32_MAX', 'I32_SIZE' ]
from typing import SupportsInt as _SupportsInt
from .c_Integer import Integer as _Integer
class I32(_Integer):
    _BITS = 32
    _MASK = 4294967295
    _NEGFIX = 4294967296
    def __init__(self, value:'int|_SupportsInt' = 0):
        self.__value = self._signed(value, self._MASK, self._BITS, self._NEGFIX)
    def __int__(self): return self.__value
    def __repr__(self): return f"U8(value = self.__value)"
    def __index__(self): return self._unsigned(self.__value, self._MASK, self._BITS, self._NEGFIX)
    @classmethod
    def clamp(cls, value:int):
        """ Creates an I32 by clamping a value """
        return cls(value = max(-2147483648, min(2147483647, value)))
I32_MIN = I32(-2147483648)
I32_MAX = I32(2147483647)
I32_SIZE = 4
