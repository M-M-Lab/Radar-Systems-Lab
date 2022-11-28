# First Radar System Laboratory Lesson - 29/11/2022
## A.A. 2022/2023

- The folder `/data` contains a couple of `.mat` files used for the live scripts;
- The function `alfasCalc.m` is needed to obtain the SO and GO CFAR coefficients. They can't be evaluated in a closed form, thus that function calculates them explicitely and looks for the value that is closer to the desired $P_{FA}$. Usage: `[alfaGO,alfaSO] = alfasCalc(N,pFA)`, where *N* is the size of the reference window (leading + lagging) and *pFA* is the desired false alarm probability;
