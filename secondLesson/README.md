# Second Radar System Laboratory Lesson - 06/12/2022
### A.A. 2022/2023

- The folder `/data` contains a couple of `.mat` files used for the live scripts;
- The function `alfasCalc.m` is needed to obtain the SO and GO CFAR coefficients. They can't be evaluated in a closed form, thus that function calculates them explicitely and looks for the value that is closer to the desired $P_{FA}$.\
Usage: `[alfaGO,alfaSO] = alfasCalc(N,pFA)`, where *N* is the size of the reference window (leading + lagging) and *pFA* is the desired false alarm probability;


> **Warning**\
> If the reference window of the CFAR is too big, the MATLAB method `nchoosek()` - within the function `alfasCalc.m` - may fail.

## References
**[1]** James A. Scheer, James L. Kurtz (editors). “Coherent Radar Performance Estimation”. Boston: Artech House (1993), ISBN 0-89006-628-0.\
**[2]** Richards, M.A. and Scheer, J.A. and Scheer, J. and Holm, W.A. "Principles of Modern Radar: Basic Principles, Volume 1". Institution of Engineering and Technology (2010), ISBN 9781891121524
