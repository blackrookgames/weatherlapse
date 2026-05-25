__all__ = ['SplashImages']

from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk
from typing import\
    TYPE_CHECKING as _TYPE_CHECKING

from .c_SplashImage import\
    SplashImage as _SplashImage

if (_TYPE_CHECKING):
    from .c_Splash import Splash as _Splash

class SplashImages:
    """ Represents the displayed images in a splash visual """

    #region nested

    class _Entry:
        """ Also accessed by Splash """
        def __init__(self, source:_SplashImage):
            self.__source = source
            self.__image:None|_Image.Image = None
            self.__imagetk:None|_ImageTk.PhotoImage = None
            self.__canvasid:None|int = None
        @property
        def source(self): return self.__source
        @property
        def image(self): return self.__image
        @image.setter
        def image(self, value:None|_Image.Image): self.__image = value
        @property
        def imagetk(self): return self.__imagetk
        @imagetk.setter
        def imagetk(self, value:None|_ImageTk.PhotoImage): self.__imagetk = value
        @property
        def canvasid(self): return self.__canvasid
        @canvasid.setter
        def canvasid(self, value:None|int): self.__canvasid = value

    #endregion

    #region init

    def __init__(self, splash:'_Splash'):
        """
        WARNING: This is only to be called by Splash
        """
        self.__splash = splash
        self.__entries:list[SplashImages._Entry] = []

    #endregion

    #region operators

    def __len__(self):
        return len(self.__entries)
    
    def __iter__(self):
        for _entry in self.__entries:
            yield _entry.source

    def __getitem__(self, index:int):
        """
        Gets the image at the specified index

        :param index: Index of image
        :return: Image at the specified index
        :raises IndexError: Index is out of range
        """
        try:
            return self.__entries[index].source
        except:
            if index >= 0 and index < len(self.__entries): raise
        raise IndexError("Index is out of range.")

    #endregion

    #region properties

    @property
    def splash(self):
        """ Splash object """
        return self.__splash

    #endregion

    #region private methods

    def __index(self, image:_SplashImage):
        for _i in range(len(self.__entries)):
            if self.__entries[_i].source is not image:
                continue
            return _i
        return -1

    #endregion

    #region internal methods

    def _refresh_entries(self):
        """ Also accessed by Splash """
        self.__splash._image_refresh(self.__entries)

    #endregion

    #region methods

    def add(self, image:_SplashImage):
        """
        Adds a splash image

        :param image: Splash image to add
        """
        # Create entry
        entry = self._Entry(image)
        self.__entries.append(entry)
        # Add to canvas
        infront = None if len(self.__entries) == 1 else self.__entries[len(self.__entries) - 2].canvasid
        self.__splash._image_add(entry, infront)

    def insert(self, index:int, image:_SplashImage):
        """
        Inserts a splash image

        :param index: Insertion index
        :param image: Splash image to insert
        :raises IndexError: Index is out of range
        """
        if index < 0 or index > len(self.__entries):
            raise IndexError("Index is out of range.")
        # Create entry
        entry = self._Entry(image)
        self.__entries.insert(index, entry)
        # Add to canvas
        infront = None if index == 0 else self.__entries[index - 1].canvasid
        self.__splash._image_add(entry, infront)

    def remove(self, image:_SplashImage):
        """
        Attempts to remove the specified splash image

        :param image: Splash image to remove
        :return: Whether or not successful
        """
        # Find index
        index = self.__index(image)
        if index == -1: return False
        # Remove
        entry = self.__entries.pop(index)
        self.__splash._image_remove(entry)
        return True

    def removeat(self, index:int):
        """
        Removes the splash image at the specified index

        :param index: Index of image to remove
        :raises IndexError: Index is out of range
        """
        if index < 0 or index >= len(self.__entries):
            raise IndexError("Index is out of range.")
        entry = self.__entries.pop(index)
        self.__splash._image_remove(entry)

    def clear(self):
        """
        Removes all splash images
        """
        while len(self.__entries) > 0:
            entry = self.__entries.pop()
            self.__splash._image_remove(entry)

    #endregion