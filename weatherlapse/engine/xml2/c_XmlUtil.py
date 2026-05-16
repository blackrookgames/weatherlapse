__all__ = [ 'XmlUtil' ]

import xml.etree.ElementTree as _ET

from io import StringIO as _StringIO
from typing import Callable as _Callable, TypeVar as _TypeVar

T = _TypeVar('T')

import engine.help as _help
import engine.num as _num

from .c_XmlElementError import XmlElementError as _XmlElementError

class XmlUtil:
    """ Represents an XML utility """
    
    #region parse_element_text, parse_element_multi

    #region helper
    
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

    @classmethod
    def parse_element_text(cls, element:_ET.Element, parse:_Callable[[str], _num.ParseResult[T]]):
        """
        Parses an element's text

        :param element: Element
        :param parse: Function for parsing
        :return: Parsed value
        :raise XmlElementError: Failed to parse element text
        """
        return cls.__parse(element, element.text, parse)
    
    @classmethod
    def parse_element_text_multi(cls, element:_ET.Element, parse:_Callable[[str], _num.ParseResult[T]]):
        """
        Parses space-separated items in an element's text

        :param element: Element
        :param parse: Function for parsing
        :return: Parsed value
        :raise XmlElementError: Failed to parse element text
        """
        return cls.__parse_multi(element, element.text, parse)

    #endregion
    
    #region get_element, find_element

    @classmethod
    def get_element(cls, parent:_ET.Element, child_tag:str):
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
    def find_element(cls, parent:_ET.Element, child_tag:str):
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

    #endregion
    
    #region create_element

    @classmethod
    def create_element(cls, tag:str = "", attrib: dict[str, str] = {}, text:None|str = None, tail:None|str = None):
        """
        Creates an XML element

        :param tag: Tag
        :param attrib: Attributes
        :param text: Text before first subelement
        :param tail: Text after end tag
        :return: Created element
        """
        element = _ET.Element(tag, attrib = attrib)
        element.text = text
        element.tail = tail
        return element

    #endregion
