__all__ = [ 'DataLoadable' ]

import io as _io

from pathlib import\
    Path as _Path

import code.engine.help as _help

class DataLoadable:
    """ Represents an object with loadable data """

    #region abstract methods

    def _load(self, reader:_io.BufferedReader|_io.BytesIO) -> None:
        """
        :raise BadDataError: Invalid data is found
        :raise Exception: An unexpected error occurred while loading
        """
        raise NotImplementedError("_load has not been implemented")
    
    #endregion

    #region methods

    def load(self, source:str|_Path|_io.BytesIO):
        """
        Loads from a source

        :param source: Source
        :raise BadDataError: Invalid data is found
        :raise UnexpectedError: An unexpected error occurred while loading
        """
        try:
            if isinstance(source, _io.BytesIO):
                self._load(source)
            else:
                with open(source, 'rb') as f: self._load(f)
            return
        except _help.BadDataError as _e: e = _e
        except Exception as _e: e = _help.UnexpectedError(_e)
        raise e
    
    #endregion