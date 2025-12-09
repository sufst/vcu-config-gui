from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtGui import QIcon
from mainwindow import MainWindow
import sys
import signal

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("stag.png"))
window = MainWindow(app)
window.resize(800, 600)
window.show()
app.exec()
