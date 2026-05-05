# Auto-generated
__all__ = [ 'U32', 'U32_MIN', 'U32_MAX', 'U32_SIZE' ]
from typing import SupportsInt as _SupportsInt
from .c_Integer import Integer as _Integer
class U32(_Integer):
    _BITS = 32
    _MASK = 4294967295
    _NEGFIX = 4294967296
    def __init__(self, value:'int|_SupportsInt' = 0):
        self.__value = self._unsigned(value, self._MASK, self._BITS, self._NEGFIX)
    def __int__(self): return self.__value
    def __repr__(self): return f"U8(value = self.__value)"
    def __index__(self): return self._unsigned(self.__value, self._MASK, self._BITS, self._NEGFIX)
    @classmethod
    def clamp(cls, value:int):
        """ Creates an U32 by clamping a value """
        return cls(value = max(0, min(4294967295, value)))
U32_MIN = U32(0)
U32_MAX = U32(4294967295)
U32_SIZE = 4
