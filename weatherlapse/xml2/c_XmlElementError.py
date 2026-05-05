__all__ = [ 'XmlElementError' ]

import xml.etree.ElementTree as _ET

class XmlElementError(Exception):
    """ Raised when an invalid XML element is found """

    #region init

    def __init__(self, element:None|_ET.Element = None, attribute:None|str = None, message:None|str = None):
        """
        Initializer for XmlElementError

        :param element: XML element that is invalid
        :param attribute: Name of attribute that is invalid
        :param message: Error message
        """
        self.__element = element
        self.__attribute = attribute
        self.__message = message

    #endregion

    #region operators

    def __str__(self):
        # Get message text
        message = "XML element is invalid." if (self.__message is None) else self.__message
        # Create string
        if self.__element is not None:
            if self.__attribute is not None:
                return f"{message} {self.__element.tag}@{self.__attribute}"
            return f"{message} {self.__element.tag}"
        if self.__attribute is not None:
            return f"{message} @{self.__attribute}"
        return message

    #endregion

    #region properties

    @property
    def element(self):
        """ XML element that is invalid """
        return self.__element

    @property
    def attribute(self):
        """ Name of attribute that is invalid """
        return self.__attribute
    
    @property
    def message(self):
        """ Error message """
        return self.__message

    #endregion