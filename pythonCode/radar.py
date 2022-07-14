#https://pypi.org/project/pyserial/
from serial import Serial,EIGHTBITS,PARITY_NONE,STOPBITS_ONE
import serial.tools.list_ports as list_SrlPorts
from configurationCommands import *
import numpy as np

def findSerialDevice():
    radarBoard = list_SrlPorts.comports()
    for rb in radarBoard:
        print(rb.device)
        if '/dev/tty' in rb.device:
            return rb.device


class radar():
    def __init__(self,radar2processor_dataQ,GUI2radar_controlQ) -> None:
        #Queue
        self.dataQ=radar2processor_dataQ
        self.controlQ=GUI2radar_controlQ

        #Init
        radarSrlAddress=findSerialDevice()
        if not radarSrlAddress:
            print('No device found, quitting.')
            quit()

        self.comPort= Serial(radarSrlAddress,1000000,EIGHTBITS,PARITY_NONE,STOPBITS_ONE,0.1)

        #System configuration
        command=systemConfiguration(0)
        self.comPort.write(command.encode())

        #Baseband configuration
        command=basebandConfiguration(1,32,0)
        self.currentBB=[1,32] #Set default Ramps, samples
        self.comPort.write(command.encode())

        #PLL configuration
        command=bandwidthConfiguration(3000)
        self.comPort.write(command.encode())
        
        self.run()

    def run(self):
        try:
            while True:
                self.comPort.write(str.encode('!N\r\n'))
                buf=''
                while not buf.startswith('!M'):
                    buf=self.comPort.readline().decode("utf-8")
                self.dataQ.put(buf)
                if self.controlQ.qsize():
                    self.updateParams()
                #print('radar Q', self.dataQ.qsize())

        except KeyboardInterrupt:
            print('Closing com port.')
            self.comPort.close()

    def updateParams(self):
        key,value=self.controlQ.get()
        if key=='Bandwidth':
            command=bandwidthConfiguration(value)
            self.comPort.write(command.encode())
        elif key=='Gain':
            command=systemConfiguration(value)
            self.comPort.write(command.encode())
        elif key=='Ramps':
            self.currentBB[0]=value
            command=basebandConfiguration(self.currentBB[0],self.currentBB[1],0)
            self.comPort.write(command.encode())
        elif key=='Samps':
            self.currentBB[1]=value
            command=basebandConfiguration(self.currentBB[0],self.currentBB[1],0)
            self.comPort.write(command.encode())
            
