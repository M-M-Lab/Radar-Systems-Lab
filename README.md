# EVALKIT SiRad Simple® Python GUI
[![made-for-VSCode](https://img.shields.io/badge/Made%20for-VSCode-1f425f.svg)](https://code.visualstudio.com/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)
[![Generic badge](https://img.shields.io/badge/siRad%20Simple%20firmware-1.4.4-green.svg)](https://siliconradar.com/wp/)

**Python library for [EVALKIT SiRad Simple®](https://siliconradar.com/evalkits/).**

This code has been wrote for laboratory's activities during the **Radar Systems** class, within the **Master Degree in Telecommunication Engineering** at **University of Pisa**.

~~:fire: MATLAB implementation coming soon :fire:~~

## TO-DO-LIST - Radar Board commands and control
 - [x] Conversion from string of bit to string of hex to write the commands
 - [x] Set bandwidth
 - [x] Search for the proper serial device
 - [x] Set Self Trigger Delay
 - [x] Added system configuration handler
 - [x] Added baseband configuration handler
 - [x] Added short commands
 - [x] Modified baseband configuration handler: added controls over downsampling, number of ramps per frame and number of samples per frame
 - [x] Modified baseband configuration handler: add control over ADC ClkDiv
 - [ ] Other control functions

> **Note**: a lot of settings of above functions are still hardcoded.

## TO-DO-LIST - GUI
 - [x] Create main, radar and processor module
 - [x] Bandwidth, Gain, Samples and Ramps configuration 
 - [ ] Improve code readability and add comments
 - [ ] Add selector to switch between spectrum and RDMap
 - [ ] Add processing options ( windowing selection, low-pass and high-pass filtering, peak detection ..)
 - [ ] Finalize base radar settings
 - [ ] Remove timer from GUI and trigger update using Queue signaling
 - [ ] Add "max hold" function 
 - [ ] Add grid to plot
 
 ## TO-DO-LIST - MATLAB implementation
 - [x] 2D CFAR detector
 - [ ] MATLAB GUI?
 - [x] Update the README.md about the MATLAB code with the useful information regarding the data format of the .json files


## Anaconda usage
```console

lab-radar@labradar-Precision-T1500:~$ conda env create -f SiliconRadar_Env.yml

```

## Citation
If you use this software, please cite it as below.
```
@software{Mancuso_Radar_System_Laboratory_2022,
 author = {Mancuso, Francesco and Meucci, Giulio},
 month = {11},
 title = {{Radar System Laboratory}},
 version = {1.0.0},
 year = {2022}
}
```
## Authors
Giulio Meucci \
[Francesco Mancuso](https://mandugo.github.io)
