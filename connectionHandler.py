#https://pypi.org/project/pyserial/

import serial

def findSerialDevice(hwID="CP2102"):
    radarBoard = serial.tools.list_ports.grep(hwID)
    print(radarBoard.description) #debug purposes
    return radarBoard.device
