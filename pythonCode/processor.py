import numpy as np


def process(radar2processor_dataQ,processor2GUI_dataQ,GUI2processor_controlQ):

    hamming=[]

    while True:
        buf=radar2processor_dataQ.get()
        buf=buf.split('\t')
        ID=buf[1]
        buffSize=int(buf[2])/2
        data=np.int16(buf[3:])
        dataI=data[0::2]
        dataQ=data[1::2]
        
        complexData=dataI+1j*dataQ
        
        if len(hamming)!=buffSize:
            hamming=np.hamming(buffSize)

        complexData=complexData*hamming
        C=np.fft.fftshift(np.fft.fft(complexData))
        C=np.log10(np.abs(C))


        #print('Proc Q', processor2GUI_dataQ.qsize())
        processor2GUI_dataQ.put(C)


