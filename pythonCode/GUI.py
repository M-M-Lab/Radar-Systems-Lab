# GUI MODULE

# Import libraries
import sys
from queue import Empty
import pyqtgraph as pg
from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QApplication
from MainWindow import Ui_MainWindow

class mainWindow(QMainWindow):
    def __init__(self,processor2GUI_dataQ,GUI2processor_controlQ,GUI2radar_controlQ) -> None:
        super(mainWindow, self).__init__()

        #Queue
        self.dataQ=processor2GUI_dataQ
        self.radarControlQ=GUI2radar_controlQ
        self.processorControlQ=GUI2processor_controlQ

        #UI
        self.win=Ui_MainWindow()
        self.win.setupUi(self)

        #Plot
        self.curve=self.win.GraphWidget.plot()
        #self.XaxisItem=pg.AxisItem('bottom')
        #self.XaxisItem.setGrid(1)

        #Connection
        self.win.BWSpinBox.valueChanged.connect(self.updateBandwidth)
        self.win.GainComboBox.currentTextChanged.connect(self.updateGain)
        self.win.RampsComboBox.currentTextChanged.connect(self.updateRamps)
        self.win.SampsComboBox.currentTextChanged.connect(self.updateSamps)

        #Schedule GUI update
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1/30)
        self.timer.timeout.connect(self.updateGUI)
        self.timer.start()

    def updateGUI(self):
        try:
            vector=self.dataQ.get(timeout=1)
            #print('Gui Q',self.dataQ.qsize())
        except Empty:
            print('GUI found empty queue, processor stuck?')
            return
        self.curve.setData(vector)

    def updateBandwidth(self):
        value=self.win.BWSpinBox.value()
        self.radarControlQ.put(('Bandwidth',value))
    
    def updateGain(self):
        value=int(self.win.GainComboBox.currentIndex())
        self.radarControlQ.put(('Gain',value))

    def updateRamps(self):
        value=int(self.win.RampsComboBox.currentText())
        self.radarControlQ.put(('Ramps',value))

    def updateSamps(self):
        value=int(self.win.SampsComboBox.currentText())
        self.radarControlQ.put(('Samps',value))