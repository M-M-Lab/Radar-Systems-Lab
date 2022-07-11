#https://pypi.org/project/pyserial/
from textwrap import wrap

# https://stackoverflow.com/a/21872007
def twosComplement(val):
    return format(val % (1 << 16), '016b')

def hexificator(bits):
    splittedString = wrap(bits, 4)
    hexStrings = [hex(int(subString,2))[2:] for subString in splittedString]
    return ''.join(hexStrings)

def bandwidthConfiguration(BW):
    start = "!P"
    stop = "\r\n"
    val = int(BW/2)
    bitString = '0000000000000000' + twosComplement(val)
    fullCommand = start + hexificator(bitString) + stop
    return fullCommand

