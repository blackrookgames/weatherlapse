__all__ = ['Pickle']

import struct as _struct

from .c_PickleError import PickleError as _PickleError

from .c_U8 import U8 as _U8, U8_MIN as _U8_MIN, U8_MAX as _U8_MAX
from .c_I8 import I8 as _I8, I8_MIN as _I8_MIN, I8_MAX as _I8_MAX, I8_SIZE as _I8_SIZE
from .c_U16 import U16 as _U16, U16_MIN as _U16_MIN, U16_MAX as _U16_MAX, U16_SIZE as _U16_SIZE
from .c_I16 import I16 as _I16, I16_MIN as _I16_MIN, I16_MAX as _I16_MAX, I16_SIZE as _I16_SIZE
from .c_U32 import U32 as _U32, U32_MIN as _U32_MIN, U32_MAX as _U32_MAX, U32_SIZE as _U32_SIZE
from .c_I32 import I32 as _I32, I32_MIN as _I32_MIN, I32_MAX as _I32_MAX, I32_SIZE as _I32_SIZE
from .c_U64 import U64 as _U64, U64_MIN as _U64_MIN, U64_MAX as _U64_MAX, U64_SIZE as _U64_SIZE
from .c_I64 import I64 as _I64, I64_MIN as _I64_MIN, I64_MAX as _I64_MAX, I64_SIZE as _I64_SIZE

