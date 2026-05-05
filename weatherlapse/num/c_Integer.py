__all__ = [ 'Integer' ]

from typing import SupportsInt as _SupportsInt

class Integer:

    #region operators

    def __int__(self) -> int: raise NotImplementedError("__init__ has not been implemented")
    
    def __float__(self): return float(int(self))
    def __str__(self): return str(int(self))

    def __hash__(self):
        return int(self)
    
    def __eq__(self, other):
        if isinstance(other, int): return int(self) == other
        if isinstance(other, _SupportsInt): return int(self) == int(other)
        return False
    
    def __ne__(self, other):
        if isinstance(other, int): return int(self) != other
        if isinstance(other, _SupportsInt): return int(self) != int(other)
        return True
    
    def __gt__(self, other) -> bool:
        if isinstance(other, int): return int(self) > other
        if isinstance(other, _SupportsInt): return int(self) > int(other)
        return NotImplemented
    
    def __ge__(self, other) -> bool:
        if isinstance(other, int): return int(self) >= other
        if isinstance(other, _SupportsInt): return int(self) >= int(other)
        return NotImplemented
    
    def __lt__(self, other) -> bool:
        if isinstance(other, int): return int(self) < other
        if isinstance(other, _SupportsInt): return int(self) < int(other)
        return NotImplemented
    
    def __le__(self, other) -> bool:
        if isinstance(other, int): return int(self) <= other
        if isinstance(other, _SupportsInt): return int(self) <= int(other)
        return NotImplemented
    
    def __neg__(self) -> int:
        return -int(self)
    
    def __add__(self, other) -> int:
        if isinstance(other, int): return int(self) + other
        if isinstance(other, _SupportsInt): return int(self) + int(other)
        return NotImplemented
    
    def __sub__(self, other) -> int:
        if isinstance(other, int): return int(self) - other
        if isinstance(other, _SupportsInt): return int(self) - int(other)
        return NotImplemented
    
    def __mul__(self, other) -> int:
        if isinstance(other, int): return int(self) * other
        if isinstance(other, _SupportsInt): return int(self) * int(other)
        return NotImplemented
    
    def __floordiv__(self, other) -> int:
        if isinstance(other, int): return int(self) // other
        if isinstance(other, _SupportsInt): return int(self) // int(other)
        return NotImplemented

    #endregion

    #region protected methods

    @classmethod
    def __unsigned_int(cls,  value:int, mask:int, bits:int, negfix:int):
        if value >= 0: return value & mask
        value_size = value.bit_length()
        if value_size < bits: return negfix + value
        return ((1 << (value_size + 1)) + value) & mask

    @classmethod
    def _unsigned(cls, value:'int|_SupportsInt', mask:int, bits:int, negfix:int):
        return cls.__unsigned_int(value if isinstance(value, int) else int(value), mask, bits, negfix)

    @classmethod
    def _signed(cls, value:'int|_SupportsInt', mask:int, bits:int, negfix:int):
        _value = cls._unsigned(value, mask, bits, negfix)
        if _value < (negfix // 2): return _value
        return _value - negfix
    
    #endregion