import numpy as np
import time
import struct
import json

def process(radar2processor_dataQ,processor2GUI_dataQ,GUI2processor_controlQ):

    NSweepIntegration=16    #Numero di sweep su cui viene fatta la mappa RD
    
    #Init
    dump2File=False
    hamming=[]
    time.sleep(0.5)
    
    while True:
        while GUI2processor_controlQ.qsize():
            key,value=GUI2processor_controlQ.get()
            #Change buffer size depending on GUI queue 
            if key=='Samps':                            
                buffSize=int(value)
            
            #Save to file
            elif key=='Dump':
                if value:   #Init recording
                    dataDict=value #??
                    dump2File=True
                    listOfFrame=[]
                    listOfTStamp=[]

                    #Create name for dump file with timestamp
                    date=time.asctime()
                    date=date.replace(' ','_')
                    fileName='../dump/dump_'+date.replace(':','')+'.json'
                else:       #Dump to file
                    f = open(fileName, 'a')
                    dataDict['data']=listOfFrame
                    dataDict['tStamp']=listOfTStamp
                    json.dump(dataDict,f)
                    f.close()
                    dump2File=False


        complexData=np.zeros(buffSize)                                     #Maybe useless!!!

        #Weighting window definition
        if len(hamming)!=buffSize:
            hammingCol=np.hamming(buffSize)
            hammingRow=np.hamming(NSweepIntegration)
            hamming=hammingCol[:,np.newaxis]*hammingRow[np.newaxis,:]

        RDMap=np.zeros((int(buffSize),NSweepIntegration),dtype=np.complex)  #Maybe useless!!!

        startTime=time.time()
        for ind in range(NSweepIntegration):
            buf,tStamp=radar2processor_dataQ.get()
            if len(buf[9:-2])>=2*buffSize:    
                buf=struct.iter_unpack('<h',buf[9:-2])
                buf=[val[0] for val in buf]
                dataI=np.array(buf[0:2*buffSize:2])
                dataQ=np.array(buf[1:2*buffSize:2])
                complexData=dataI+1j*dataQ
                if dump2File:
                    listOfFrame.append(buf)
                    listOfTStamp.append(tStamp)
            RDMap[:,ind]=complexData
        PRI=(time.time()-startTime)/NSweepIntegration
        
        #Hamming
        RDMap=RDMap*hamming
        
        #FFT (TODO: implement zeropadding selector)
        RangeMap=np.fft.fft(RDMap,2*buffSize,axis=0)
        C=np.fft.fftshift(np.fft.fft(RangeMap,NSweepIntegration*4,axis=1),1)
        
        #Cut RDMap in half
        C=C[int(buffSize):,:]
        C[C == 0] = np.min(C[C != 0]) #MODIFIED -> = 1 [rimuove gli zeri per evitare problemi con la np.log10(.)]
        C=np.log10(np.abs(C))
        
        #print('Proc Q', processor2GUI_dataQ.qsize()) #Debug, mostra la lunghezza della coda tra processore e interfaccia grafica
        processor2GUI_dataQ.put((C,PRI))
