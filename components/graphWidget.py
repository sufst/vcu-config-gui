from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QSizePolicy, QComboBox
import pyqtgraph as pg
from PySide6.QtCore import Qt
from components.inputWidget import inputWidget
from components.inputWidgetWrapper import inputWidgetWrapper
from components.WidgetManager import widgetManager

class GraphWidget(pg.PlotWidget):
    def __init__(self, parent=None, title="Graph", xLabel="X Axis", xMax=100.0, yMax=500.0):
        self.xMax = xMax
        self.yMax = yMax
        super().__init__(parent)
        
        self.setBackground('#1D1D21')
        self.showGrid(x=True, y=True, alpha=0.3)
        self.setXRange(0, self.xMax, padding=0.02)
        self.setYRange(0, self.yMax, padding=0.05)
        self.setLabel('left', 'Torque (Nm)', color="#F0F0F0")
        self.setLabel('bottom', xLabel, color="#F0F0F0")
        self.setTitle(title, color="#F0F0F0", size="14pt")
        self.setScale(1.0)
        self.setLimits(xMin=0, xMax=self.xMax, yMin=0, yMax=self.yMax)
        self.plotData = self.plot([], [], symbol='o', symbolSize=10, symbolBrush='#2A95F6', pen=pg.mkPen('#2A95F6', width=2))

    def updatePlateau(self, maxTorque, slopeStart, slopeEnd, minTorque):
        x = [0, slopeStart, slopeEnd, self.xMax]
        y = [maxTorque, maxTorque, minTorque, minTorque]
        self.plotData.setData(x, y)

    def updatePedalCurve(self, maxTorque, deadzonePercent):
        x = [deadzonePercent, self.xMax]
        y = [0, maxTorque]
        self.plotData.setData(x, y)

class BaseGraphSection(QWidget):
    def __init__(self, main_window, title, xLabel, xMax, yMax):
        super().__init__()
        self.namePrefix = title.replace(" ", "_") #storing data to dict/xml

        self.layout = QHBoxLayout(self)
        
        self.graph = GraphWidget(main_window, title, xLabel, xMax, yMax)
        
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setAlignment(Qt.AlignTop)
        
        self.layout.addWidget(self.graph, stretch=4)
        self.layout.addWidget(self.sidebar, stretch=1)

class PedalGraphSection(BaseGraphSection):
    def __init__(self, main_window, sharedMaxTorque):
        super().__init__(main_window, "Pedal Map", "Pedal (%)", 100.0, 500.0)
        
        self.sidebarLayout.addWidget(QLabel("Pedal Settings"))

        self.maxTorque = sharedMaxTorque
        self.deadzone = inputWidget(self, True, 0, 1) #fraction 0-1
        
        self.sidebarLayout.addWidget(QLabel("Deadzone Frac:"))
        self.sidebarLayout.addWidget(self.deadzone)
        
        self.applyBtn = QPushButton("Update Map")
        self.applyBtn.clicked.connect(self.syncPedal)
        self.sidebarLayout.addWidget(self.applyBtn)

    def syncPedal(self):
        dzVal = self.deadzone.getStored() * 100.0
        self.graph.plotData.setData([0, dzVal, 100.0], [0, 0, self.maxTorque.getStored()])
    
    def getSettings(self):
        return {
            f"{self.namePrefix}_Max_Torque": self.maxTorque.getStored(),
            f"{self.namePrefix}_Deadzone": self.deadzone.getStored()
        }
    
    def toXML(self):
        maxTorque = self.maxTorque.getStored()
        deadzone = self.deadzone.getStored()
        return f'\n   <Deadzone_{self.namePrefix}>{deadzone}</Deadzone_{self.namePrefix}>\n'
    
    def fromXML(self, deadzone):
        self.deadzone.setValue(deadzone)
        self.syncPedal()

class PlateauGraphSection(BaseGraphSection):
    def __init__(self, main_window, title, x_label, x_max, sharedMaxTorque):
        super().__init__(main_window, title, x_label, x_max, 500.0)
        
        self.sidebarLayout.addWidget(QLabel(f"{title} Settings"))
        self.maxTorque = sharedMaxTorque
        self.slopeStart = inputWidget(self, False, 0, x_max)
        self.slopeEnd = inputWidget(self, False, 0, x_max)
        self.minTorque = inputWidget(self, False, 0, 500)

        self.sidebarLayout.addWidget(QLabel("Slope Start:"))
        self.sidebarLayout.addWidget(self.slopeStart)
        self.sidebarLayout.addWidget(QLabel("Slope End:"))
        self.sidebarLayout.addWidget(self.slopeEnd)
        self.sidebarLayout.addWidget(QLabel("Min Torque (Shelf):"))
        self.sidebarLayout.addWidget(self.minTorque)

        self.applyBtn = QPushButton("Update Map")
        self.applyBtn.clicked.connect(self.syncPlateau)
        self.sidebarLayout.addWidget(self.applyBtn)

    def syncPlateau(self):
        x = [0, self.slopeStart.getStored(), self.slopeEnd.getStored(), self.graph.xMax]
        y = [self.maxTorque.getStored(), self.maxTorque.getStored(), self.minTorque.getStored(), self.minTorque.getStored()]
        self.graph.plotData.setData(x, y)

    def get_settings(self):
        return {
            f"{self.namePrefix}_Max_Torque": self.maxTorque.getStored(),
            f"{self.namePrefix}_Slope_Start": self.slopeStart.getStored(),
            f"{self.namePrefix}_Slope_End": self.slopeEnd.getStored(),
            f"{self.namePrefix}_Min_Torque": self.minTorque.getStored()
        }
    
    def toXML(self):
        slopeStart = self.slopeStart.getStored()
        slopeEnd = self.slopeEnd.getStored()
        minTorque = self.minTorque.getStored()
        return f'   <Slope_Start_{self.namePrefix}>{slopeStart}</Slope_Start_{self.namePrefix}>\n   <Slope_End_{self.namePrefix}>{slopeEnd}</Slope_End_{self.namePrefix}>\n   <Min_Torque_{self.namePrefix}>{minTorque}</Min_Torque_{self.namePrefix}>\n'

    def fromXML(self, slopeStart, slopeEnd, minTorque):
        self.slopeStart.setValue(slopeStart)
        self.slopeEnd.setValue(slopeEnd)
        self.minTorque.setValue(minTorque)
        self.syncPlateau()