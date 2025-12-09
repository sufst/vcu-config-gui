from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QSizePolicy, QComboBox
import pyqtgraph as pg
from PySide6.QtCore import Qt
from components.inputWidget import inputWidget
from components.inputWidgetWrapper import inputWidgetWrapper
from components.WidgetManager import widgetManager

class GraphWidget(pg.PlotWidget):
    def __init__(self, main_window):
        x_axis = pg.AxisItem(orientation='bottom')
        y_axis = pg.AxisItem(orientation='left')

        self.initialDeadzone = 0
        self.initialMaxTorque = 0
        self.initialMinTorque = 0
        self.xMax = 100.00
        self.yMax = 5000.00

        x_axis.setTicks([[(i, str(i)) for i in range(0, int(self.xMax) + 1, int(self.xMax)//10)]])
        y_axis.setTicks([[(i, str(i)) for i in range(0, int(self.yMax) + 1, int(self.yMax)//10)]])

        super().__init__(main_window, axisItems={'bottom': x_axis, 'left': y_axis})
        self.setMouseEnabled(x=False, y=False)
        self.setMinimumSize(600, 400)
        self.setSizePolicy(
            QSizePolicy.Expanding,   # Can grow horizontally
            QSizePolicy.Expanding    # Can grow vertically
        )
    
        self.setXRange(0.00, self.xMax, padding=0.02)
        self.setYRange(0.00, self.yMax, padding=0)
        self.setLabel('left', 'Torque (Nm)', color="#F0F0F0", size="12px")
        self.setLabel('bottom', 'Pedal Position (%)', color="#F0F0F0", size="16px")
        self.setTitle("Torque Map", color="#F0F0F0", size="16px")
        # self.setRange(xRange=[0.00, self.xMax], yRange=[0.00, self.yMax], padding=0.05)

        self.plotData = self.plot([], [], symbol='o', symbolSize=10, symbolBrush=('#2A95F6'))
        
        self.deleting = False
        self.dragging_point = None
        self.dragging_index = None
        self.scene().installEventFilter(self)
        
        self.autoSort = True ## sort the graph points by x value allow to change later

        self.setPlot([self.initialDeadzone, self.xMax], [self.initialMinTorque, self.initialMaxTorque])

        self.pen = pg.mkPen(color=("#09315A"), width=2)
        self.roi = pg.ROI([0, 0], [self.initialDeadzone, self.yMax], pen=self.pen, hoverPen = self.pen , maxBounds=pg.QtCore.QRectF(0, 0, self.yMax, self.yMax), 
                            movable=False, rotatable=False, resizable=False, removable=False)
        self.addItem(self.roi)


    def create_graph_controls(self):
        graphControl = QWidget()
        graphControl.setLayout(QVBoxLayout())
        graphControl.layout().setSpacing(0)
        graphControl.layout().setContentsMargins(0, 0, 0, 0)
        graphControl.layout().setAlignment(Qt.AlignLeft)

        self.comboBox = QComboBox()
        self.comboBox.addItems(["Torque map 1", "Torque map 2", "Torque map 3"])
        graphControl.layout().addWidget(self.comboBox)

        OUTPUTMAXname = "Maximum_Torque"
        self.outputMax = self.create_input_widget(graphControl, OUTPUTMAXname.replace("_", " "),1, 0, 3000, False, connect_callback=self.on_max_output_change)
        self.outputMax.setValue(self.initialMinTorque)

        DEADZONEFRACname = "Deadzone_Fraction"
        self.deadzoneFrac = self.create_input_widget(graphControl, DEADZONEFRACname.replace("_", " "),1, 0, 1, True, connect_callback=self.on_deadzone_change)
        self.deadzoneFrac.setValue(self.initialDeadzone / 100.0)

        return graphControl

    def on_deadzone_change(self, value):
        deadzone_percent = value * 100.0

        #ensure deadzone less than last point.
        if deadzone_percent < self.xMax:
            xData = list(self.plotData.xData)
            xData[0] = deadzone_percent
            self.setPlot(xData, list(self.plotData.yData))
            #update ROI
            self.roi.setSize([deadzone_percent, self.yMax])


    def on_max_output_change(self, value):
        yData = list(self.plotData.yData)
        yData[-1] = value
        self.setPlot(list(self.plotData.xData), yData)


    def update_Plot_Data(self):
        # self.plotData.setData.sort()
        # print("graph re-drawn")
        self.plotData.setData(self.plotData.xData, self.plotData.yData)

    def setPlot(self, x, y):
        self.plotData.setData(x, y)

    def from_xml(self, xData, yData):
        self.setPlot(xData, yData)
        self.update_Plot_Data()
        if len(xData) > 0 and len(yData) > 0:
            self.deadzoneFrac.setValue(xData[0]/100.0)
            if len(yData) > 1:
                self.outputMax.setValue(yData[-1])
        deadzone_percent = xData[0]
        self.roi.setSize([deadzone_percent, self.yMax])
        self.roi.removeHandle(0)
        self.roi.addScaleHandle([1, 0.5], [0, 0.5])

    def to_xml(self):
        xml_content = "\n" #init string
        xml_content += "   <Deadzone_Fraction>" + f"{self.plotData.xData[0]/100.0}" + "</Deadzone_Fraction>\n"
        xml_content += "   <Max_Output>" + f"{self.plotData.yData[-1]}" + "</Max_Output>\n"
        return xml_content
    
    def create_input_widget(self, parent, label, spacing, minVal, maxVal, isFraction, connect_callback=None):
        layout = QHBoxLayout()
        layout.setSpacing(spacing)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        
        label_widget = QLabel(label)
        iw = inputWidget(parent, isFraction, minVal, maxVal)
        apply_btn = QPushButton("Apply")
        apply_btn.setMaximumWidth(60)

        layout.addWidget(label_widget)
        layout.addWidget(iw)
        layout.addWidget(apply_btn)
        layout.addStretch(1)
        parent.layout().addLayout(layout)

        if connect_callback:
            apply_btn.clicked.connect(lambda: connect_callback(iw.getStored()))

        return iw