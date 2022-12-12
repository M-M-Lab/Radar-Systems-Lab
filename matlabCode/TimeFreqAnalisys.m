clearvars 
close all
clc

%% Setting dei parametri
zp=4;

windowSize=128;

blindCells=64;

f0=122e9;

c=3e8;

omega=2*pi/75;  %Velocità angolare del tavolo rotante

load('cubo.mat')

%% Inizializzazione

radarData=data.data.';

nPlots=size(radarData,2)-windowSize;

PRF=1/mean(diff(data.tStamp));

lambda=c/f0;

Hn=hamming(data.Samps);

windowedData=radarData.*Hn;

%% Filtri

%filteredData = filter([1 -1],1,windowedData,[],1);
%filteredData=highpass(windowedData,0.35,'Steepness',0.9);
%filteredData=bandpass(windowedData,[0.5,0.95]);
%filteredData=highpass(windowedData.',0.05,'Steepness',0.9).';
filteredData=windowedData;

%% Costruzione dello spettrogramma

SPgram=zeros(zp*windowSize,nPlots);

rangeProfiles=fft(filteredData,zp*data.Samps);

for index = 1:nPlots

    winRangeProfiles=rangeProfiles(:,index:index+windowSize-1);

    RDmap=fft(winRangeProfiles,zp*windowSize,2);

    RDmap=fftshift(RDmap,2);

    RDmap=RDmap(blindCells:end/2,:);

    strip=max(abs(RDmap),[],1);

    SPgram(:,index)=strip./max(strip,[],'all');

end

fd=linspace(-PRF/2,PRF/2,size(SPgram,1));
tVect=linspace(0,nPlots/PRF,size(SPgram,2));

figure(1)
imagesc(tVect,fd,log10(abs(SPgram)))
colorbar
xlabel('Time [s]')
ylabel('Doppler Frequency [Hz]')
clim([-0.5 0])


%% Inverse Radon Transform

angoli=linspace(0,360,nPlots);
iRad=abs(iradon(SPgram,angoli,size(SPgram,1)));

xVect=fd*lambda/(2*omega);
yVect=fd*lambda/(2*omega);

figure(3)
imagesc(xVect,yVect,iRad)
colorbar
title('IRT')

