% 
% Reads, interprets, and displays the ADC raw data coming from the given 
% serial port.
%
% @param[in] com_port A serial port handle opened by serial().
% @param[in] autoscale Set to 1 to activate auto Y axis scaling.
%
function [complexData]= sirad_UART_read_data_M_frame(com_port, samples)
% frame format of M frame:
% !M0400/-FFED/0005/-FFF9/...|
% !: start marker
% M: ADC raw data frame marker
% 0400: number of samples, 4 chars
% /: data delimiter
% -: optional signed indicator
% FFED, 0005 and the like: data
% |: frame end delimiter
%
% one data point is:
% delimiter (/) + 4 chars data (FFED) + signed indicator (-) = max. 6 chars
% data to read: samples * 6 + 4 chars number of samples
  
  %pause(0.1);
  writeline(com_port, "!N");  % Easy
  flush(com_port);
  
  % read a big amount of chars to be sure we get the M frame and all of its
  % content, there are small frames sent before the M frame also, which are
  % not bigger than 100 chars altogether
  buf='';
  while ~startsWith(buf,'!M')
    buf = readline(com_port);
  end
  % convert to string
  frameM = split(buf);
  frameM = frameM(4:end);
  
  % replace all delimiters and optional sign chars before conversion
  % to numbers
  
  dataM = double(int16(str2num(char(frameM))));
  dataI = dataM(1:2:end-1);
  dataQ = dataM(2:2:end);

  complexData=(dataI+1i*dataQ)'; %Trasposta per ritornare un vettore riga
end
 