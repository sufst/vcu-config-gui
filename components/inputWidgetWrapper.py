from components.WidgetWrapper import widgetWrapper
from components.inputWidget import inputWidget

class inputWidgetWrapper(widgetWrapper):
    def __init__(self, widget = None, tag_name = "input", context = None):
        super().__init__(tag_name, context, widget or inputWidget())

    def to_xml(self):
        val = self.widget.getStored()
        return f'<{self.tag_name}>{val}</{self.tag_name}>'
    
    def from_xml(self, element):
        if (element.text.find('.') == -1): # contains a decimal
            value = int(element.text)
        else:
            value = float(element.text)
        self.widget.setValue(value)

    def get_Value(self):
        return self.widget.getStored()
    
    def get_context(self):
        return self.context