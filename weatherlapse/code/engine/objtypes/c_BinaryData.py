__all__ = ['BinaryData']

import io as _io
import struct as _struct

import code.engine.data as _data

class BinaryData(_data.DataLoadable, _data.DataSavable):
    """ Represents binary data grouped by name """

    #region init

    def __init__(self):
        """ Initializer for BinaryData """
        self.__entries:dict[str, bytes] = {}

    #endregion

    #region load/save

    def _load(self, reader:_io.BufferedReader|_io.BytesIO):
        self.__entries.clear()
        count = _struct.unpack('<i', reader.read(4))[0]
        for _i in range(count):
            _offset_name = _struct.unpack('<i', reader.read(4))[0]
            _offset_data = _struct.unpack('<i', reader.read(4))[0]
            _return = reader.tell()
            # Name
            reader.seek(_offset_name)
            _name_len = _struct.unpack('<i', reader.read(4))[0]
            with _io.StringIO() as _name_io:
                for _ in range(_name_len):
                    _name_io.write(chr(_struct.unpack('<h', reader.read(2))[0]))
                _name = _name_io.getvalue()
            # Data
            reader.seek(_offset_data)
            _data_len = _struct.unpack('<i', reader.read(4))[0]
            _data = reader.read(_data_len)
            # Add
            self.__entries[_name] = _data
            # Next
            reader.seek(_return)

    def _save(self, writer:_io.BufferedWriter|_io.BytesIO):
        """
        Saves to a file

        :param path: File path
        :raise UnexpectedError: An unexpected error occurred while saving
        """
        # Header (placeholder)
        writer.write(_struct.pack('<i', len(self.__entries)))
        headpos = writer.tell()
        for _ in range(len(self.__entries)):
            writer.write(_struct.pack('<i', 0))
            writer.write(_struct.pack('<i', 0))
        # Groups
        for _name, _data in self.__entries.items():
            # Name
            _offset_name = writer.tell()
            writer.write(_struct.pack('<i', len(_name)))
            for _char in _name: writer.write(_struct.pack('<h', ord(_char)))
            self._pad(writer)
            # Data
            _offset_data = writer.tell()
            writer.write(_struct.pack('<i', len(_data)))
            writer.write(_data)
            self._pad(writer)
            # Offsets
            _return = writer.tell()
            writer.seek(headpos)
            writer.write(_struct.pack('<i', _offset_name))
            writer.write(_struct.pack('<i', _offset_data))
            headpos = writer.tell()
            writer.seek(_return)

    #endregion

    #region operators

    def __len__(self):
        return len(self.__entries)
    
    def __iter__(self):
        """
        Iterates thru the groups

        :yield: Group name and data
        """
        for name, data in self.__entries.items():
            yield name, data

    def __getitem__(self, name:str):
        """
        Retrieves the data of the group of the specified name

        :param name: Group name
        :return: Group data
        :raises KeyError: Group could not be found
        """
        try:
            return self.__entries[name]
        except:
            if name in self.__entries: raise
        raise KeyError("Could not find a group of data under the specified name.")
    
    def __contains__(self, name:str):
        """
        Checks whether or not a group exists of the specified name

        :param name: Group name
        :return: Whether or not a group exists of the specified name
        """
        return name in self.__entries
    
    #endregion

    #region methods

    def add(self, name:str, data:bytes):
        """
        Creates a group with the specified name and containing the specified data

        :param name: Group name
        :param data: Group data
        :raises KeyError: There already exists a group of data under the specified name
        """
        if name in self.__entries:
            raise KeyError("There already exists a group of data under the specified name.")
        self.__entries[name] = data
    
    def remove(self, name:str):
        """
        Removes the group of the specified name and returns its data

        :param name: Group name
        :return: Group data
        :raises KeyError: Group could not be found
        """
        try: return self.__entries.pop(name)
        except: pass
        raise KeyError("Could not find a group of data under the specified name.")
    
    def clear(self):
        """
        Removes all groups
        """
        self.__entries.clear()

    #endregion