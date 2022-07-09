#https://pypi.org/project/pyserial/


# https://stackoverflow.com/a/21872007
def twosComplement(val):
    return format(val % (1 << 16), '016b')

def hexify(bits):
    return hex(int(bits,2))[2:]

def bandwidthConfiguration(BW):
    start = "!P"
    stop = "\r\n"
    val = int(BW/2)
    bitString = '0000000000000000' + twosComplement(val)
    command = hexify(bitString[0:4]) + hexify(bitString[4:8]) + hexify(bitString[8:12]) + hexify(bitString[12:16]) + hexify(bitString[16:20]) + hexify(bitString[20:24]) + hexify(bitString[24:28]) + hexify(bitString[28:])   
    fullCommand = start + command + stop
    return fullCommand

