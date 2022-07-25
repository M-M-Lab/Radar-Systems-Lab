function [radarPar,radarData] = simpleDataRead(filename)

    fid = fopen(filename); 
    raw = fread(fid,inf); 
    str = char(raw'); 
    fclose(fid);
    % https://it.mathworks.com/matlabcentral/fileexchange/42236-parse-json-text?s_tid=mwa_osa_a
    data = JSON.parse(str);

    radarPar.Bandwidth = data.Bandwidth;
    radarPar.fs = data.SamplingFrequency;
    radarPar.nRamps = data.Ramps;
    radarPar.nSamples = data.Samps;
    radarPar.nFrame = length(data.data);
    radarPar.PRI = str2double(data.PRI);
    radarPar.gain = data.Gain;

    dataMatrix = zeros(radarPar.nFrame,2*radarPar.nSamples);
    for index = 1:radarPar.nFrame
        dataMatrix(index,:) = cell2mat(data.data{1,index});
    end
    
    dataMatrixI = dataMatrix(:,1:2:end-1);
    dataMatrixQ = dataMatrix(:,2:2:end);
    radarData = dataMatrixI.' + 1i*dataMatrixQ.';

end