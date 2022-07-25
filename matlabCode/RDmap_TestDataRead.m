clear all
close all
clc

[radarPar,radarData] = simpleDataRead('giulioCammina.json');

zp = 4;
windowSize = 64;
nPlots = floor(radarPar.nFrame/windowSize);

window = true;
if window
    Hn = hamming(radarPar.nSamples);
    Hm = hamming(windowSize);
else
    Hn = ones(radarPar.nSamples,1);
    Hm = ones(windowSize,1);
end

ham2D = repmat(Hn,1,windowSize).*repmat(Hm.',radarPar.nSamples,1);
HP_filter = [1 -2 1];
filteredData = filter(HP_filter,1,radarData,[],1);

% for index = 1:nPlots
%     data = radarData(:,(index-1)*windowSize+1:index*windowSize).*ham2D;
%     tempRangeCompressed = ifft(data,zp*radarPar.nSamples,1);
%     RDmap(:,:,index) = fftshift(fft(tempRangeCompressed,zp*windowSize,2),2);
% %     imagesc(20*log10(abs(RDmap(1:end/2,:))))
% %     colormap hot
% %     colorbar
% end
% 
% implay(abs(RDmap),10)

lambda = 0.25; %2.5 mm, 0.25 cm
maxRange = ((radarPar.nSamples + 37.5)*3e8)/(4*radarPar.Bandwidth*1e6);
maxVel = lambda/(4*radarPar.PRI);

rangeVec = 0:maxRange/(zp*radarPar.nSamples/2):maxRange - maxRange/(zp*radarPar.nSamples);
velVec = -maxVel:2*maxVel/(zp*windowSize):maxVel - maxVel/(zp*windowSize);
[V,R] = meshgrid(velVec,rangeVec);

figure(1)
tiledlayout(2,1)
for index = 1:nPlots
    data = filteredData(:,(index-1)*windowSize+1:index*windowSize).*ham2D;
    tempRangeCompressed = ifft(data,zp*radarPar.nSamples,1);
    RDmap = fftshift(fft(tempRangeCompressed,zp*windowSize,2),2);
    nexttile(1)
    imagesc(velVec,rangeVec,abs(RDmap(1:end/2,:)))
    %imagesc(velVec,rangeVec,20*log10(abs(RDmap)))
    ylim([0 maxRange])
    xlim([-maxVel maxVel])
    ylabel('Range [m]')
    xlabel('Speed [cm/s]')
    nexttile(2)
    surf(V,R,abs(RDmap(1:end/2,:)))
    %surf(V,R,20*log10(abs(RDmap)))
    shading flat
    view(30,60)
    ylim([0 maxRange])
    xlim([-maxVel maxVel])
    ylabel('Range [m]')
    xlabel('Speed [cm/s]')
    colormap hot
    hcb = colorbar;
    hcb.Label.String = "Amplitude [linear]";
    hcb.Layout.Tile = 'east';
    titleStr = ['Elapsed time = ', num2str(index*windowSize*radarPar.PRI), 's'];
    sgtitle(titleStr)
    pause(windowSize*radarPar.PRI)
end
