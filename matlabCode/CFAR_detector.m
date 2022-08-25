clear all
close all
clc

[radarPar,radarData] = simpleDataRead('giulioCammina.json');

zp = 4;
windowSize = 32;
nPlots = floor(radarPar.nFrame/windowSize) + floor(radarPar.nFrame/windowSize) - 1;

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


% CFAR detector ------------
detector = phased.CFARDetector2D('TrainingBandSize',[9,9], ...
    'GuardBandSize',[9,7], ...
    'Method','GOCA', ...
    'ProbabilityFalseAlarm',1e-3);

Ngc = detector.GuardBandSize(2);
Ngr = detector.GuardBandSize(1);
Ntc = detector.TrainingBandSize(2);
Ntr = detector.TrainingBandSize(1);
cutidx = [];
colstart = Ntc + Ngc + 1;
colend = zp*windowSize - (Ntc + Ngc);
rowstart = Ntr + Ngr + 1;
rowend = zp*radarPar.nSamples/2 - (Ntr + Ngr);
for m = colstart:colend
    for n = rowstart:rowend
        cutidx = [cutidx,[n;m]];
    end
end
ncutcells = size(cutidx,2);
% -----------------------

lambda = 0.25; %2.5 mm, 0.25 cm
maxRange = ((radarPar.nSamples + 37.5)*3e8)/(4*radarPar.Bandwidth*1e6);
maxVel = lambda/(4*radarPar.PRI);

rangeVec = 0:maxRange/(zp*radarPar.nSamples/2):maxRange - maxRange/(zp*radarPar.nSamples);
velVec = -maxVel:2*maxVel/(zp*windowSize):maxVel - maxVel/(zp*windowSize);
[V,R] = meshgrid(velVec,rangeVec);

figure('Units','normalized','Position',[0 0 1 1])
tiledlayout(2,2)
for index = 1:nPlots
    data = filteredData(:,((index-1)*(windowSize/2))+1:(((index-1)/2) + 1)*windowSize).*ham2D;
    tempRangeCompressed = ifft(data,zp*radarPar.nSamples,1);
    RDmap = fftshift(fft(tempRangeCompressed,zp*windowSize,2),2);

    dets = detector(abs(RDmap(1:end/2,:)),cutidx);

    nexttile(1);
    imagesc(velVec,rangeVec,abs(RDmap(1:end/2,:)))
    %imagesc(velVec,rangeVec,20*log10(abs(RDmap)))
    ylim([0 maxRange])
    xlim([-maxVel maxVel])
    ylabel('Range [m]')
    xlabel('Speed [cm/s]')
    
    nexttile(2);
    surf(V,R,abs(RDmap(1:end/2,:)))
    %surf(V,R,20*log10(abs(RDmap)))
    shading flat
    view(30,60)
    ylim([0 maxRange])
    xlim([-maxVel maxVel])
    ylabel('Range [m]')
    xlabel('Speed [cm/s]')
    colormap hot
%     hcb = colorbar;
%     hcb.Label.String = "Amplitude [linear]";
%     hcb.Layout.Tile = 'east';
    
    
    detimg = zeros(zp*radarPar.nSamples/2,zp*windowSize);
    for k = 1:ncutcells
        detimg(cutidx(1,k),cutidx(2,k)) = dets(k);
    end
    nexttile(3);
    imagesc(detimg)
    title("CFAR detection")
    set(gca,'xticklabel',[])
    set(gca,'yticklabel',[])
    
    targetPoint = regionprops(detimg,'centroid');
    if ~isempty(targetPoint)
        nexttile(4);
        plot(targetPoint.Centroid(1),targetPoint.Centroid(2),'ro')
        hold on
        grid on
        axis([1 128 0 64])
        set(gca, 'YDir','reverse')
        title("CFAR detection centroid")
        set(gca,'xticklabel',[])
        set(gca,'yticklabel',[])
    end

    titleStr = ['Elapsed time = ', num2str(index*(windowSize/2)*radarPar.PRI), 's'];
    sgtitle(titleStr)
    pause((windowSize/2)*radarPar.PRI)
end
