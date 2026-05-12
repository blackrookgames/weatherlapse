# Auto-generated
__all__ = [ 'I64', 'I64_MIN', 'I64_MAX', 'I64_SIZE' ]
from typing import SupportsInt as _SupportsInt
from .c_Integer import Integer as _Integer
class I64(_Integer):
    _BITS = 64
    _MASK = 18446744073709551615
    _NEGFIX = 18446744073709551616
    def __init__(self, value:'int|_SupportsInt' = 0):
        self.__value = self._signed(value, self._MASK, self._BITS, self._NEGFIX)
    def __int__(self): return self.__value
    def __repr__(self): return f"U8(value = self.__value)"
    def __index__(self): return self._unsigned(self.__value, self._MASK, self._BITS, self._NEGFIX)
    @classmethod
    def clamp(cls, value:int):
        """ Creates an I64 by clamping a value """
        return cls(value = max(-9223372036854775808, min(9223372036854775807, value)))
I64_MIN = I64(-9223372036854775808)
I64_MAX = I64(9223372036854775807)
I64_SIZE = 8
