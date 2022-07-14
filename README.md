# Laboratorio-SiliconRadar
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
