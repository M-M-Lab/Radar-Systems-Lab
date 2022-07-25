# MATLAB code description

The two `.json` files contain some data acquired by using the Python GUI. Besides I and Q data, they contain the radar parameter used for the acquisition:
``` 
{ "Bandwidth": 6000,
   "SamplingFrequency": 2.571,
   "Ramps": 1, 
   "Samps": 32, 
   "PRI": "0.01577", 
   "Gain": 8, 
   "data": [...] 
 }
 ``` 
 **Bandwidth** and **SamplingFrequency** are MHz, **PRI** is measured in seconds and **Gain** is in dB.
 
`JSON.m` is a [JSON parser](https://it.mathworks.com/matlabcentral/fileexchange/42236-parse-json-text?s_tid=mwa_osa_a), used in `simpleDataRead.m` to properly read and parse the data acquired by the Python GUI. The function `simpleDataRead.m` takes as input the name of the data file and it returns a matrix containing the data and a structure with the radar parameters, for example:
```
[radarPar,radarData] = simpleDataRead('giulioCammina.json)
```
The matrix `radarData` will have a number of rows equal to the number of samples and a number of columns equal to the number of acquired frames (i.e., the range profiles ara arranged along the columns).

##
The script `RDmap_TestDataRead.m` does an high pass filtering on the data, by using a simple 3-pulse canceller along range profiles, followed by a windowing, by using an Hamming window, and plots the Range-Doppler map using a sliding window that goes through the acquired frames, providing a sort of live Range-Doppler map. The dimension of the sliding window can be adjusted.
 
 ## References
  - Joe Hicklin (2022). Parse JSON text (https://www.mathworks.com/matlabcentral/fileexchange/42236-parse-json-text), MATLAB Central File Exchange. Retrieved July 25, 2022.
