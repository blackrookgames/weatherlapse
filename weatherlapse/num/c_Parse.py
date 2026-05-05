__all__ = [ 'Parse' ]

from enum import Enum as _Enum
from typing import TypeVar as _TypeVar

from .c_U8 import U8 as _U8, U8_MIN as _U8_MIN
from .c_I8 import I8 as _I8, I8_MIN as _I8_MIN
from .c_U16 import U16 as _U16, U16_MIN as _U16_MIN
from .c_I16 import I16 as _I16, I16_MIN as _I16_MIN
from .c_U32 import U32 as _U32, U32_MIN as _U32_MIN
from .c_I32 import I32 as _I32, I32_MIN as _I32_MIN
from .c_U64 import U64 as _U64, U64_MIN as _U64_MIN
from .c_I64 import I64 as _I64, I64_MIN as _I64_MIN

from .c_ParseError import ParseError as _ParseError
from .c_ParseResult import ParseResult as _ParseResult

TEnum = _TypeVar('TEnum', bound = _Enum)

class Parse:
    """ Utility for parsing data """

    #region helper methods

    @classmethod
    def __normalize(cls, s:str):
        return s.strip().lower()
    
    @classmethod
    def __badvalue(cls, s:str, desc:str):
        return _ParseError(f"\"{s.strip()}\" is not a valid {desc} value.")

    #endregion

    #region int

    @classmethod
    def to_int(cls, s:str):
        """
        Parses a string to an integer

        :param s: String to parse
        :return: Parsed value
        :raises ParseError: String is not valid
        """
        try:
            ss = cls.__normalize(s)
            if len(ss) > 1:
                match ss[1]:
                    case 'b': return int(ss[2:], base = 2)
                    case 'x': return int(ss[2:], base = 16)
            return int(ss)
        except: e = cls.__badvalue(s, "integer")
        raise e
    
    @classmethod
    def try_int(cls, s:str):
        """
        Attempts to parse a string to an integer

        :param s: String to parse
        :return: Parse result
        """
        try: return _ParseResult[int](cls.to_int(s), None)
        except _ParseError as _e: return _ParseResult[int](0, _e)
    
    #endregion

    #region float

    @classmethod
    def to_float(cls, s:str):
        """
        Parses a string to a float

        :param s: String to parse
        :return: Parsed value
        :raises ParseError: String is not valid
        """
        try: return float(cls.__normalize(s))
        except: e = cls.__badvalue(s, "floating-point")
        raise e
    
    @classmethod
    def try_float(cls, s:str):
        """
        Attempts to parse a string to a float

        :param s: String to parse
        :return: Parse result
        """
        try: return _ParseResult[float](cls.to_float(s), None)
        except _ParseError as _e: return _ParseResult[float](0, _e)
    
    #endregion

    #region enum

    @classmethod
    def to_enum(cls, t:type[TEnum], s:str) -> TEnum:
        """
        Parses a string to an enum value

        :param t: Enum type
        :param s: String to parse
        :return: Parsed value
        :raises ParseError: String is not valid
        """
        try: return t[s.strip()] # Do NOT call __normalize
        except: e = cls.__badvalue(s, t.__name__)
        raise e
    
    @classmethod
    def try_enum(cls, t:type[TEnum], s:str) -> _ParseResult[TEnum]:
        """
        Attempts to parse a string to an enum value

        :param t: Enum type
        :param s: String to parse
        :return: Parse result
        """
        try: return _ParseResult[TEnum](cls.to_enum(t, s), None)
        except _ParseError as _e: return _ParseResult[TEnum](next(iter(t)), _e)
    
    #endregion

    #region U8, I8, U16, I16, U32, I32, U64, I64

    #region U8

    @classmethod
    def to_U8(cls, s:str): 
        """
        Parses a string to an 8-bit unsigned integer

        :param s: String to parse
        :return: Parsed value
        :raises ParseError: String is not valid
        """
        try:
            raw = cls.to_int(s)
            val = _U8(raw)
            if raw != val: raise cls.__badvalue(s, "8-bit unsigned integer")
            return val
        except _ParseError as _e: e = _e
        raise e
    
    @classmethod
    def try_U8(cls, s:str):
        """
        Attempts to parse a string to an 8-bit unsigned integer

        :param s: String to parse
        :return: Parse result
        """
        try: return _ParseResult[_U8](cls.to_U8(s), None)
        except _ParseError as _e: return _ParseResult[_U8](_U8_MIN, _e)
    
    #endregion

    #region I8

    @classmethod
    def to_I8(cls, s:str): 
        """
        Parses a string to an 8-bit signed integer

        :param s: String to parse
        :return: Parsed value
        :raises ParseError: String is not valid
        """
        try:
            raw = cls.to_int(s)
            val = _I8(raw)
            if raw != val: raise cls.__badvalue(s, "8-bit signed integer")
            return val
        except _ParseError as _e: e = _e
        raise e
    
    @classmethod
    def try_I8(cls, s:str):
        """
        Attempts to parse a string to an 8-bit signed integer

        :param s: String to parse
        :return: Parse result
        """
        try: return _ParseResult[_I8](cls.to_I8(s), None)
        except _ParseError as _e: return _ParseResult[_I8](_I8_MIN, _e)
    
    #endregion

    #region U16

    @classmethod
    def to_U16(cls, s:str): 
        """
        Parses a string to a 16-bit unsigned integer

        :param s: String to parse
        :return: Parsed value
        :raises ParseError: String is not valid
        """
        try:
            raw = cls.to_int(s)
            val = _U16(raw)
            if raw != val: raise cls.__badvalue(s, "16-bit unsigned integer")
            return val
        except _ParseError as _e: e = _e
        raise e
    
    @classmethod
    def try_U16(cls, s:str):
        """
        Attempts to parse a string to a 16-bit unsigned integer

        :param s: String to parse
        :return: Parse result
        """
        try: return _ParseResult[_U16](cls.to_U16(s), None)
        except _ParseError as _e: return _ParseResult[_U16](_U16_MIN, _e)
    
    #endregion

    #region I16

    @classmethod
    def to_I16(cls, s:str): 
        """
        Parses a string to a 16-bit signed integer

        :param s: String to parse
        :return: Parsed value
        :raises ParseError: String is not valid
        """
        try:
            raw = cls.to_int(s)
            val = _I16(raw)
            if raw != val: raise cls.__badvalue(s, "16-bit signed integer")
            return val
        except _ParseError as _e: e = _e
        raise e
    
    @classmethod
    def try_I16(cls, s:str):
        """
        Attempts to parse a string to a 16-bit signed integer

        :param s: String to parse
        :return: Parse result
        """
        try: return _ParseResult[_I16](cls.to_I16(s), None)
        except _ParseError as _e: return _ParseResult[_I16](_I16_MIN, _e)
    
    #endregion

    #region U32

    @classmethod
    def to_U32(cls, s:str): 
        """
        Parses a string to a 32-bit unsigned integer

        :param s: String to parse
        :return: Parsed value
        :raises ParseError: String is not valid
        """
        try:
            raw = cls.to_int(s)
            val = _U32(raw)
            if raw != val: raise cls.__badvalue(s, "32-bit unsigned integer")
            return val
        except _ParseError as _e: e = _e
        raise e
    
    @classmethod
    def try_U32(cls, s:str):
        """
        Attempts to parse a string to a 32-bit unsigned integer

        :param s: String to parse
        :return: Parse result
        """
        try: return _ParseResult[_U32](cls.to_U32(s), None)
        except _ParseError as _e: return _ParseResult[_U32](_U32_MIN, _e)
    
    #endregion

    #region I32

    @classmethod
    def to_I32(cls, s:str): 
        """
        Parses a string to a 32-bit signed integer

        :param s: String to parse
        :return: Parsed value
        :raises ParseError: String is not valid
        """
        try:
            raw = cls.to_int(s)
            val = _I32(raw)
            if raw != val: raise cls.__badvalue(s, "32-bit signed integer")
            return val
        except _ParseError as _e: e = _e
        raise e
    
    @classmethod
    def try_I32(cls, s:str):
        """
        Attempts to parse a string to a 32-bit signed integer

        :param s: String to parse
        :return: Parse result
        """
        try: return _ParseResult[_I32](cls.to_I32(s), None)
        except _ParseError as _e: return _ParseResult[_I32](_I32_MIN, _e)
    
    #endregion

    #region U64

    @classmethod
    def to_U64(cls, s:str): 
        """
        Parses a string to a 64-bit unsigned integer

        :param s: String to parse
        :return: Parsed value
        :raises ParseError: String is not valid
        """
        try:
            raw = cls.to_int(s)
            val = _U64(raw)
            if raw != val: raise cls.__badvalue(s, "64-bit unsigned integer")
            return val
        except _ParseError as _e: e = _e
        raise e
    
    @classmethod
    def try_U64(cls, s:str):
        """
        Attempts to parse a string to a 64-bit unsigned integer

        :param s: String to parse
        :return: Parse result
        """
        try: return _ParseResult[_U64](cls.to_U64(s), None)
        except _ParseError as _e: return _ParseResult[_U64](_U64_MIN, _e)
    
    #endregion

    #region I64

    @classmethod
    def to_I64(cls, s:str): 
        """
        Parses a string to a 64-bit signed integer

        :param s: String to parse
        :return: Parsed value
        :raises ParseError: String is not valid
        """
        try:
            raw = cls.to_int(s)
            val = _I64(raw)
            if raw != val: raise cls.__badvalue(s, "64-bit signed integer")
            return val
        except _ParseError as _e: e = _e
        raise e
    
    @classmethod
    def try_I64(cls, s:str):
        """
        Attempts to parse a string to a 64-bit signed integer

        :param s: String to parse
        :return: Parse result
        """
        try: return _ParseResult[_I64](cls.to_I64(s), None)
        except _ParseError as _e: return _ParseResult[_I64](_I64_MIN, _e)
    
    #endregion

    #endregion
