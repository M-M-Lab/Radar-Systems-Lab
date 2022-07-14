from textwrap import wrap
import math

# ---------- AUXILIARY FUNCTIONS ------------ #

# https://stackoverflow.com/a/21872007
def twosComplement(val):
    if isinstance(val, int):
        return format(val % (1 << 16), '016b')
    else:
        raise TypeError("The input must be an integer.")

def hexificator(bits):
    if (isinstance(bits, str) and (len(bits) % 4) == 0):
        splittedString = wrap(bits, 4)
        hexStrings = [hex(int(subString,2)).upper()[2:] for subString in splittedString]
        return ''.join(hexStrings)
    else:
        raise TypeError("The input must be a string and it must contain a number of bits multiple of four.")

# ---------- CONFIGURATION COMMANDS ------------ #

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
        if delay >= 0 and delay <= 128:
            if delay == 0:
                return '{0:03b}'.format(0)
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

def systemConfiguration(gainLevel=0):
    selfTrigDelay = selfTrigDelaySetting()
    res = '0' # reserved
    LOG = '1' # linear magnitude
    FMT = '0' # TL in mm
    LED = '00' # LED off
    protocol = '010' # bin output
    AGC = '0' # automatic gain control off
    if gainLevel >= 0 and gainLevel <= 3:
        gain = '{0:02b}'.format(gainLevel) # gain - default 8dB
    else:
        gain = '00'
        print("\nWarning: wrong gain level. Gain set to 8dB.\n")
    SER2 = '0' # output on SER2 off
    SER1 = '1' # output on SER1 on
    dataFrames = '00000001' # only RAW data on
    SLF = '1' # standard mode
    PRE = '0' # standard mode
    command = selfTrigDelay + res + LOG + FMT + LED + res + res + res + res + protocol + AGC + gain + SER2 + SER1 + dataFrames + res + res + SLF + PRE
    return '!S' + hexificator(command) + '\r\n'

# ABOUT THE GAIN:
# gainLevel
# 0: 8dB
# 1: 21dB
# 2: 43dB
# 3: 56dB

def basebandConfiguration(nRamps=1,nSamples=32,downSampl=0):
    WIN = '0' # windowing off
    FIR = '0' # FIR filter off
    DC = '0' # DC cancellation off
    CFAR = '00' # CA-CFAR - disabled
    CFAR_T = '0000' # CFAR threshold - disabled
    CFAR_S = '0000' # CFAR size - disabled
    CFAR_G = '00' # CFAR guard - disabled
    averageN = '00' # how many FFTs are averaged - disabled
    FFTsize = '000' # number of FFT points - disabled

    if downSampl >= 0 and downSampl <= 64: # down sampling factor
        if downSampl == 0:
            downSamplCommand = '{0:03b}'.format(0)
        else:
            pow = math.log(downSampl,2)
            if (math.ceil(pow) != math.floor(pow)):
                downSamplCommand = '{0:03b}'.format(math.floor(pow) + 1)
            else:
                downSamplCommand = '{0:03b}'.format(int(pow) + 1)
    else:
        downSamplCommand = '{0:03b}'.format(0)
        print("\nWarning: wrong downsampling factor. Set to 0.\n")

    if nRamps >= 1 and nRamps <= 128: # number of ramps for each measurement
        pow = math.log(nRamps,2)
        if (math.ceil(pow) != math.floor(pow)):
            nRampsCommand = '{0:03b}'.format(math.floor(pow))
        else:
            nRampsCommand = '{0:03b}'.format(int(pow))
    else:
        nRampsCommand = '{0:03b}'.format(0)
        print("\nWarning: wrong number of ramps per measurement. Set to 1.\n")

    if nSamples >= 32 and nSamples <= 2048: # number of samples for each measurement
        pow = math.log(nSamples,2) - 5
        if (math.ceil(pow) != math.floor(pow)):
            nSamplesCommand = '{0:03b}'.format(math.floor(pow))
        else:
            nSamplesCommand = '{0:03b}'.format(int(pow))
    else:
        nSamplesCommand = '{0:03b}'.format(0)
        print("\nWarning: wrong number of samples per measurement. Set to 32.\n")

    ADC_clkDiv = '000' # sampling frequency - needs to be implemented?
    command = WIN + FIR + DC + CFAR + CFAR_T + CFAR_S + CFAR_G + averageN + FFTsize + downSamplCommand + nRampsCommand + nSamplesCommand + ADC_clkDiv
    return '!B' + hexificator(command) + '\r\n'

# ---------- SHORT COMMANDS ------------ #

def getError():
    return '!E\r\n'

def getSystemInfo():
    return '!I\r\n'

def getVersionInfo():
    return '!V\r\n'
