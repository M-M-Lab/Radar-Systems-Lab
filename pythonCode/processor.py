import numpy as np
import time
import struct
import json
import scipy
import array

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
                    fileName='../dump/dump_'+date.replace(':','')+'.mat'
                else:       #Dump to file
                    f = open(fileName, 'a')
                    dataDict['data']=listOfFrame
                    dataDict['tStamp']=listOfTStamp
                    scipy.io.savemat(fileName,{'data': dataDict})                    
                    #json.dump(dataDict,f)
                    f.close()
                    dump2File=False


        complexData=np.zeros(buffSize)                                     #Maybe useless!!!

        #Weighting window definition
        if len(hamming)!=buffSize:
            hammingCol=np.hamming(buffSize)
            hammingRow=np.hamming(NSweepIntegration)
            hamming=hammingCol[:,np.newaxis]*hammingRow[np.newaxis,:]

        RDMap=np.zeros((int(buffSize),NSweepIntegration),dtype=np.complex)  #Maybe useless!!!

        #startTime=time.time()
        tStamp=np.zeros((NSweepIntegration,1))
        for ind in range(NSweepIntegration):
            buf,tStamp[ind]=radar2processor_dataQ.get()
            #buffSize=int(int.from_bytes(buf[7:8],"big")/2)
            try: #if len(buf[9:-2])>=2*buffSize:
                #New  TOTEST
                short_array = np.array(array.array('h', buf[9:-2]))
                complexData=short_array[:2*buffSize:2]+1j*short_array[1:2*buffSize:2]  
                #buf=struct.iter_unpack('<h',buf[9:-2])
                #buf=[val[0] for val in buf]
                #dataI=np.array(buf[0:2*buffSize:2])
                #dataQ=np.array(buf[1:2*buffSize:2])
                #complexData=dataI+1j*dataQ
                if dump2File:
                    listOfFrame.append(complexData.tolist())
                    listOfTStamp.append(tStamp[ind])
                RDMap[:,ind]=complexData
            except:
                pass
        PRI=np.mean(np.diff(tStamp,1,0))
        
        #Hamming
        RDMap=RDMap*hamming
        
        #FFT (TODO: implement zeropadding selector)
        RangeMap=np.fft.fft(RDMap,2*buffSize,axis=0)
        C=np.fft.fftshift(np.fft.fft(RangeMap,NSweepIntegration*4,axis=1),1)
        
        #Cut RDMap in half
        C=C[int(buffSize):,:]
        try:
            C[C == 0] = np.min(C[C != 0]) #MODIFIED -> = 1 [rimuove gli zeri per evitare problemi con la np.log10(.)]
            C=np.log10(np.abs(C))
        except:
            pass
        #print('Proc Q', processor2GUI_dataQ.qsize()) #Debug, mostra la lunghezza della coda tra processore e interfaccia grafica
        processor2GUI_dataQ.put((C,PRI))
