# GUI MODULE

# Import libraries
import numpy as np
from queue import Empty
from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QApplication
from WindowDefinition import Ui_MainWindow
import pyqtgraph as pg

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
        #print(getmembers(self.win.GraphWidget))
        self.imageItem=pg.ImageItem()
        self.plotItem=pg.PlotItem()
        self.plotItem.getViewBox().invertY(True)
        self.win.GraphWidget.setCentralItem(self.plotItem)

        self.cm=pg.colormap.get('inferno')
        self.bar = pg.ColorBarItem(colorMap=self.cm ) 
        self.bar.setImageItem(self.imageItem, insert_in=self.plotItem)
        
        #self.imageItem.setColorMap()

        self.plotItem.addItem(self.imageItem)
        #self.XaxisItem=pg.AxisItem('bottom')
        #self.XaxisItem.setGrid(1)
        #self.plotItem.addItem(self.XaxisItem)

        #Connection
        self.win.BWSpinBox.valueChanged.connect(self.updateBandwidth)
        self.win.GainComboBox.currentTextChanged.connect(self.updateGain)
        self.win.RampsComboBox.currentTextChanged.connect(self.updateRamps)
        self.win.FSComboBox.currentTextChanged.connect(self.updateFS)
        self.win.SampsComboBox.currentTextChanged.connect(self.updateSamps)
        self.win.SaveFileButton.clicked.connect(self.dump2file)

        #Schedule GUI update
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1/30) #Funziona finchè processore è più lento
        self.timer.timeout.connect(self.updateGUI)
        self.timer.start()
        
        #Radar params
        self.FS=2.571
        self.Ramps=1
        self.bandwidth=6000
        self.PRI=0.015
        self.gain=8
        
        #Setup processor
        self.updateSamps()



    def updateGUI(self):
        try:
            RDMap,self.PRI=self.dataQ.get(timeout=1)
            #print('Gui Q',self.dataQ.qsize())
        except Empty:
            print('GUI found empty queue, processor stuck?')
            return
        
        self.win.PRIValue.setText("{0:.2f}".format(self.PRI*1e3))
        lev=self.bar.levels()
        self.imageItem.setImage(RDMap.T)
        self.bar.setLevels([1,np.max(RDMap)])
        self.imageItem.setRect(-self.maxV,self.maxR,2*self.maxV,-self.maxR)

    def updateBandwidth(self):
        value=self.win.BWSpinBox.value()
        if value:
            self.bandwidth=value
            self.radarControlQ.put(('Bandwidth',value))
            self.rescaleAxis()
    
    def updateGain(self):
        value=int(self.win.GainComboBox.currentIndex())
        self.gain=value
        self.radarControlQ.put(('Gain',value))

    def updateRamps(self):
        value=int(self.win.RampsComboBox.currentText())
        self.Ramps=value
        self.radarControlQ.put(('Ramps',value))
        self.rescaleAxis()

    def updateSamps(self):
        value=int(self.win.SampsComboBox.currentText())
        self.Samps=value
        self.radarControlQ.put(('Samps',value))
        self.processorControlQ.put(('Samps',value))
        self.rescaleAxis()
    
    def updateFS(self):
        value=float(self.win.FSComboBox.currentText())
        self.FS=value
        self.radarControlQ.put(('FS',36/value))
        self.rescaleAxis()
    
    def rescaleAxis(self):
        #Tr=(85+self.Samps)/(self.FS*1e6)
        self.maxR=(self.Samps+37.4)*3e8/(4e6*self.bandwidth) #self.FS*3e8*Tr/(2*self.bandwidth)
        self.maxV=0.25/(4*self.PRI) #Velocità in cm/s
    
    def dump2file(self):
        if self.win.SaveFileButton.isChecked():
            #Disable panel control
            self.win.BWSpinBox.setEnabled(False)
            self.win.GainComboBox.setEnabled(False)
            self.win.RampsComboBox.setEnabled(False)
            self.win.SampsComboBox.setEnabled(False)
            self.win.FSComboBox.setEnabled(False)



            self.win.SaveFileButton.setText('Acquiring...')
            value={'Bandwidth':self.bandwidth,
                'SamplingFrequency':self.FS,
                'Ramps':self.Ramps,
                'Samps':self.Samps,
                'PRI':"{0:.5f}".format(self.PRI),
                'Gain':self.gain
                }
            self.processorControlQ.put(('Dump',value))
        else:
            self.win.BWSpinBox.setEnabled(True)
            self.win.GainComboBox.setEnabled(True)
            self.win.RampsComboBox.setEnabled(True)
            self.win.SampsComboBox.setEnabled(True)
            self.win.FSComboBox.setEnabled(True)
            self.win.SaveFileButton.setText('Save to file')
            self.processorControlQ.put(('Dump',False))

        