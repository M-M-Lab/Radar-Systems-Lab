import numpy as np
import time
import struct
import json

def process(radar2processor_dataQ,processor2GUI_dataQ,GUI2processor_controlQ):

    NSweepIntegration=16
    dump2File=False
    hamming=[]
    time.sleep(0.5)
    while True:
        while GUI2processor_controlQ.qsize():
            key,value=GUI2processor_controlQ.get()
            if key=='Samps':
                buffSize=int(value)
            elif key=='Dump':
                if value:
                    #Init recording
                    dataDict=value #??
                    dump2File=True
                    listOfFrame=[]
                    listOfTStamp=[]
                    #Create name for dump file with timestamp
                    date=time.asctime()
                    date=date.replace(' ','_')
                    fileName='../dump/dump_'+date.replace(':','')+'.json'
                else:
                    f = open(fileName, 'a')
                    dataDict['data']=listOfFrame
                    dataDict['tStamp']=listOfTStamp
                    json.dump(dataDict,f)
                    f.close()
                    dump2File=False


        complexData=np.zeros(buffSize)

        if len(hamming)!=buffSize:
            hammingCol=np.hamming(buffSize)
            hammingRow=np.hamming(NSweepIntegration)
            hamming=hammingCol[:,np.newaxis]*hammingRow[np.newaxis,:]

        RDMap=np.zeros((int(buffSize),NSweepIntegration),dtype=np.complex)

        startTime=time.time()
        for ind in range(NSweepIntegration):
            buf,tStamp=radar2processor_dataQ.get()
            #buffSize=int(int.from_bytes(buf[7:8],"big")/2)
            if len(buf[9:-2])>=2*buffSize:    
                buf=struct.iter_unpack('<h',buf[9:-2])
                buf=[val[0] for val in buf]
                dataI=np.array(buf[0:2*buffSize:2])
                dataQ=np.array(buf[1:2*buffSize:2])
                complexData=dataI+1j*dataQ
                if dump2File:
                    listOfFrame.append(buf)
                    listOfTStamp.append(tStamp)
                #complexData=complexData-np.mean(complexData)
            RDMap[:,ind]=complexData
        PRI=(time.time()-startTime)/NSweepIntegration
        
        #Hamming
        RDMap=RDMap*hamming
        
        #FFT 1
        RangeMap=np.fft.fft(RDMap,2*buffSize,axis=0)
        #rowPhase=np.exp(1j*np.mean(np.angle(RangeMap),0))
        #colPhase=np.exp(1j*np.mean(np.angle(RangeMap),1))
        #meanPhaseMat=rowPhase[np.newaxis,:]*colPhase[:,np.newaxis]
        #RangeMap=RangeMap*np.conj(meanPhaseMat)#*np.conj(colPhase[:,np.newaxis])
        C=np.fft.fftshift(np.fft.fft(RangeMap,NSweepIntegration*4,axis=1),1)
        
        #FFT 2
        #C=np.fft.fftshift(np.fft.fft2(RDMap),1)
        
        #Cut RDMap in half
        C=C[int(buffSize):,:]
        C[C == 0] = np.min(C[C != 0]) #MODIFIED -> = 1
        C=np.log10(np.abs(C))
        
        #print('Proc Q', processor2GUI_dataQ.qsize())
        processor2GUI_dataQ.put((C,PRI))
