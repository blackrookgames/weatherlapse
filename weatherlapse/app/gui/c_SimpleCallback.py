__all__ = ['SimpleCallback']

from typing import\
    Callable as _Callable,\
    TypeVar as _TypeVar

T = _TypeVar('T')

type SimpleCallback[T] = _Callable[[T], None]