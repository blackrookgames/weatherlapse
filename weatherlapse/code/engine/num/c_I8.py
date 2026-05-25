# Auto-generated
__all__ = [ 'I8', 'I8_MIN', 'I8_MAX', 'I8_SIZE' ]
from typing import SupportsInt as _SupportsInt
from .c_Integer import Integer as _Integer
class I8(_Integer):
    _BITS = 8
    _MASK = 255
    _NEGFIX = 256
    def __init__(self, value:'int|_SupportsInt' = 0):
        self.__value = self._signed(value, self._MASK, self._BITS, self._NEGFIX)
    def __int__(self): return self.__value
    def __repr__(self): return f"U8(value = self.__value)"
    def __index__(self): return self._unsigned(self.__value, self._MASK, self._BITS, self._NEGFIX)
    @classmethod
    def clamp(cls, value:int):
        """ Creates an I8 by clamping a value """
        return cls(value = max(-128, min(127, value)))
I8_MIN = I8(-128)
I8_MAX = I8(127)
I8_SIZE = 1
