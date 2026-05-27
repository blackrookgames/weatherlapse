from .c_Info import *

from pathlib import\
    Path as _Path

from code.engine.help import\
    BadOpError as _BadOpError

_info:None|Info = None

def raise_if_init():
    """
    Raises a BadOpError if the application information has already been initialized

    :raise BadOpError: Application information has already been initialized
    """
    global _info
    if _info is None: return
    raise _BadOpError("Application information has already been initialized.")

def raise_if_notinit():
    """
    Raises a BadOpError if the application information has not been initialized

    :raise BadOpError: Application information has not been initialized
    """
    global _info
    if _info is not None: return
    raise _BadOpError("Application information has not been initialized.")

def init(appdir:_Path, iswindows:bool):
    """
    Initializes application information

    :param appdir: Application directory
    :param iswindows: Whether or not application is running on Windows

    :raise BadOpError: Application information has already been initialized
    """
    global _info
    raise_if_init()
    _info = Info(appdir, iswindows)

def init_from_pickle(data:bytes):
    """
    Initializes application information using pickled data

    :param data: Pickled data

    :raise BadOpError: Application information has already been initialized
    """
    global _info
    raise_if_init()
    _info = Info.unpickle(data)

def get_info():
    """
    Retrieve information about the application

    :return: App information (or None if application information has not been initialized)
    """
    global _info
    return _info

def get_info_if_init():
    """
    Retrieve information about the application. 
    If the application information has not been initialized a BadOpError is raised.

    :return: App information
    :raise BadOpError: Application information has not been initialized
    """
    global _info
    raise_if_notinit()
    assert _info is not None
    return _info