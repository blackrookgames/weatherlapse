__all__ = ['DataUtil']

import io as _io

from dataclasses import\
    dataclass as _dataclass
from typing import\
    Callable as _Callable

import code.engine.num as _num

class DataUtil:
    """ Utility for data-related operations """

    #region Prim

    @_dataclass(frozen = True)
    class _Prim:
        write_U16:_Callable[[_io.BufferedWriter|_io.BytesIO, _num.U16|int], None]
        read_U16:_Callable[[_io.BufferedReader|_io.BytesIO], _num.U16]
        write_I16:_Callable[[_io.BufferedWriter|_io.BytesIO, _num.I16|int], None]
        read_I16:_Callable[[_io.BufferedReader|_io.BytesIO], _num.I16]
        write_U32:_Callable[[_io.BufferedWriter|_io.BytesIO, _num.U32|int], None]
        read_U32:_Callable[[_io.BufferedReader|_io.BytesIO], _num.U32]
        write_I32:_Callable[[_io.BufferedWriter|_io.BytesIO, _num.I32|int], None]
        read_I32:_Callable[[_io.BufferedReader|_io.BytesIO], _num.I32]
        write_U64:_Callable[[_io.BufferedWriter|_io.BytesIO, _num.U64|int], None]
        read_U64:_Callable[[_io.BufferedReader|_io.BytesIO], _num.U64]
        write_I64:_Callable[[_io.BufferedWriter|_io.BytesIO, _num.I64|int], None]
        read_I64:_Callable[[_io.BufferedReader|_io.BytesIO], _num.I64]
        write_single:_Callable[[_io.BufferedWriter|_io.BytesIO, float], None]
        read_single:_Callable[[_io.BufferedReader|_io.BytesIO], float]
        write_double:_Callable[[_io.BufferedWriter|_io.BytesIO, float], None]
        read_double:_Callable[[_io.BufferedReader|_io.BytesIO], float]

    #endregion

    #region string16

    @classmethod
    def __write_string16(cls, prim:'DataUtil._Prim', f:_io.BufferedWriter|_io.BytesIO, value:str):
        prim.write_I32(f, len(value))
        for c in value: prim.write_U16(f, ord(c))

    @classmethod
    def __read_string16(cls, prim:'DataUtil._Prim', f:_io.BufferedReader|_io.BytesIO):
        with _io.StringIO() as s:
            length = prim.read_I32(f)
            for _ in range(length): s.write(chr(prim.read_U16(f)))
            return s.getvalue()
        
    @classmethod
    def write_string16(cls, f:_io.BufferedWriter|_io.BytesIO, value:str, big:bool):
        if big: cls.write_string16_b(f, value)
        else: cls.write_string16_l(f, value)
        
    @classmethod
    def write_string16_l(cls, f:_io.BufferedWriter|_io.BytesIO, value:str):
        cls.__write_string16(cls.PRIM_L, f, value)
        
    @classmethod
    def write_string16_b(cls, f:_io.BufferedWriter|_io.BytesIO, value:str):
        cls.__write_string16(cls.PRIM_B, f, value)
        
    @classmethod
    def read_string16(cls, f:_io.BufferedReader|_io.BytesIO, big:bool):
        return cls.read_string16_b(f) if big else cls.read_string16_l(f)
        
    @classmethod
    def read_string16_l(cls, f:_io.BufferedReader|_io.BytesIO):
        return cls.__read_string16(cls.PRIM_L, f)
        
    @classmethod
    def read_string16_b(cls, f:_io.BufferedReader|_io.BytesIO):
        return cls.__read_string16(cls.PRIM_B, f)
        
    #endregion

    #region U8

    @classmethod
    def write_U8(cls, f:_io.BufferedWriter|_io.BytesIO, value:_num.U8|int):
        f.write(_num.Pickle.pickle_U8(value))
    
    @classmethod
    def read_U8(cls, f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_U8(f.read(1))

    #endregion

    #region I8

    @classmethod
    def write_I8(cls, f:_io.BufferedWriter|_io.BytesIO, value:_num.I8|int):
        f.write(_num.Pickle.pickle_I8(value))
    
    @classmethod
    def read_I8(cls, f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_I8(f.read(1))

    #endregion

    #region U16

    @classmethod
    def write_U16(cls, f:_io.BufferedWriter|_io.BytesIO, value:_num.U16|int, big:bool):
        return cls.write_U16_b(f, value) if big else cls.write_U16_l(f, value)

    @staticmethod
    def write_U16_l(f:_io.BufferedWriter|_io.BytesIO, value:_num.U16|int):
        f.write(_num.Pickle.pickle_U16_l(value))

    @staticmethod
    def write_U16_b(f:_io.BufferedWriter|_io.BytesIO, value:_num.U16|int):
        f.write(_num.Pickle.pickle_U16_b(value))
    
    @classmethod
    def read_U16(cls, f:_io.BufferedReader|_io.BytesIO, big:bool):
        return cls.read_U16_b(f) if big else cls.read_U16_l(f)
    
    @staticmethod
    def read_U16_l(f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_U16_l(f.read(2))
    
    @staticmethod
    def read_U16_b(f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_U16_b(f.read(2))
    
    #endregion
    
    #region I16

    @classmethod
    def write_I16(cls, f:_io.BufferedWriter|_io.BytesIO, value:_num.I16|int, big:bool):
        return cls.write_I16_b(f, value) if big else cls.write_I16_l(f, value)

    @staticmethod
    def write_I16_l(f:_io.BufferedWriter|_io.BytesIO, value:_num.I16|int):
        f.write(_num.Pickle.pickle_I16_l(value))

    @staticmethod
    def write_I16_b(f:_io.BufferedWriter|_io.BytesIO, value:_num.I16|int):
        f.write(_num.Pickle.pickle_I16_b(value))
    
    @classmethod
    def read_I16(cls, f:_io.BufferedReader|_io.BytesIO, big:bool):
        return cls.read_I16_b(f) if big else cls.read_I16_l(f)
    
    @staticmethod
    def read_I16_l(f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_I16_l(f.read(2))
    
    @staticmethod
    def read_I16_b(f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_I16_b(f.read(2))
    
    #endregion

    #region U32

    @classmethod
    def write_U32(cls, f:_io.BufferedWriter|_io.BytesIO, value:_num.U32|int, big:bool):
        return cls.write_U32_b(f, value) if big else cls.write_U32_l(f, value)

    @staticmethod
    def write_U32_l(f:_io.BufferedWriter|_io.BytesIO, value:_num.U32|int):
        f.write(_num.Pickle.pickle_U32_l(value))

    @staticmethod
    def write_U32_b(f:_io.BufferedWriter|_io.BytesIO, value:_num.U32|int):
        f.write(_num.Pickle.pickle_U32_b(value))
    
    @classmethod
    def read_U32(cls, f:_io.BufferedReader|_io.BytesIO, big:bool):
        return cls.read_U32_b(f) if big else cls.read_U32_l(f)
    
    @staticmethod
    def read_U32_l(f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_U32_l(f.read(4))
    
    @staticmethod
    def read_U32_b(f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_U32_b(f.read(4))
    
    #endregion
    
    #region I32

    @classmethod
    def write_I32(cls, f:_io.BufferedWriter|_io.BytesIO, value:_num.I32|int, big:bool):
        return cls.write_I32_b(f, value) if big else cls.write_I32_l(f, value)

    @staticmethod
    def write_I32_l(f:_io.BufferedWriter|_io.BytesIO, value:_num.I32|int):
        f.write(_num.Pickle.pickle_I32_l(value))

    @staticmethod
    def write_I32_b(f:_io.BufferedWriter|_io.BytesIO, value:_num.I32|int):
        f.write(_num.Pickle.pickle_I32_b(value))
    
    @classmethod
    def read_I32(cls, f:_io.BufferedReader|_io.BytesIO, big:bool):
        return cls.read_I32_b(f) if big else cls.read_I32_l(f)
    
    @staticmethod
    def read_I32_l(f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_I32_l(f.read(4))
    
    @staticmethod
    def read_I32_b(f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_I32_b(f.read(4))
    
    #endregion
    
    #region U64

    @classmethod
    def write_U64(cls, f:_io.BufferedWriter|_io.BytesIO, value:_num.U64|int, big:bool):
        return cls.write_U64_b(f, value) if big else cls.write_U64_l(f, value)

    @staticmethod
    def write_U64_l(f:_io.BufferedWriter|_io.BytesIO, value:_num.U64|int):
        f.write(_num.Pickle.pickle_U64_l(value))

    @staticmethod
    def write_U64_b(f:_io.BufferedWriter|_io.BytesIO, value:_num.U64|int):
        f.write(_num.Pickle.pickle_U64_b(value))
    
    @classmethod
    def read_U64(cls, f:_io.BufferedReader|_io.BytesIO, big:bool):
        return cls.read_U64_b(f) if big else cls.read_U64_l(f)
    
    @staticmethod
    def read_U64_l(f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_U64_l(f.read(8))
    
    @staticmethod
    def read_U64_b(f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_U64_b(f.read(8))
    
    #endregion
    
    #region I64

    @classmethod
    def write_I64(cls, f:_io.BufferedWriter|_io.BytesIO, value:_num.I64|int, big:bool):
        return cls.write_I64_b(f, value) if big else cls.write_I64_l(f, value)

    @staticmethod
    def write_I64_l(f:_io.BufferedWriter|_io.BytesIO, value:_num.I64|int):
        f.write(_num.Pickle.pickle_I64_l(value))

    @staticmethod
    def write_I64_b(f:_io.BufferedWriter|_io.BytesIO, value:_num.I64|int):
        f.write(_num.Pickle.pickle_I64_b(value))
    
    @classmethod
    def read_I64(cls, f:_io.BufferedReader|_io.BytesIO, big:bool):
        return cls.read_I64_b(f) if big else cls.read_I64_l(f)
    
    @staticmethod
    def read_I64_l(f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_I64_l(f.read(8))
    
    @staticmethod
    def read_I64_b(f:_io.BufferedReader|_io.BytesIO):
        return _num.Pickle.unpickle_I64_b(f.read(8))
    
    #endregion
    
    #region single

    @classmethod
    def write_single(cls, f:_io.BufferedWriter|_io.BytesIO, value:float, big:bool):
        return cls.write_single_b(f, value) if big else cls.write_single_l(f, value)

    @staticmethod
    def write_single_l(f:_io.BufferedWriter|_io.BytesIO, value:float):
        f.write(_num.Pickle.pickle_single_l(value))

    @staticmethod
    def write_single_b(f:_io.BufferedWriter|_io.BytesIO, value:float):
        f.write(_num.Pickle.pickle_single_b(value))
    
    @classmethod
    def read_single(cls, f:_io.BufferedReader|_io.BytesIO, big:bool):
        return cls.read_single_b(f) if big else cls.read_single_l(f)
    
    @staticmethod
    def read_single_l(f:_io.BufferedReader|_io.BytesIO) -> float:
        return _num.Pickle.unpickle_single_l(f.read(4))
    
    @staticmethod
    def read_single_b(f:_io.BufferedReader|_io.BytesIO) -> float:
        return _num.Pickle.unpickle_single_b(f.read(4))
    
    #endregion

    #region double

    @classmethod
    def write_double(cls, f:_io.BufferedWriter|_io.BytesIO, value:float, big:bool):
        return cls.write_double_b(f, value) if big else cls.write_double_l(f, value)

    @staticmethod
    def write_double_l(f:_io.BufferedWriter|_io.BytesIO, value:float):
        f.write(_num.Pickle.pickle_double_l(value))

    @staticmethod
    def write_double_b(f:_io.BufferedWriter|_io.BytesIO, value:float):
        f.write(_num.Pickle.pickle_double_b(value))
    
    @classmethod
    def read_double(cls, f:_io.BufferedReader|_io.BytesIO, big:bool):
        return cls.read_double_b(f) if big else cls.read_double_l(f)
    
    @staticmethod
    def read_double_l(f:_io.BufferedReader|_io.BytesIO) -> float:
        return _num.Pickle.unpickle_double_l(f.read(8))
    
    @staticmethod
    def read_double_b(f:_io.BufferedReader|_io.BytesIO) -> float:
        return _num.Pickle.unpickle_double_b(f.read(8))
    
    #endregion

    #region prim

    PRIM_L = _Prim(\
        write_U16_l, read_U16_l, write_I16_l, read_I16_l,\
        write_U32_l, read_U32_l, write_I32_l, read_I32_l,\
        write_U64_l, read_U64_l, write_I64_l, read_I64_l,\
        write_single_l, read_single_l, write_double_l, read_double_l)

    PRIM_B = _Prim(\
        write_U16_b, read_U16_b, write_I16_b, read_I16_b,\
        write_U32_b, read_U32_b, write_I32_b, read_I32_b,\
        write_U64_b, read_U64_b, write_I64_b, read_I64_b,\
        write_single_b, read_single_b, write_double_b, read_double_b)

    #endregion