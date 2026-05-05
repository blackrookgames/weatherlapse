# Auto-generated
__all__ = [ 'U64', 'U64_MIN', 'U64_MAX', 'U64_SIZE' ]
from typing import SupportsInt as _SupportsInt
from .c_Integer import Integer as _Integer
class U64(_Integer):
    _BITS = 64
    _MASK = 18446744073709551615
    _NEGFIX = 18446744073709551616
    def __init__(self, value:'int|_SupportsInt' = 0):
        self.__value = self._unsigned(value, self._MASK, self._BITS, self._NEGFIX)
    def __int__(self): return self.__value
    def __repr__(self): return f"U8(value = self.__value)"
    def __index__(self): return self._unsigned(self.__value, self._MASK, self._BITS, self._NEGFIX)
    @classmethod
    def clamp(cls, value:int):
        """ Creates an U64 by clamping a value """
        return cls(value = max(0, min(18446744073709551615, value)))
U64_MIN = U64(0)
U64_MAX = U64(18446744073709551615)
U64_SIZE = 8
