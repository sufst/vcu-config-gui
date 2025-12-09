from PySide6.QtCore import Qt, QLocale
from PySide6.QtGui import QDoubleValidator, QValidator, QIntValidator
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QWidget

class inputWidget(QWidget):
    def __init__(self, parent=None, isFraction=True, minVal=0.0, maxVal=1.0):
        super().__init__()

        self.input = QLineEdit()

        #store min, max vals
        self.minVal = minVal
        self.maxVal = maxVal
        self.decimals = 3 if isFraction else 0
        self.storedValue = float(minVal) if isFraction else int(minVal)

        self.setValue(self.storedValue)

        self.input.setAlignment(Qt.AlignLeft)
        self.input.editingFinished.connect(self.validateInput)
        self.input.setStyleSheet("color: #F0F0F0")

        # Layout
        layout = QHBoxLayout()
        layout.addWidget(self.input)
        self.setLayout(layout)
        self.input.setMaximumWidth(50)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignRight)

    def validateInput(self):
        input_text = self.input.text()
        try:
            value = float(input_text) if self.decimals == 3 else int(float(input_text))
            value = max(self.minVal, min(self.maxVal, value))  # Clamp value within min and max
            self.storedValue = value
        except ValueError:
            # Revert to last valid value if conversion fails
            pass
    
        self.setValue(self.storedValue)
    
    def getStored(self):
        return self.storedValue
    
    def setValue(self, value):
        value = max(self.minVal, min(self.maxVal, value))  # Clamp value within min and max

        if self.decimals == 0:
            self.storedValue = int(value)
            self.input.setText(str(self.storedValue))
        else:
            self.storedValue = float(value)
            self.input.setText(f"{self.storedValue:.{self.decimals}f}")