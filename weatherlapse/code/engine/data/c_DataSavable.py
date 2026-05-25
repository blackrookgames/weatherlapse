__all__ = [ 'DataSavable' ]

import io as _io

from pathlib import\
    Path as _Path

import code.engine.help as _help

class DataSavable:
    """ Represents an object with savable data """

    #region helper

    @classmethod
    def _pad(cls, writer:_io.BufferedWriter|_io.BytesIO):
        pos = writer.tell()
        rem = pos % 4
        if rem == 0: return
        writer.write(bytes(0 for _ in range(rem, 4)))
    
    #endregion

    #region abstract methods

    def _save(self, writer:_io.BufferedWriter|_io.BytesIO) -> None:
        """
        :raise Exception: An unexpected error occurred while saving
        """
        raise NotImplementedError("_save has not been implemented")
    
    #endregion

    #region methods

    def save(self, dest:str|_Path|_io.BytesIO):
        """
        Saves to a destination

        :param dest: Destination
        :raise UnexpectedError: An unexpected error occurred while saving
        """
        try:
            if isinstance(dest, _io.BytesIO):
                self._save(dest)
            else:
                with open(dest, 'wb') as f: self._save(f)
            return
        except Exception as _e: e = _help.UnexpectedError(_e)
        raise e
    
    #endregion