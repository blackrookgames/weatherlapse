# Auto-generated
__all__ = [ 'U8', 'U8_MIN', 'U8_MAX', 'U8_SIZE' ]
from typing import SupportsInt as _SupportsInt
from .c_Integer import Integer as _Integer
class U8(_Integer):
    _BITS = 8
    _MASK = 255
    _NEGFIX = 256
    def __init__(self, value:'int|_SupportsInt' = 0):
        self.__value = self._unsigned(value, self._MASK, self._BITS, self._NEGFIX)
    def __int__(self): return self.__value
    def __repr__(self): return f"U8(value = self.__value)"
    def __index__(self): return self._unsigned(self.__value, self._MASK, self._BITS, self._NEGFIX)
    @classmethod
    def clamp(cls, value:int):
        """ Creates an U8 by clamping a value """
        return cls(value = max(0, min(255, value)))
U8_MIN = U8(0)
U8_MAX = U8(255)
U8_SIZE = 1
