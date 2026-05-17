__all__ = ['SecHand']

import engine.num as _num

class SecHand:
    """ Represents the value of the second-hand of a clock """

    #region init

    def __init__(self, second:int, microsecond:int):
        """
        Initializer for SecHand

        :param second:
            Second value
        :param microsecond:
            Microsecond value
        :raises ValueError: 
            Second value is out of range\n
            or\n
            Microsecond value is out of range
        """
        if second < 0 or second >= 60:
            raise ValueError("Second value is out of range.")
        if microsecond < 0 or microsecond >= self.__MILLION:
            raise ValueError("Microsecond value is out of range.")
        self.__second = second
        self.__microsecond = microsecond

    #endregion

    #region operators

    def __str__(self): return str(self.to_float())
    
    def __eq__(self, other): return self.__eq(other)
    def __ne__(self, other): return not self.__eq(other)
    def __hash__(self): return hash(self.__second)

    #endregion

    #region const
    
    __MILLION = 1000000

    #endregion

    #region properties

    @property
    def second(self):
        """ Second value """
        return self.__second

    @property
    def microsecond(self):
        """ Microsecond value """
        return self.__microsecond

    #endregion

    #region helper methods

    def __eq(self, other):
        if not isinstance(other, SecHand): return False
        return self.__second == other.__second and self.__microsecond == other.__microsecond

    #endregion

    #region methods

    @classmethod
    def from_float(cls, input:float):
        """
        Converts a floating-point value to a SecHand value

        :param input: Input floating-point value
        :return: Converted value
        :raises ValueError: Second value is out of range
        """
        micros = round(input * cls.__MILLION)
        return cls(micros // cls.__MILLION, micros % cls.__MILLION)
    
    def to_float(self):
        """
        Converts a SecHand value to a floating-point value

        :return: Converted value
        """
        return self.__second + self.__microsecond / self.__MILLION
    
    @classmethod
    def tryparse(cls, s:str):
        """
        Attempts to parse a string to a SecHand value

        :param s: String to parse
        :return: Parse result
        """
        DEFAULT = cls(0, 0)
        # Parse float
        result = _num.Parse.try_float(s)
        if not result.success: return _num.ParseResult(DEFAULT, result.error)
        # Parse second
        try: return _num.ParseResult(cls.from_float(result.value), None)
        except Exception as _ex: return _num.ParseResult(DEFAULT, _num.ParseError(_ex))

    #endregion