class Pickle:
    """ Utility for pickling/unpickling data """

    #region U8

    __U8_MIN = int(_U8_MIN)
    __U8_MAX = int(_U8_MAX)

    @classmethod
    def pickle_U8(cls, value:_U8|int):
        """
        Pickles an 8-bit unsigned integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _U8): return bytes([value, ])
        return bytes([ max(cls.__U8_MIN, min(cls.__U8_MAX, value)), ])
    
    @classmethod
    def unpickle_U8(cls, data:bytes):
        """
        Unpickles an 8-bit unsigned integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data is empty
        """
        if len(data) == 0: raise _PickleError("Data cannot be empty.")
        return _U8(data[0])

    #endregion

    #region I8

    __I8_MIN = int(_I8_MIN)
    __I8_MAX = int(_I8_MAX)
    __I8_NUMVALS = 1 << (_I8_SIZE * 8)

    @classmethod
    def pickle_I8(cls, value:_I8|int):
        """
        Pickles an 8-bit signed integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _I8): value = int(value)
        else: value = max(cls.__I8_MIN, min(cls.__I8_MAX, value))
        return bytes([value if (value >= 0) else (value + cls.__I8_NUMVALS), ])
    
    @classmethod
    def unpickle_I8(cls, data:bytes):
        """
        Unpickles an 8-bit signed integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data is empty
        """
        if len(data) == 0: raise _PickleError("Data cannot be empty.")
        value = data[0]
        return _I8(value if (value < -cls.__I8_MIN) else (value - cls.__I8_NUMVALS))

    #endregion

    #region U16

    @classmethod
    def pickle_U16(cls, value:_U16|int, big:bool):
        """
        Pickles a 16-bit unsigned integer

        :param value: Value to pickle
        :param big: Whether or not to use big-endian
        :return: Pickled data
        """
        return cls.pickle_U16_b(value) if big else cls.pickle_U16_l(value)

    @classmethod
    def pickle_U16_l(cls, value:_U16|int):
        """
        Pickles a little-endian 16-bit unsigned integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _U16): return _struct.pack('<H', value)
        return _struct.pack('<H', max(_U16_MIN, min(_U16_MAX, value)))

    @classmethod
    def pickle_U16_b(cls, value:_U16|int):
        """
        Pickles a big-endian 16-bit unsigned integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _U16): return _struct.pack('>H', value)
        return _struct.pack('>H', max(_U16_MIN, min(_U16_MAX, value)))
    
    @classmethod
    def unpickle_U16(cls, data:bytes, big:bool):
        """
        Unpickles a 16-bit unsigned integer

        :param data: Pickled data
        :param big: Whether or not to use big-endian
        :return: Unpickled value
        :raise PickleError: Data length is less than 2
        """
        return cls.unpickle_U16_b(data) if big else cls.unpickle_U16_l(data)
    
    @classmethod
    def unpickle_U16_l(cls, data:bytes):
        """
        Unpickles a little-endian 16-bit unsigned integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 2
        """
        if len(data) >= _U16_SIZE: return _U16(_struct.unpack('<H', data)[0])
        raise _PickleError(f"Data length must be greater than or equal to {_U16_SIZE}.")
    
    @classmethod
    def unpickle_U16_b(cls, data:bytes):
        """
        Unpickles a big-endian 16-bit unsigned integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 2
        """
        if len(data) >= _U16_SIZE: return _U16(_struct.unpack('>H', data)[0])
        raise _PickleError(f"Data length must be greater than or equal to {_U16_SIZE}.")
    
    #endregion
    
    #region I16

    @classmethod
    def pickle_I16(cls, value:_I16|int, big:bool):
        """
        Pickles a 16-bit signed integer

        :param value: Value to pickle
        :param big: Whether or not to use big-endian
        :return: Pickled data
        """
        return cls.pickle_I16_b(value) if big else cls.pickle_I16_l(value)

    @classmethod
    def pickle_I16_l(cls, value:_I16|int):
        """
        Pickles a little-endian 16-bit signed integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _I16): return _struct.pack('<h', value)
        return _struct.pack('<h', max(_I16_MIN, min(_I16_MAX, value)))

    @classmethod
    def pickle_I16_b(cls, value:_I16|int):
        """
        Pickles a big-endian 16-bit signed integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _I16): return _struct.pack('>h', value)
        return _struct.pack('>h', max(_I16_MIN, min(_I16_MAX, value)))
    
    @classmethod
    def unpickle_I16(cls, data:bytes, big:bool):
        """
        Unpickles a 16-bit signed integer

        :param data: Pickled data
        :param big: Whether or not to use big-endian
        :return: Unpickled value
        :raise PickleError: Data length is less than 2
        """
        return cls.unpickle_I16_b(data) if big else cls.unpickle_I16_l(data)
    
    @classmethod
    def unpickle_I16_l(cls, data:bytes):
        """
        Unpickles a little-endian 16-bit signed integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 2
        """
        if len(data) >= _I16_SIZE: return _I16(_struct.unpack('<h', data)[0])
        raise _PickleError(f"Data length must be greater than or equal to {_I16_SIZE}.")
    
    @classmethod
    def unpickle_I16_b(cls, data:bytes):
        """
        Unpickles a big-endian 16-bit signed integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 2
        """
        if len(data) >= _I16_SIZE: return _I16(_struct.unpack('>h', data)[0])
        raise _PickleError(f"Data length must be greater than or equal to {_I16_SIZE}.")
    
    #endregion

    #region U32

    @classmethod
    def pickle_U32(cls, value:_U32|int, big:bool):
        """
        Pickles a 32-bit unsigned integer

        :param value: Value to pickle
        :param big: Whether or not to use big-endian
        :return: Pickled data
        """
        return cls.pickle_U32_b(value) if big else cls.pickle_U32_l(value)

    @classmethod
    def pickle_U32_l(cls, value:_U32|int):
        """
        Pickles a little-endian 32-bit unsigned integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _U32): return _struct.pack('<I', value)
        return _struct.pack('<I', max(_U32_MIN, min(_U32_MAX, value)))

    @classmethod
    def pickle_U32_b(cls, value:_U32|int):
        """
        Pickles a big-endian 32-bit unsigned integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _U32): return _struct.pack('>I', value)
        return _struct.pack('>I', max(_U32_MIN, min(_U32_MAX, value)))
    
    @classmethod
    def unpickle_U32(cls, data:bytes, big:bool):
        """
        Unpickles a 32-bit unsigned integer

        :param data: Pickled data
        :param big: Whether or not to use big-endian
        :return: Unpickled value
        :raise PickleError: Data length is less than 4
        """
        return cls.unpickle_U32_b(data) if big else cls.unpickle_U32_l(data)
    
    @classmethod
    def unpickle_U32_l(cls, data:bytes):
        """
        Unpickles a little-endian 32-bit unsigned integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 4
        """
        if len(data) >= _U32_SIZE: return _U32(_struct.unpack('<I', data)[0])
        raise _PickleError(f"Data length must be greater than or equal to {_U32_SIZE}.")
    
    @classmethod
    def unpickle_U32_b(cls, data:bytes):
        """
        Unpickles a big-endian 32-bit unsigned integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 4
        """
        if len(data) >= _U32_SIZE: return _U32(_struct.unpack('>I', data)[0])
        raise _PickleError(f"Data length must be greater than or equal to {_U32_SIZE}.")
    
    #endregion
    
    #region I32

    @classmethod
    def pickle_I32(cls, value:_I32|int, big:bool):
        """
        Pickles a 32-bit signed integer

        :param value: Value to pickle
        :param big: Whether or not to use big-endian
        :return: Pickled data
        """
        return cls.pickle_I32_b(value) if big else cls.pickle_I32_l(value)

    @classmethod
    def pickle_I32_l(cls, value:_I32|int):
        """
        Pickles a little-endian 32-bit signed integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _I32): return _struct.pack('<i', value)
        return _struct.pack('<i', max(_I32_MIN, min(_I32_MAX, value)))

    @classmethod
    def pickle_I32_b(cls, value:_I32|int):
        """
        Pickles a big-endian 32-bit signed integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _I32): return _struct.pack('>i', value)
        return _struct.pack('>i', max(_I32_MIN, min(_I32_MAX, value)))
    
    @classmethod
    def unpickle_I32(cls, data:bytes, big:bool):
        """
        Unpickles a 32-bit signed integer

        :param data: Pickled data
        :param big: Whether or not to use big-endian
        :return: Unpickled value
        :raise PickleError: Data length is less than 4
        """
        return cls.unpickle_I32_b(data) if big else cls.unpickle_I32_l(data)
    
    @classmethod
    def unpickle_I32_l(cls, data:bytes):
        """
        Unpickles a little-endian 32-bit signed integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 4
        """
        if len(data) >= _I32_SIZE: return _I32(_struct.unpack('<i', data)[0])
        raise _PickleError(f"Data length must be greater than or equal to {_I32_SIZE}.")
    
    @classmethod
    def unpickle_I32_b(cls, data:bytes):
        """
        Unpickles a big-endian 32-bit signed integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 4
        """
        if len(data) >= _I32_SIZE: return _I32(_struct.unpack('>i', data)[0])
        raise _PickleError(f"Data length must be greater than or equal to {_I32_SIZE}.")
    
    #endregion
    
    #region U64

    @classmethod
    def pickle_U64(cls, value:_U64|int, big:bool):
        """
        Pickles a 64-bit unsigned integer

        :param value: Value to pickle
        :param big: Whether or not to use big-endian
        :return: Pickled data
        """
        return cls.pickle_U64_b(value) if big else cls.pickle_U64_l(value)

    @classmethod
    def pickle_U64_l(cls, value:_U64|int):
        """
        Pickles a little-endian 64-bit unsigned integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _U64): return _struct.pack('<Q', value)
        return _struct.pack('<Q', max(_U64_MIN, min(_U64_MAX, value)))

    @classmethod
    def pickle_U64_b(cls, value:_U64|int):
        """
        Pickles a big-endian 64-bit unsigned integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _U64): return _struct.pack('>Q', value)
        return _struct.pack('>Q', max(_U64_MIN, min(_U64_MAX, value)))
    
    @classmethod
    def unpickle_U64(cls, data:bytes, big:bool):
        """
        Unpickles a 64-bit unsigned integer

        :param data: Pickled data
        :param big: Whether or not to use big-endian
        :return: Unpickled value
        :raise PickleError: Data length is less than 8
        """
        return cls.unpickle_U64_b(data) if big else cls.unpickle_U64_l(data)
    
    @classmethod
    def unpickle_U64_l(cls, data:bytes):
        """
        Unpickles a little-endian 64-bit unsigned integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 8
        """
        if len(data) >= _U64_SIZE: return _U64(_struct.unpack('<Q', data)[0])
        raise _PickleError(f"Data length must be greater than or equal to {_U64_SIZE}.")
    
    @classmethod
    def unpickle_U64_b(cls, data:bytes):
        """
        Unpickles a big-endian 64-bit unsigned integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 8
        """
        if len(data) >= _U64_SIZE: return _U64(_struct.unpack('>Q', data)[0])
        raise _PickleError(f"Data length must be greater than or equal to {_U64_SIZE}.")
    
    #endregion
    
    #region I64

    @classmethod
    def pickle_I64(cls, value:_I64|int, big:bool):
        """
        Pickles a 64-bit signed integer

        :param value: Value to pickle
        :param big: Whether or not to use big-endian
        :return: Pickled data
        """
        return cls.pickle_I64_b(value) if big else cls.pickle_I64_l(value)

    @classmethod
    def pickle_I64_l(cls, value:_I64|int):
        """
        Pickles a little-endian 64-bit signed integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _I64): return _struct.pack('<q', value)
        return _struct.pack('<q', max(_I64_MIN, min(_I64_MAX, value)))

    @classmethod
    def pickle_I64_b(cls, value:_I64|int):
        """
        Pickles a big-endian 64-bit signed integer

        :param value: Value to pickle
        :return: Pickled data
        """
        if isinstance(value, _I64): return _struct.pack('>q', value)
        return _struct.pack('>q', max(_I64_MIN, min(_I64_MAX, value)))
    
    @classmethod
    def unpickle_I64(cls, data:bytes, big:bool):
        """
        Unpickles a 64-bit signed integer

        :param data: Pickled data
        :param big: Whether or not to use big-endian
        :return: Unpickled value
        :raise PickleError: Data length is less than 8
        """
        return cls.unpickle_I64_b(data) if big else cls.unpickle_I64_l(data)
    
    @classmethod
    def unpickle_I64_l(cls, data:bytes):
        """
        Unpickles a little-endian 64-bit signed integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 8
        """
        if len(data) >= _I64_SIZE: return _I64(_struct.unpack('<q', data)[0])
        raise _PickleError(f"Data length must be greater than or equal to {_I64_SIZE}.")
    
    @classmethod
    def unpickle_I64_b(cls, data:bytes):
        """
        Unpickles a big-endian 64-bit signed integer

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 8
        """
        if len(data) >= _I64_SIZE: return _I64(_struct.unpack('>q', data)[0])
        raise _PickleError(f"Data length must be greater than or equal to {_I64_SIZE}.")
    
    #endregion
    
    #region single

    @classmethod
    def pickle_single(cls, value:float, big:bool):
        """
        Pickles a single-precision floating-point value

        :param value: Value to pickle
        :param big: Whether or not to use big-endian
        :return: Pickled data
        """
        return cls.pickle_single_b(value) if big else cls.pickle_single_l(value)

    @classmethod
    def pickle_single_l(cls, value:float):
        """
        Pickles a little-endian single-precision floating-point value

        :param value: Value to pickle
        :return: Pickled data
        """
        return _struct.pack('<f', value)

    @classmethod
    def pickle_single_b(cls, value:float):
        """
        Pickles a big-endian single-precision floating-point value

        :param value: Value to pickle
        :return: Pickled data
        """
        return _struct.pack('>f', value)
    
    @classmethod
    def unpickle_single(cls, data:bytes, big:bool):
        """
        Unpickles a single-precision floating-point value

        :param data: Pickled data
        :param big: Whether or not to use big-endian
        :return: Unpickled value
        :raise PickleError: Data length is less than 4
        """
        return cls.unpickle_single_b(data) if big else cls.unpickle_single_l(data)
    
    @classmethod
    def unpickle_single_l(cls, data:bytes) -> float:
        """
        Unpickles a little-endian single-precision floating-point value

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 4
        """
        if len(data) >= 4: return _struct.unpack('<f', data)[0]
        raise _PickleError("Data length must be greater than or equal to 4.")
    
    @classmethod
    def unpickle_single_b(cls, data:bytes) -> float:
        """
        Unpickles a big-endian single-precision floating-point value

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 4
        """
        if len(data) >= 4: return _struct.unpack('>f', data)[0]
        raise _PickleError("Data length must be greater than or equal to 4.")
    
    #endregion

    #region double

    @classmethod
    def pickle_double(cls, value:float, big:bool):
        """
        Pickles a double-precision floating-point value

        :param value: Value to pickle
        :param big: Whether or not to use big-endian
        :return: Pickled data
        """
        return cls.pickle_double_b(value) if big else cls.pickle_double_l(value)

    @classmethod
    def pickle_double_l(cls, value:float):
        """
        Pickles a little-endian double-precision floating-point value

        :param value: Value to pickle
        :return: Pickled data
        """
        return _struct.pack('<d', value)

    @classmethod
    def pickle_double_b(cls, value:float):
        """
        Pickles a big-endian double-precision floating-point value

        :param value: Value to pickle
        :return: Pickled data
        """
        return _struct.pack('>d', value)
    
    @classmethod
    def unpickle_double(cls, data:bytes, big:bool):
        """
        Unpickles a double-precision floating-point value

        :param data: Pickled data
        :param big: Whether or not to use big-endian
        :return: Unpickled value
        :raise PickleError: Data length is less than 8
        """
        return cls.unpickle_double_b(data) if big else cls.unpickle_double_l(data)
    
    @classmethod
    def unpickle_double_l(cls, data:bytes) -> float:
        """
        Unpickles a little-endian double-precision floating-point value

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 8
        """
        if len(data) >= 8: return _struct.unpack('<d', data)[0]
        raise _PickleError("Data length must be greater than or equal to 8.")
    
    @classmethod
    def unpickle_double_b(cls, data:bytes) -> float:
        """
        Unpickles a big-endian double-precision floating-point value

        :param data: Pickled data
        :return: Unpickled value
        :raise PickleError: Data length is less than 8
        """
        if len(data) >= 8: return _struct.unpack('>d', data)[0]
        raise _PickleError("Data length must be greater than or equal to 8.")
    
    #endregion