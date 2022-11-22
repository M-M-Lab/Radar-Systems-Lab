#https://pypi.org/project/pyserial/

from serial.tools import list_ports

def findSerialDevice(vid=6790):
    devices = list_ports.comports()
    for serObj in devices:
        if serObj.vid == vid: return serObj.device
    