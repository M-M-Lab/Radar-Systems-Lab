clear all
close all
fclose('all');
clc

fprintf("\nRetrieving port ...\n")
pause(0.5);
sPort = serialportlist;
baudRate = 1e6;

fprintf("Connecting to %s ...\n",sPort)
com_port = serialport(sPort(2),baudRate);
set(com_port, "DataBits", 8);
set(com_port, "Parity", 'none');
set(com_port, "StopBits", 1);
set(com_port, "Timeout", 1);
configureTerminator(com_port,'CR/LF');

pause(0.5);
fprintf("\nSetting the radar ...\n")

writeline(com_port,"!S08021012")
writeline(com_port,"!K")
writeline(com_port,"!B20000008")    %1 rampa, 64 campioni

pause(0.5);
fprintf("Acquiring data ...\n")

not_terminated = 1;
win = hamming(64).';
% 
% writeline(com_port, "!L");  % Easy
% buf = readline(com_port)

nfft = 512;

lambda = 0.25; %2.5 mm, 0.25 cm
maxRange = ((64 + 37.5)*3e8)/(4*6100*1e6);

rangeVec = 0:maxRange/256:maxRange - maxRange/512;

h = plot(ones(1,nfft));
set(h,'XData',rangeVec);
grid on
phaseVec = [];

[FILTERED,phil] = highpass(ones(1,64),0.2);

while not_terminated
    buf = '';
    while isempty(buf) || ~startsWith(buf,'!M')
        buf = readline(com_port);
    end
    % convert to string
    frameM = split(buf);
    frameM = frameM(4:end);
    
    % replace all delimiters and optional sign chars before conversion
    % to numbers
    
    %dataM = double(int16(str2num(char(frameM))));
    dataM = str2double(frameM);
    dataI = dataM(1:2:end-1);
    dataQ = dataM(2:2:end);
    
    complexData = (dataI+1i*dataQ)'; %Trasposta per ritornare un vettore riga

%     HP_filter = [1 -1];
%     filteredData = filter(HP_filter,1,complexData,[],2);
    FILTERED = filter(phil,complexData);
    %plot(abs(fft(complexData,128)))
    if length(FILTERED) == 64
        rangeProfile = fft(FILTERED.*win,nfft);
        set(h,'YData',abs(rangeProfile(1:end/2)));
    end
    
    phaseVec = [phaseVec, angle(max(rangeProfile))];


end




