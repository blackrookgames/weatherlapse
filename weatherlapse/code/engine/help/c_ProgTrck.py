__all__ = ['ProgTrck']

class ProgTrck:
    """ Represents a progress tracker """

    #region init

    def __init__(self):
        """ Initializer for ProgTrck """
        self.__maxx:int = 0
        self.__value:int = 0

    #endregion

    #region properties

    @property
    def maxx(self):
        """ Max value """
        return self.__maxx
    @maxx.setter
    def maxx(self, maxx:int):
        self.__maxx = maxx
    
    @property
    def value(self):
        """ Progress value """
        return self.__value
    @value.setter
    def value(self, value:int):
        self.__value = value
    
    #endregion

    #region methods

    def percent(self):
        """
        Computes the percentage value

        :return: Percentage value
        """
        if self.__maxx <= 0: return 0.0
        return 100.0 * (self.__value / self.__maxx)

    #endregion
