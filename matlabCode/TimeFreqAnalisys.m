clearvars 
close all
clc

%% Setting dei parametri
zp = 4;

windowSize = 128;

blindCells=64;

lambda = 0.25; %2.5 mm, 0.25 cm

%% Inizializzazione

load('rotante120.mat')

radarData=data.data(3:end,:).';

nPlots = size(radarData,2)-windowSize;

PRI=max(diff(data.tStamp));

Hn = hamming(data.Samps);

windowedData=radarData.*Hn;

%% Filtri

%filteredData = filter([1 -1],1,windowedData,[],1);
%filteredData=highpass(windowedData,0.35,'Steepness',0.9);
%filteredData=bandpass(windowedData,[0.5,0.95]);
%filteredData=highpass(windowedData.',0.05,'Steepness',0.9).';


%% Costruzione dello spettrogramma

SPgram=zeros(zp*windowSize,nPlots);

rangeProfiles=fft(filteredData,zp*data.Samps);

for index = 1:nPlots

    winRangeProfiles = rangeProfiles(:,index:index+windowSize-1);

    RDmap=fft(winRangeProfiles,zp*windowSize,2);

    RDmap = fftshift(RDmap,2);

    RDmap=RDmap(blindCells:end/2,:);

    strip=mean(abs(RDmap),1);

    SPgram(:,index)=strip./max(strip,[],'all');

end

maxRange = ((data.Samps + 37.5)*3e8)/(4*data.Bandwidth*1e6);
maxVel = lambda/(4*str2num(data.PRI));

rangeVec = 0:maxRange/(zp*data.Samps/2):maxRange - maxRange/(zp*data.Samps);
velVec = -maxVel:2*maxVel/(zp*windowSize):maxVel - maxVel/(zp*windowSize);
[V,R] = meshgrid(velVec,rangeVec);



figure(1)
imagesc([],velVec,log10(abs(SPgram)))
colorbar
clim([-1.5 0])



omega=2*pi/75;
angoli=linspace(0,360,size(SPgram,2));
iRad=abs(iradon(SPgram,angoli,size(RDmap,2)));
f=linspace(-1/(2*str2num(data.PRI)),1/(2*str2num(data.PRI)),size(RDmap,2));

lambda=3e10/120e9;
xVect=f*lambda/(2*omega);

yVect=f*lambda/(2*omega);
figure(3)
imagesc(xVect,yVect,iRad)
colorbar


