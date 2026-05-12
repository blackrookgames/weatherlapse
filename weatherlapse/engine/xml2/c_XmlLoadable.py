__all__ = [ 'XmlLoadable' ]

import xml.etree.ElementTree as _ET

from io import StringIO as _StringIO
from typing import Callable as _Callable, TypeVar as _TypeVar

T = _TypeVar('T')

import help as _help
import num as _num

from .c_XmlElementError import XmlElementError as _XmlElementError

class XmlLoadable:
    """ Represents an object that can load from an XML element """

    #region private methods

    @classmethod
    def __fullpath(cls, root:_ET.Element, element:_ET.Element):
        plist:list[str] = []
        def find(parent:_ET.Element, index:int = -1):
            nonlocal element, plist
            # Add tag
            plist.append(f"{parent.tag}{(f"[{index}]" if (index >= 0) else "")}")
            # Loop thru children
            for _i in range(len(parent)):
                _child = parent[_i]
                # Is this it?
                if _child is element:
                    # Add child tag
                    plist.append(_child.tag)
                    # Found it!!!
                    return True
                # No! Check child's children.
                _plist_len = len(plist)
                if find(_child, index = _i): return True
                # Child couldn't find it either. Now remove what child added.
                while len(plist) > _plist_len: plist.pop()
            # Could not find element.
            return False
        # Search for element
        if not find(root): return None
        # Create path
        with _StringIO() as _s:
            for i in range(len(plist)):
                if i > 0: _s.write("/")
                _s.write(plist[i])
            return _s.getvalue()

    @classmethod
    def __finalerror(cls, root:_ET.Element, error:_XmlElementError):
        if error.element is None: return error
        path = cls.__fullpath(root, error.element)
        if path is None: return error
        if error.attribute is None: return _XmlElementError(message = f"{error.message} {path}")
        return _XmlElementError(message = f"{error.message} {path}@{error.attribute}")
    
    @classmethod
    def __parse(cls, element:_ET.Element, s:str|None, parse:_Callable[[str], _num.ParseResult[T]]):
        result = parse("" if (s is None) else s)
        if not result: raise _XmlElementError(element = element, message = str(result.error))
        return result.value
    
    @classmethod
    def __parse_multi(cls, element:_ET.Element, s:str|None, parse:_Callable[[str], _num.ParseResult[T]]):
        values:list[T] = []
        for _arg in _help.StrUtil.to_argv("" if (s is None) else s):
            result = parse(_arg)
            if not result: raise _XmlElementError(element = element, message = str(result.error))
            values.append(result.value)
        return values
    
    #endregion
    
    #region protected methods

    @classmethod
    def _wrapper(cls, reset:_Callable[[], None], load:_Callable[[], None]):
        """
        This can be used in implementations of _load_from_xml.
        1) reset is called first
        2) Followed by load
        3) If load raises an XmlElementError, reset is called again to ensure the reset object remains in a valid state

        :param reset: Reset function
        :param load: Load function
        :raise XmlElementError: An XML error was raised by load (see top)
        """
        reset()
        try:
            load()
        except _XmlElementError:
            reset()
            raise
        return

    @classmethod
    def _get_element(cls, parent:_ET.Element, child_tag:str):
        """
        Retrieves the first child element with the specified tag.

        :param parent: Parent element
        :param child_tag: Tag of child element
        :return: Retrieved child element
        :raise XmlElementError: throw is True and parent element does not contain a child element with the specified tag.
        """
        for _child in parent:
            if _child.tag != child_tag: continue
            return _child
        raise _XmlElementError(parent, f"{child_tag} element is missing.")

    @classmethod
    def _find_element(cls, parent:_ET.Element, child_tag:str):
        """
        Searches for a child element with the specified tag.

        :param parent: Parent element
        :param child_tag: Tag of child element
        :return: Found child element (or None if element could not be found)
        """
        for _child in parent:
            if _child.tag != child_tag: continue
            return _child
        return None

    @classmethod
    def _parse_text(cls, element:_ET.Element, parse:_Callable[[str], _num.ParseResult[T]]):
        """
        Parses an element's text

        :param element: Element
        :param parse: Function for parsing
        :return: Parsed value
        :raise XmlElementError: Failed to parse element text
        """
        return cls.__parse(element, element.text, parse)
    
    @classmethod
    def _parse_text_multi(cls, element:_ET.Element, parse:_Callable[[str], _num.ParseResult[T]]):
        """
        Parses space-separated items in an element's text

        :param element: Element
        :param parse: Function for parsing
        :return: Parsed value
        :raise XmlElementError: Failed to parse element text
        """
        return cls.__parse_multi(element, element.text, parse)

    #endregion

    #region abstract methods

    def _load_from_xml(self, element:_ET.Element) -> None:
        """
        :raise XmlElementError: Element contains invalid data
        """
        raise NotImplementedError("load_from_xml has not been implemented")
    
    #endregion

    #region methods

    def load_from_xml(self, element:_ET.Element) -> None:
        """
        Loads from an XML element

        :param element: Element to load from
        :raise XmlElementError: Element contains invalid data
        """
        try: return self._load_from_xml(element)
        except _XmlElementError as _e: e = _e
        raise self.__finalerror(element, e)

    def load_from_xml_file(self, path:str):
        """
        Loads from an XML file

        :param path: File path
        :raise ParseError: Failed to parse as XML
        :raise BadDataError: XML contains invalid data
        :raise UnexpectedError: An unexpected error occurred while loading
        """
        def load():
            nonlocal path
            try:
                tree = _ET.parse(path)
                return tree.getroot()
            except _ET.ParseError as _e: e = _e
            except Exception as _e: e = _help.UnexpectedError(_e)
            raise e
        self.load_from_xml(load())
    
    #endregion