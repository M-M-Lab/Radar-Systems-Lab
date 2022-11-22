#https://pypi.org/project/pyserial/
from serial import Serial,EIGHTBITS,PARITY_NONE,STOPBITS_ONE
import serial.tools.list_ports as list_SrlPorts
from configurationCommands import *
import numpy as np
import time
from connectionHandler import findSerialDevice


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
        command=basebandConfiguration(1,32,14,0)
        self.currentBB=[1,32,14,0] #Set default Ramps, samples
        self.comPort.write(command.encode())

        #PLL configuration
        command=bandwidthConfiguration(6000)
        self.comPort.write(command.encode())
        
        self.run()

    def run(self):
        try:
            while True:
                self.comPort.write(str.encode('!N\r\n'))
                self.comPort.flush()
                buf=b''
                writtenBytes=0
                while not buf.startswith(b'\xaa\xaa\xbb\xccM'):
                    buf=self.comPort.read_until(expected=b'\r\n')
                    writtenBytes+=len(buf)
                tStamp=time.time()
                #print(writtenBytes,writtenBytes*8/1e3)
                #print(buf[:10])
                #print(buf[5:6],int.from_bytes(buf[5:6],"big"))
                #print(buf[7:8], int.from_bytes(buf[7:8],"big"))
                
                #print(int.from_bytes(buf,"big",signed=True))
                self.dataQ.put((buf,tStamp))
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
            command=basebandConfiguration(self.currentBB[0],self.currentBB[1],self.currentBB[2],self.currentBB[3])
            self.comPort.write(command.encode())
        elif key=='Samps':
            self.currentBB[1]=value
            command=basebandConfiguration(self.currentBB[0],self.currentBB[1],self.currentBB[2],self.currentBB[3])
            self.comPort.write(command.encode())
        elif key=='FS':
            self.currentBB[2]=value
            command=basebandConfiguration(self.currentBB[0],self.currentBB[1],self.currentBB[2],self.currentBB[3])
            self.comPort.write(command.encode())
            
