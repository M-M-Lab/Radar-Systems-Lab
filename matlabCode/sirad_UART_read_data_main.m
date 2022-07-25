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
%disp("Set COM port options: 230400baud, 8 bit, 1 stop, no parity, read timeout 3s...");
set(com_port, "BaudRate", 1e6);
%set(com_port, "baudrate", 1000000);
set(com_port, "DataBits", 8);
set(com_port, "Parity", 'none');
set(com_port, "StopBits", 1);
%set(com_port, 'requesttosend', 'off');
%set(com_port, 'dataterminalready', 'off');
set(com_port, "Timeout", 1);
configureTerminator(com_port,'CR/LF')

% optional flush of input and output buffers
pause(0.5);
flush(com_port);

% activate external trigger mode on device
pause(0.5);
disp("Configure device to external trigger mode...");
disp("Configure RAW data output...");

%writeline(com_port, "!S01129810")  % Simple
writeline(com_port,"!S08029010")

pause(0.5);
flush(com_port);
  
%writeline(com_port, "!B00000000"); %1 rampa 32 campioni
%writeline(com_port, "!B000001D0"); %128 rampe %128 campioni
%writeline(com_port, "!B00000190"); %64 rampe %128 campioni
%writeline(com_port, "!B00000197"); %64 rampe %128 campioni (con clk divider basso, più lento)
%writeline(com_port, "!B00000090"); %4 rampe %128 campioni
%writeline(com_port,"!B00000048")    %2 rampe, 64 campioni
%writeline(com_port,"!B00000008")    %1 rampa, 64 campioni
%writeline(com_port, "!B00000080"); %4 rampe %32 campioni
writeline(com_port,"!B200001D8") %128, 256
writeline(com_port,'!B200001D0') %128, 128
writeline(com_port,'!B20000150') %32, 128

%srl_write(com_port, ["!BB034C125\r\n"]);  % 120000 MHz
pause(0.1);
flush(com_port);

% configure front end and PLL
%writeline(com_port, "!F00075300");  % 120000 MHz
pause(0.1);
%flush(com_port);
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
win=hamming(128);
while (not_terminated)
  % if not terminated, process data
  tmp=sirad_UART_read_data_M_frame(com_port, 2*ADCsamples);
  %tmp=diff(tmp);
  RDMap=[RDMap;tmp.*win'];
  if size(RDMap,1)>=8
      A=fftshift(fft2(RDMap),1);
      %A(end/2:end/2+1,:)=1;
        imagesc(log10(abs(A(:,1:end/2))))
        colorbar
        RDMap=[];
        %not_terminated=0;
  end
end

% close port
disp("Close COM port...");
fclose(com_port);
disp("Done. Exit.");




