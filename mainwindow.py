import pyqtgraph as pg
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QMessageBox, QFileDialog, QScrollArea, QGridLayout, QSizePolicy
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtCore import Qt, QSize
from components.graphWidget import PedalGraphSection, PlateauGraphSection, GraphWidget
from components.inputWidget import inputWidget
from components.inputWidgetWrapper import inputWidgetWrapper
from components.checkboxWrapper import checkboxWrapper
from components.WidgetManager import widgetManager
from components.graphWidget import GraphWidget
import xml.etree.ElementTree as Tree
import os


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("VCU-GUI")
        self.setWindowIcon(QIcon("stag.png"))
        self.setStyleSheet("background-color: #1D1D21;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(scroll_area)

        scroll_content = QWidget()
        scroll_content.setMaximumWidth(1200)

        main_layout = QVBoxLayout(scroll_content)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(15, 15, 15, 15)

        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        #grid formatting
        grid_layout.setSpacing(20)
        grid_layout.setAlignment(Qt.AlignCenter)
        
        menu_bar = self.menuBar() # menu bar to store file, settings and help
        file_menu = menu_bar.addMenu("File")

        # init the open button
        open_action = QAction(QIcon.fromTheme("document-open"), "&Open", self)
        open_action.setStatusTip("Open an XML file") 
        open_action.triggered.connect(self.open_file)   
        file_menu.addAction(open_action)

        save_action = QAction(QIcon.fromTheme("document-save"), "&Save", self)
        save_action.setStatusTip("Save the current file")
        save_action.triggered.connect(self.save)
        file_menu.addAction(save_action)

        self.widgetManager = widgetManager()

        #Main Title

        self.add_main_title(scroll_content, "VCU Config", "stag.png")

        #BPS Section
        self.add_section_title(grid_layout, "BPS Configuration", 1, 0)
        self.bpsPage = QWidget()
        self.bpsPage.setLayout(QVBoxLayout())


        MINADCName = "Min_ADC"
        self.MinADC = self.create_input_widget(self.bpsPage, MINADCName.replace("_", " "), 0, 0, 500, False)
        self.MinADC.setValue(0)
        self.widgetManager.add_widget(MINADCName, inputWidgetWrapper(self.MinADC, MINADCName, ".bps"))
        
        
        MAXADCName = "Max_ADC"
        self.MaxADC = self.create_input_widget(self.bpsPage, MAXADCName.replace("_", " "), 0, 0, 500, False)
        self.MaxADC.setValue(0)
        self.widgetManager.add_widget(MAXADCName, inputWidgetWrapper(self.MaxADC, MAXADCName, ".bps"))
        
        MINMAPPEDName = "Min_Mapped"
        self.MinMapped = self.create_input_widget(self.bpsPage, MINMAPPEDName.replace("_", " "), 0, 0, 500, False)
        self.MinMapped.setValue(0)
        self.widgetManager.add_widget(MINMAPPEDName, inputWidgetWrapper(self.MinMapped, MINMAPPEDName, ".bps"))

        MAXMAPPEDName = "Max_Mapped"
        self.MaxMapped = self.create_input_widget(self.bpsPage, MAXMAPPEDName.replace("_", " "), 0, 0, 500, False)
        self.MaxMapped.setValue(0)
        self.widgetManager.add_widget(MAXMAPPEDName, inputWidgetWrapper(self.MaxMapped, MAXMAPPEDName, ".bps"))

        FPFName = "Fully_Pressed_Fraction"
        self.FullyPressedFraction = self.create_input_widget(self.bpsPage, FPFName.replace("_"," "), 0, 0, 1, True) # create widget, assign page and name
        self.FullyPressedFraction.setValue(0) # set initial value
        self.widgetManager.add_widget(FPFName, inputWidgetWrapper(self.FullyPressedFraction, FPFName, ".bps")) # add widget to widget manager

        OBFBPSName = "Outside_Bounds_Fraction"
        self.OutsideBoundsFractionBPS = self.create_input_widget(self.bpsPage, OBFBPSName.replace("_"," "), 0, 0, 1, True)
        self.OutsideBoundsFractionBPS.setValue(0)
        self.widgetManager.add_widget(OBFBPSName, inputWidgetWrapper(self.OutsideBoundsFractionBPS, OBFBPSName, ".bps"))

        self.bpsPage.layout().addStretch(1)

        grid_layout.addWidget(self.bpsPage, 2, 0)

        #APPS Section
        self.add_section_title(grid_layout, "APPS Configuration", 1, 1)
        self.appsPage = QWidget()
        self.appsPage.setLayout(QVBoxLayout())

        MINADC1Name = "Min_ADC_1"
        self.MinADC1 = self.create_input_widget(self.appsPage, MINADC1Name.replace("_", " "), 20, 0, 500, False)
        self.MinADC1.setValue(0) #init value
        self.widgetManager.add_widget(MINADC1Name, inputWidgetWrapper(self.MinADC1, MINADC1Name, ".apps_1_scs"))

        MINADC2Name = "Min_ADC_2"
        self.MinADC2 = self.create_input_widget(self.appsPage, MINADC2Name.replace("_", " "), 20, 0, 500, False)
        self.MinADC2.setValue(0)
        self.widgetManager.add_widget(MINADC2Name, inputWidgetWrapper(self.MinADC2, MINADC2Name, ".apps_2_src"))

        MAXADC1Name = "Max_ADC_1"
        self.MaxADC1 = self.create_input_widget(self.appsPage, MAXADC1Name.replace("_", " "), 20, 0, 500, False)
        self.MaxADC1.setValue(0)
        self.widgetManager.add_widget(MAXADC1Name, inputWidgetWrapper(self.MaxADC1, MAXADC1Name, ".apps_1_scs"))

        MAXADC2Name = "Max_ADC_2"
        self.MaxADC2 = self.create_input_widget(self.appsPage, MAXADC2Name.replace  ("_", " "), 20, 0, 500, False)
        self.MaxADC2.setValue(0)
        self.widgetManager.add_widget(MAXADC2Name, inputWidgetWrapper(self.MaxADC2, MAXADC2Name, ".apps_2_src"))

        MINMAPPED1Name = "Min_Mapped_1"
        self.MinMapped1 = self.create_input_widget(self.appsPage, MINMAPPED1Name.replace("_", " "), 20, 0, 500, False)
        self.MinMapped1.setValue(0)
        self.widgetManager.add_widget(MINMAPPED1Name, inputWidgetWrapper(self.MinMapped1, MINMAPPED1Name, ".apps_1_scs"))

        MINMAPPED2Name = "Min_Mapped_2"
        self.MinMapped2 = self.create_input_widget(self.appsPage, MINMAPPED2Name.replace("_", " "), 20, 0, 500, False)
        self.MinMapped2.setValue(0)
        self.widgetManager.add_widget(MINMAPPED2Name, inputWidgetWrapper(self.MinMapped2, MINMAPPED2Name, ".apps_2_src"))

        MAXMAPPED1Name = "Max_Mapped_1"
        self.MaxMapped1 = self.create_input_widget(self.appsPage, MAXMAPPED1Name.replace("_", " "), 20, 0, 500, False)
        self.MaxMapped1.setValue(0)
        self.widgetManager.add_widget(MAXMAPPED1Name, inputWidgetWrapper(self.MaxMapped1, MAXMAPPED1Name, ".apps_1_scs"))

        MAXMAPPED2Name = "Max_Mapped_2"
        self.MaxMapped2 = self.create_input_widget(self.appsPage, MAXMAPPED2Name.replace("_", " "), 20, 0, 500, False)
        self.MaxMapped2.setValue(0)
        self.widgetManager.add_widget(MAXMAPPED2Name, inputWidgetWrapper(self.MaxMapped2, MAXMAPPED2Name, ".apps_2_src"))

        OBFA1Name = "Outside_Bounds_Fraction_1"
        self.OutsideBoundsFractionAPPS1 = self.create_input_widget(self.appsPage, OBFA1Name.replace("_"," "), 20, 0, 1, True)
        self.OutsideBoundsFractionAPPS1.setValue(0.0)
        self.widgetManager.add_widget(OBFA1Name, inputWidgetWrapper(self.OutsideBoundsFractionAPPS1, OBFA1Name,".apps_1_scs"))

        OBFA2Name = "Outside_Bounds_Fraction_2"
        self.OutsideBoundsFractionAPPS2 = self.create_input_widget(self.appsPage, OBFA2Name.replace("_"," "), 20, 0, 1, True)
        self.OutsideBoundsFractionAPPS2.setValue(0)
        self.widgetManager.add_widget(OBFA2Name, inputWidgetWrapper(self.OutsideBoundsFractionAPPS2, OBFA2Name, ".apps_2_src"))

        MDName = "Max_Discrepancy"
        self.MaxDiscrepancy = self.create_input_widget(self.appsPage, MDName.replace("_"," "), 20, 0, 500, False)
        self.MaxDiscrepancy.setValue(0)
        self.widgetManager.add_widget(MDName, inputWidgetWrapper(self.MaxDiscrepancy, MDName, ".apps"))

        self.appsPage.layout().addStretch(1)

        grid_layout.addWidget(self.appsPage, 2, 1)

        #Control Section
        self.add_section_title(grid_layout, "Control Configuration", 1, 3)
        self.controlPage = QWidget()
        self.controlPage.setLayout(QVBoxLayout())
        FOTName = "Fan_On_Threshold"
        self.FanOnThreshold = self.create_input_widget(self.controlPage, FOTName.replace("_", " "), 20, 0, 100, False)
        self.FanOnThreshold.setValue(0)
        self.widgetManager.add_widget(FOTName, inputWidgetWrapper(self.FanOnThreshold, FOTName, ".ctrl"))

        FOFName = "Fan_Off_Threshold"
        self.FanOffThreshold = self.create_input_widget(self.controlPage, FOFName.replace("_", " "), 20, 0, 100, False)
        self.FanOffThreshold.setValue(0)
        self.widgetManager.add_widget(FOFName, inputWidgetWrapper(self.FanOffThreshold, FOFName , ".ctrl"))

        RCName = "Remote_Control"
        self.RemoteControl = self.create_checkbox(self.controlPage, RCName.replace("_"," "), 20)
        self.RemoteControl.setChecked(False)
        self.widgetManager.add_widget(RCName, checkboxWrapper(self.RemoteControl, RCName))

        self.controlPage.layout().addStretch(1)
        grid_layout.addWidget(self.controlPage, 2, 3)

        main_layout.addWidget(grid_widget)

        #Graph Section
        #self.graphWidget = GraphWidget(self)
        #graphControl = self.graphWidget.create_graph_controls()

        #graph_section = QWidget()
        #graph_layout = QHBoxLayout(graph_section)
        #graph_layout.addStretch(1)
        #graph_layout.addWidget(self.graphWidget)
        #graph_layout.addWidget(graphControl)
        #graph_layout.addStretch(1)
        #main_layout.addWidget(graph_section)
        graphGrid = QGridLayout()

        self.sharedMaxTorque = inputWidget(self, False, 0, 500)
        self.sharedMaxTorque.setValue(0)

        sharedTorqueContainer = QWidget()
        sharedTorqueLayout = QHBoxLayout(sharedTorqueContainer)
        sharedTorqueLayout.addWidget(QLabel("Shared Max Torque:"))
        sharedTorqueLayout.addWidget(self.sharedMaxTorque)
        sharedTorqueLayout.addStretch(1)
        main_layout.addWidget(sharedTorqueContainer)



        self.pedalMap = PedalGraphSection(self, sharedMaxTorque=self.sharedMaxTorque)
        graphGrid.addWidget(self.pedalMap, 0, 0)

        self.thermalMap = PlateauGraphSection(self, "Thermal", "Temp (°C)", 70.0, sharedMaxTorque=self.sharedMaxTorque)
        graphGrid.addWidget(self.thermalMap, 0, 1)

        self.batteryMap = PlateauGraphSection(self, "Battery", "Charge (%)", 100.0, sharedMaxTorque=self.sharedMaxTorque)
        graphGrid.addWidget(self.batteryMap, 1, 0)

        self.speedMap = PlateauGraphSection(self, "Speed", "RPM", 5000.0, sharedMaxTorque=self.sharedMaxTorque)
        graphGrid.addWidget(self.speedMap, 1, 1)

        main_layout.addLayout(graphGrid)

        #Buttons for sending to VCU section

        button_section = QWidget()
        button_layout = QHBoxLayout(button_section)
        button_layout.setAlignment(Qt.AlignCenter)
        self.controlWriteButton = QPushButton("Write Config to VCU")
        self.controlWriteButton.clicked.connect(self.configToCAN)
        self.controlWriteButton.setFixedSize(200, 50)
        button_layout.addWidget(self.controlWriteButton)
        self.torqueWriteButton = QPushButton("Write Torque Data to VCU")
        self.torqueWriteButton.clicked.connect(self.torqueToCan)
        self.torqueWriteButton.setFixedSize(200, 50)
        button_layout.addWidget(self.torqueWriteButton)
        main_layout.addWidget(button_section)
        scroll_area.setWidget(scroll_content)

    ## HELPER FUNCTIONS

    def add_section_title(self, parent, title, row, col):
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 15px; margin-bottom: 10px; color: #2A95F6;")
        parent.layout().addWidget(title_label, row, col)

    def add_main_title(self, parent, title, logo_path):
        title_container = QWidget()
        horiz_layout = QHBoxLayout(title_container)
        logo_label = QLabel()
        icon = QIcon(logo_path)
        icon_size = 48
        #conv to pixel map icon
        pixmap = icon.pixmap(QSize(icon_size, icon_size), QIcon.Normal, QIcon.Off)
        logo_label.setPixmap(pixmap)
        horiz_layout.addWidget(logo_label)
        main_title = QLabel(title)
        main_title.setStyleSheet("font-weight: bold; font-size: 25px; margin-top: 10px; margin-bottom: 10px; color: #2A95F6;")
        main_title.setAlignment(Qt.AlignCenter)
        horiz_layout.addWidget(main_title)
        horiz_layout.addStretch(1)
        parent.layout().addWidget(title_container, alignment=Qt.AlignCenter)

    def create_input_widget(self, parent, label, spacing, minVal, maxVal, isFraction):
        layout = QHBoxLayout()
        layout.setSpacing(spacing)
        label_widget = QLabel(label)
        layout.addWidget(label_widget)
        label_widget.setStyleSheet("color: #F0F0F0;")
        iw = inputWidget(parent, isFraction, minVal, maxVal)
        layout.addWidget(iw)
        parent.layout().addLayout(layout)
        return iw

    def create_checkbox(self, parent, label, spacing):
        layout = QHBoxLayout()
        layout.setSpacing(spacing)
        layout.addWidget(QLabel(label))
        checkbox = QCheckBox()
        layout.addWidget(checkbox)
        parent.layout().addLayout(layout)
        return checkbox
    

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(None, "Select Save Location", "", "XML Files (*.xml);;All Files (*)")

        if filePath:
            if not filePath.lower().endswith(".xml"):
                filePath += ".xml"
            sharedMaxXML = f'\n   <Shared_Max_Torque>{self.sharedMaxTorque.getStored()}</Shared_Max_Torque>'
            xml_content = self.widgetManager.to_xml() + sharedMaxXML + self.pedalMap.toXML() + self.thermalMap.toXML() + self.batteryMap.toXML() + self.speedMap.toXML() + "</Configs>"
            print (xml_content)
            with open(filePath, "w") as file:
                file.write(xml_content)
                QMessageBox.information(self, "Success", f"File successfully saved to {filePath}")
    

    def open_file(self):
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.AnyFile)
            dialog.setNameFilter("XML Files (*.xml);;All Files (*)")
            dialog.setViewMode(QFileDialog.Detail)
            if dialog.exec():
                file_path = dialog.selectedFiles()[0]
                tree = Tree.parse(file_path)
                root = tree.getroot()
                xml_content = Tree.tostring(root, encoding ='unicode')
                self.widgetManager.from_xml(xml_content)
                data = {child.tag: child.text for child in root}
                #shared max
                if "Shared_Max_Torque" in data:
                    self.sharedMaxTorque.setValue(float(data["Shared_Max_Torque"]))
                
                if "Deadzone_Pedal_Map" in data:
                    self.pedalMap.fromXML(float(data["Deadzone_Pedal_Map"]))
                for section, prefix in [(self.thermalMap, "Thermal"), (self.batteryMap, "Battery"), (self.speedMap, "Speed")]:
                    s_start = data.get(f"Slope_Start_{prefix}")
                    s_end = data.get(f"Slope_End_{prefix}")
                    m_torque = data.get(f"Min_Torque_{prefix}")

                    if all(v is not None for v in [s_start, s_end, m_torque]):
                        section.fromXML(float(s_start), float(s_end), float(m_torque))

    def getAllConfigData(self):
        #collect config data to dictionary.
        configData = {}
        configData.update(self.widgetManager.to_dict())
        return configData

    def getAllTorqueData(self):
        torqueData = {}
        torqueData.update(self.pedalMap.getSettings())
        torqueData.update(self.thermalMap.get_settings())
        torqueData.update(self.batteryMap.get_settings())
        torqueData.update(self.speedMap.get_settings())
        return torqueData

    def configToCAN(self):
        #collect to dict each time pressed.
        configData = self.getAllConfigData()
        #TODO: CAN LOGIC.
        print(configData)

    def torqueToCan(self):
        torqueData = self.getAllTorqueData()
        print(torqueData)
        #TODO: CAN LOGIC
                