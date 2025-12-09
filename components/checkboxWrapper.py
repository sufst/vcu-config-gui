from components.WidgetWrapper import widgetWrapper
class checkboxWrapper(widgetWrapper):
    def __init__(self, widget = None ,tag_name = "checkbox", context = None):
        super().__init__(tag_name, context ,widget or checkboxWidget())

    def to_xml(self):
        return f'<{self.tag_name}>{self.widget.isChecked()}</{self.tag_name}>'
    
    def from_xml(self, xml):
        check = xml.text
        self.widget.setChecked(check == 'True')

    def get_Value(self):
        return self.widget.isChecked()
    
    def get_context(self):
        return self.context