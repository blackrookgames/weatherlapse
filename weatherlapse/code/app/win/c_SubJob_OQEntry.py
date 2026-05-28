from io import\
    BytesIO as _BytesIO,\
    StringIO as _StringIO

import code.engine.data as _data
import code.engine.num as _num

from .c_SubJobState import SubJobState as _SubJobState

def _write_str(f:_BytesIO, s:str):
    f.write(_num.Pickle.pickle_I32_l((-1) if (s is None) else len(s)))
    for c in s: f.write(_num.Pickle.pickle_I16_l(ord(c)))

def _read_str(f:_BytesIO):
    with _StringIO() as s:
        length = _num.Pickle.unpickle_I32_l(f.read(4))
        for _ in range(length):
            c = chr(_num.Pickle.unpickle_I16_l(f.read(2)))
            s.write(c)
        return s.getvalue()

class _OQEntryData(_data.Picklable):
    @property
    def state(self) -> _SubJobState: raise NotImplementedError("state has not been implemented")
    
class _OQEntryData_Init(_OQEntryData):
    def pickle(self): return b""
    @classmethod
    def unpickle(cls, data:bytes): return cls()
    @property
    def state(self): return _SubJobState.INIT

class _OQEntryData_Running(_OQEntryData):
    def __init__(self, main_desc:str, main_prog:float, sub_desc:str, sub_prog:float):
        self.__main_desc:str = main_desc
        self.__main_prog:float = main_prog
        self.__sub_desc:str = sub_desc
        self.__sub_prog:float = sub_prog
    def pickle(self):
        f = _BytesIO()
        _write_str(f, self.__main_desc)
        f.write(_num.Pickle.pickle_single_l(self.__main_prog))
        _write_str(f, self.__sub_desc)
        f.write(_num.Pickle.pickle_single_l(self.__sub_prog))
        return f.getvalue()
    @classmethod
    def unpickle(cls, data:bytes):
        f = _BytesIO(data)
        main_desc = _read_str(f)
        if main_desc is None: main_desc = ""
        main_prog = _num.Pickle.unpickle_single_l(f.read(4))
        sub_desc = _read_str(f)
        if sub_desc is None: sub_desc = ""
        sub_prog = _num.Pickle.unpickle_single_l(f.read(4))
        return cls(main_desc, main_prog, sub_desc, sub_prog)
    @property
    def state(self): return _SubJobState.RUNNING
    @property
    def main_desc(self): return self.__main_desc
    @property
    def main_prog(self): return self.__main_prog
    @property
    def sub_desc(self): return self.__sub_desc
    @property
    def sub_prog(self): return self.__sub_prog

class _OQEntryData_Finished(_OQEntryData):
    def __init__(self, data:bytes):
        self.__data = data
    def pickle(self): return self.__data
    @classmethod
    def unpickle(cls, data:bytes): return cls(data)
    @property
    def state(self): return _SubJobState.FINISHED
    @property
    def data(self): return self.__data

class _OQEntryData_Cancelled(_OQEntryData):
    def pickle(self): return b""
    @classmethod
    def unpickle(cls, data:bytes): return cls()
    @property
    def state(self): return _SubJobState.CANCELLED

class _OQEntryData_Error(_OQEntryData):
    def __init__(self, message:str):
        self.__message = message
    def pickle(self):
        f = _BytesIO()
        _write_str(f, self.__message)
        return f.getvalue()
    @classmethod
    def unpickle(cls, data:bytes):
        f = _BytesIO(data)
        return cls(_read_str(f))
    @property
    def state(self): return _SubJobState.ERROR
    @property
    def message(self): return self.__message

class _OQEntry(_data.Picklable):

    #region init
    
    def __init__(self, data:_OQEntryData):
        self.__state = data.state
        self.__data = data
         
    #endregion

    #region pickle

    def pickle(self):
        return _num.Pickle.pickle_U8(self.__state.value) + self.__data.pickle()
    
    @classmethod
    def unpickle(cls, data:bytes):
        state = _SubJobState(_num.Pickle.unpickle_U8(data))
        data = data[1:]
        match state:
            case _SubJobState.INIT: return cls(_OQEntryData_Init.unpickle(data))
            case _SubJobState.RUNNING: return cls(_OQEntryData_Running.unpickle(data))
            case _SubJobState.FINISHED: return cls(_OQEntryData_Finished.unpickle(data))
            case _SubJobState.CANCELLED: return cls(_OQEntryData_Cancelled.unpickle(data))
            case _SubJobState.ERROR: return cls(_OQEntryData_Error.unpickle(data))
        return cls(_OQEntryData_Init.unpickle(data))
         
    #endregion

    #region properties

    @property
    def state(self): return self.__state

    @property
    def data(self): return self.__data

    #endregion