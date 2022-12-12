clearvars
close all
clc

%% Setting dei parametri
c=3e8;

f0=122e9;

load('rotante200.mat')

PRF=1/mean(diff(data.tStamp));

rawData=(data.data(10:end-10,:));

nfft=2.^(nextpow2(size(rawData))+2);

%% Pulizia del dato

windowedData=rawData.*hamming(size(rawData,2))'.*hamming(size(rawData,1));

filteredData=highpass(windowedData.',0.25,'Steepness',0.9).';

%% Range Doppler Map

RD=fft2(filteredData,nfft(1),nfft(2));

RD=fftshift(RD,1);

RD=RD(:,1:end/2);


%% Scaling degli assi
fd=linspace(-PRF/2,PRF/2,size(RD,1));
vVect=fd*c/(2*f0);

maxRange = ((data.Samps + 37.5)*3e8)/(4*data.Bandwidth*1e6);
rVect=linspace(0,maxRange,size(RD,2));
imagesc(rVect,vVect,10*log10(abs(RD)))
colormap('hot')
colorbar
title('Range Doppler Map')
