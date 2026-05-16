__all__ = [ 'XmlSavable' ]

import xml.etree.ElementTree as _ET

import engine.help as _help

class XmlSavable:
    """ Represents an object that can save to an XML element """

    #region abstract methods

    def _save_to_xml(self, element:_ET.Element) -> None:
        raise NotImplementedError("save_to_xml has not been implemented")
    
    #endregion

    #region methods

    def save_to_xml(self, element:_ET.Element) -> None:
        """
        Saves to an XML element

        :param element: Element to save to
        """
        self._save_to_xml(element)
    
    def save_to_xml_file(self, path:str) -> None:
        """
        Saves to an XML file

        :param path: File path
        :raise UnexpectedError: An unexpected error occurred while saving
        """
        def save(root:_ET.Element):
            nonlocal path
            try:
                tree = _ET.ElementTree(root)
                tree.write(path, encoding="utf-8", xml_declaration=True)
                return
            except Exception as _e: e = _help.UnexpectedError(_e)
            raise e
        root = _ET.Element("")
        self.save_to_xml(root)
        save(root)
    
    #endregion