from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

class widgetWrapper(ABC):
    def __init__(self, tag_name, context, widget):
        self.tag_name = tag_name
        self.context = context
        self.widget = widget # actual widget object

    @abstractmethod
    def to_xml(self):
        pass
    
    @abstractmethod
    def from_xml(self, xml):
        pass

    @abstractmethod
    def get_Value(self):
        pass

    @abstractmethod
    def get_context(self):
        pass