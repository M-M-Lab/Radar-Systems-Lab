% ---------------------------------------------------------------------------
%                           CLEAR ENVIRONEMNT
% ---------------------------------------------------------------------------
clear;
close all;
fclose('all');

% ---------------------------------------------------------------------------
%                             USER SETTINGS
% ---------------------------------------------------------------------------

% set Serial Port (modify number after "COM")
com_port_string = "COM27";
% used Eval Kit (SiRad Easy or SiRad Simple, choose one)
useEasy = 0;
useSimple = 1;
% set desired number of samples (128, 256, 512, 1024, 2048)
ADCsamples = 128;
% set number of ramps for measurement (1, 2, 4, 8, 16, 32, 64, 128)
ramps = 1;

% ---------------------------------------------------------------------------
%                            RAW DATA VIEWER
% ---------------------------------------------------------------------------
%page_output_immediately (1);
%page_screen_output (0);

disp(" -------------------------------------------------------------");
disp("|                SILICON RADAR RAW DATA VIEWER                |");
disp(" -------------------------------------------------------------");
disp(["Connect to " com_port_string "."]);
disp("Please modify script if neccessary.");
disp("PRESS KEY TO START / STOP");

% open com port
%com_port = serialport(["\\\\.\\" com_port_string]);
com_port = serialport("/dev/ttyUSB0", 1e6);
%pause(1);
pause(0.5);

% set com port parameters
%disp("SetCOM port options: 230400baud, 8 bit, 1 stop, no parity, read timeout 3s...");
set(com_port, "BaudRate", 1e6);
%set(com_port, "baudrate", 230400);
set(com_port, "DataBits", 8);
%set(com_port,"ByteOrder",'big-endian')
set(com_port, "Parity", 'none');
set(com_port, "StopBits",1);
%set(com_port, 'requesttosend', 'off');
%set(com_port, 'dataterminalready', 'off');
set(com_port, "Timeout", 10);
configureTerminator(com_port,'CR/LF')

% optional flush of input and output buffers
pause(0.5);
flush(com_port);

% activate external trigger mode on device
pause(0.5);
disp("Configure device to external trigger mode...");
disp("Configure RAW data output...");

%writeline(com_port, "!S01129810")  % Simple
%writeline(com_port,"!S08023010") % gain 41db
%writeline(com_port,"!S08021010") % 8 db
%writeline(com_port,"!S08023012") % prova nth
%writeline(com_port,"!S08033012") % nth+1
%writeline(com_port,"!S08021012") %agc off
%writeline(com_port,"!S08021010") %trigger external
%writeline(com_port,"!S08025010") %gain a 21 db
writeline(com_port,"!S08029010")
%writeline(com_port,"!S000049BA")    % webGUI

pause(0.4);
flush(com_port);
  

%writeline(com_port, "!B00000000"); %1 rampa 32 campioni
%writeline(com_port, "!B000001F0"); %128 rampe %2048 campioni
%writeline(com_port, "!B200001F0"); %128 rampe %2048 campioni
%writeline(com_port,"!B200001E0") %128, 512
writeline(com_port,"!B200001D8") %128, 256
%writeline(com_port, "!B000001A8"); %webGUI
%writeline(com_port, "!B000001B0"); %64 rampe %2048 campioni
%writeline(com_port,"!B000000F0") %8 rampe 2048 campioni
%writeline(com_port,"!B00000130") %4 rampe 2048 campioni
%writeline(com_port,"!B00000170") %32 rampe 2048 campioni
%writeline(com_port,"!B00000168") %32 rampe 1024 campioni
%writeline(com_port,"!B00000160") %32 rampe 512 campioni
%writeline(com_port,'!B20000160') %32 rampe, 512 campioni, DC corretion on
%writeline(com_port,"!B00000140") %32 rampe 32 campioni
%writeline(com_port,"!B00000188") %64 rampe 64 campioni
%writeline(com_port,"!B00000190") %64 rampe 128 campioni


pause(0.2);
flush(com_port);

%writeline(com_port,"!P000001F4") %1GHz
writeline(com_port,"!K")    %Set max BW
%writeline(com_port, "!P00000BB8"); % 5000 MHz 
%srl_write(com_port, ["!P00001770\r\n"]);  % 6000 MHz

% default settings from WebGUI
%!S011049BA
%!F0201D4C0
%!P00001388
%!BB034C125

pause(0.1);
flush(com_port);
  
disp("Done. Aquiring data...");
%flush(com_port);


% continue data processing from Serial Port while state "not terminated"
not_terminated = 1;
RDMap=[];
%win=hamming(128).*hamming(16)';
win=hamming(256)';
while (not_terminated)
  writeline(com_port, "!N");  % send trigge

  buf='';
  while ~startsWith(buf,'!M')
    buf = readline(com_port);
  end
  % convert to string
  frameM = split(buf);
  %frameM(1:10);
  frameM = frameM(4:end);

  dataM = double(int16(str2num(char(frameM))));
  dataI = dataM(1:2:end-1);
  dataQ = dataM(2:2:end);

  complexData=(dataI+1i*dataQ)';


  plot(log(abs(fftshift(fft(complexData.*win,2^12)))))
%   RDMap=reshape(complexData,128,[]).*win;
%   A=fftshift(fft2(RDMap,128*2,16*2),1);
%   %A(end/2:end/2+1,:)=1;
%   imagesc(log10(abs(A(:,1:end/2))))
%   %colorbar
end

% close port
disp("Close COM port...");
fclose(com_port);
disp("Done. Exit.");




