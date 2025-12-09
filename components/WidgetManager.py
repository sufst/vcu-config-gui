import xml.etree.ElementTree as ET
import re
from components.fileWriter import FileWriter

class widgetManager:
    def __init__(self):
        self.widgets = {}

    def add_widget(self, name, widget):
        self.widgets[name] = widget

    def to_xml(self):
        xml_content = "<Configs>\n"
        for widget in self.widgets.values():
           xml_content += f"   {widget.to_xml()}\n"
        # xwl_content += "</Configs>"

        return xml_content[0:(len(xml_content) - 1)]
    
    def from_xml(self, xml):
        root = ET.fromstring(xml)

        for element in root:
            name = element.tag
            if name in self.widgets:
                print(f"Loading {name} widget")
                self.widgets[name].from_xml(element)

    def to_dict(self):
        #export data to dictionary
        config_data = {}
        for name, wrapper in self.widgets.items():
            config_data[name] = wrapper.get_Value()
        return config_data
