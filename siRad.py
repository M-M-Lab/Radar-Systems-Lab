#https://pypi.org/project/pyserial/
from textwrap import wrap
#import serial
import math

# ---------- COMMANDS FORMATTING ------------ #

# https://stackoverflow.com/a/21872007
def twosComplement(val):
    if isinstance(val, int):
        return format(val % (1 << 16), '016b')
    else:
        raise TypeError("The input must be an integer.")

def hexificator(bits):
    if (isinstance(bits, str) and (len(bits) % 4) == 0):
        splittedString = wrap(bits, 4)
        hexStrings = [hex(int(subString,2))[2:] for subString in splittedString]
        return ''.join(hexStrings)
    else:
        raise TypeError("The input must be a string and it must contain a number of bits multiple of four.")

def bandwidthConfiguration(BW=1000):
    if isinstance(BW, int):
        if BW <= 65534 and BW >= -65536:
            val = int(BW/2)
            bitString = '0000000000000000' + twosComplement(val)
            fullCommand = "!P" + hexificator(bitString) + "\r\n"
            return fullCommand
        else:
            raise ValueError("The bandwidth must be a number between -65536 MHz and 65534 MHz.")
    else:
        raise TypeError("The input must be an integer.")

def selfTrigDelaySetting(delay=0):
    if isinstance(delay, int):
        if delay <= 128 and delay >= 0:
            if delay == 0:
                return '000'
            pow = math.log(delay,2)
            if (math.ceil(pow) != math.floor(pow)):
                twoPow = math.floor(pow)
                delay = int(2**twoPow) # round to the lowest power of two
            else:
                twoPow = int(pow)
            return '{0:03b}'.format(twoPow)
        else:
            raise ValueError("The delay must be a number between 0 ms and 128 ms.")
    else:
        raise TypeError("The input must be an integer.")

def systemConfiguration():
    selfTrigDelay = selfTrigDelaySetting()
    res = '0' # reserved
    LOG = '1' # linear magnitude
    FMT = '0' # TL in mm
    LED = '00' # LED off
    protocol = '010' # bin output
    AGC = '0' # automatic gain control off
    gain = '00' # 8dB - FUNCTION MUST BE IMPLEMENTED
    SER2 = '0' # output on SER2 off
    SER1 = '1' # output on SER1 on
    dataFrames = '00000001' # only RAW data on
    SLF = '1' # standard mode
    PRE = '0' # standard mode
    command = selfTrigDelay + res + LOG + FMT + LED + res + res + res + res + protocol + AGC + gain + SER2 + SER1 + dataFrames + res + res + SLF + PRE
    return '!S' + hexificator(command) + '\r\n'

# ---------- SERIAL HANDLING ------------ #

""" def findSerialDevice(hwID="pappappero"):
    radarBoard = serial.tools.list_ports.grep(hwID)
    print(radarBoard.description) #debug purposes
    return radarBoard.device
 """