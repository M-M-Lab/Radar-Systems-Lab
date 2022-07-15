# Laboratorio-SiliconRadar
[![made-for-VSCode](https://img.shields.io/badge/Made%20for-VSCode-1f425f.svg)](https://code.visualstudio.com/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)
[![Generic badge](https://img.shields.io/badge/siRad%20Simple%20firmware-1.4.4-green.svg)](https://siliconradar.com/wp/)


Python library for [EVALKIT SiRad Simple®](https://siliconradar.com/evalkits/).

:fire: MATLAB implementation coming soon :fire:

## TO-DO-LIST - Radar Board commands and control
 - [x] Conversion from string of bit to string of hex to write the commands
 - [x] Set bandwidth
 - [x] Search for the proper serial device
 - [x] Set Self Trigger Delay
 - [x] Added system configuration handler
 - [x] Added baseband configuration handler
 - [x] Added short commands
 - [x] Modified baseband configuration handler: added controls over downsampling, number of ramps per frame and number of samples per frame
 - [ ] Modified baseband configuration handler: add control over ADC ClkDiv
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

## Authors
Giulio Meucci \
Francesco Mancuso

## 
> Written with [StackEdit](https://stackedit.io/), [ForTheBadge](https://forthebadge.com/) and [Markdown Badges](https://github.com/Ileriayo/markdown-badges)
