import multiprocessing
from radar import radar
from processor import process
from GUI import mainWindow
from PySide2.QtWidgets import QApplication

####### Queue
#DataQ
radar2processor_dataQ=multiprocessing.Queue()
processor2GUI_dataQ=multiprocessing.Queue()

#ControlQ
GUI2radar_controlQ=multiprocessing.Queue()
GUI2processor_controlQ=multiprocessing.Queue()

####### Process

#Radar
radar_child=multiprocessing.Process(target=radar, args=(radar2processor_dataQ,GUI2radar_controlQ))
radar_child.daemon=True
radar_child.start()

#Processor
processor_child=multiprocessing.Process(target=process, args=(radar2processor_dataQ,processor2GUI_dataQ,GUI2processor_controlQ))
processor_child.daemon=True
processor_child.start()

#GUI
app = QApplication([])
gui=mainWindow(processor2GUI_dataQ,GUI2processor_controlQ,GUI2radar_controlQ)
gui.showMaximized()
app.exec_()