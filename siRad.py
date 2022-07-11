#https://pypi.org/project/pyserial/
from textwrap import wrap
import serial

# ---------- COMMANDS FORMATTING ------------ #

# https://stackoverflow.com/a/21872007
def twosComplement(val):
    return format(val % (1 << 16), '016b')

def hexificator(bits):
    splittedString = wrap(bits, 4)
    hexStrings = [hex(int(subString,2))[2:] for subString in splittedString]
    return ''.join(hexStrings)

def bandwidthConfiguration(BW):
    if BW <= 65534 and BW >= -65536:
        val = int(BW/2)
        bitString = '0000000000000000' + twosComplement(val)
        fullCommand = "!P" + hexificator(bitString) + "\r\n"
        return fullCommand
    else:
        raise ValueError("The bandwidth must be a number between -65536 MHz and 65534 MHz.")

# ---------- SERIAL HANDLING ------------ #

def findSerialDevice(hwID="pappappero"):
    radarBoard = serial.tools.list_ports.grep(hwID)
    print(radarBoard.description) #debug purposes
    return radarBoard.device

