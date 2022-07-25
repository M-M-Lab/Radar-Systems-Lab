% Copyright (c) 2014, Petri Väisänen 
% All rights reserved.
%
% Redistribution and use in source and binary forms, with or without 
% modification, are permitted provided that the following conditions are 
% met:
%
% Redistributions of source code must retain the above copyright 
% notice, this list of conditions and the following disclaimer. 
% Redistributions in binary form must reproduce the above copyright 
% notice, this list of conditions and the following disclaimer in 
% the documentation and/or other materials provided with the distribution
%
% THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
% AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
% IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
% ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
% LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
% CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
% SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
% INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
% CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
% ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
% POSSIBILITY OF SUCH DAMAGE.
%
% code source:
% https://de.mathworks.com/matlabcentral/fileexchange/47002-shex2dec-m#license_modal

function d = shex2dec(h)
%SHEX2DEC Convert hexadecimal string to decimal integer.
%   D = SHEX2DEC(H) interprets the hexadecimal string H and returns in D the
%   equivalent decimal number.  
%  
%   If H is a character array or cell array of strings, each row is interpreted
%   as a hexadecimal string. 
%
%   EXAMPLES:
%       shex2dec('FFFFFF2B') and shex2dec('f2b') both return -213
%
%   See also HEX2DEC, DEC2HEX, HEX2NUM, BIN2DEC, BASE2DEC.

%   Modified from the HEX2DEC by MathWorks, Inc.

  if iscellstr(h), h = char(h); end
  if isempty(h), d = []; return, end

  % Work in upper case.
  h = upper(h);

  [m,n]=size(h);

  % Right justify strings and form 2-D character array.
  if ~isempty(find((h==' ' | h==0),1))
    h = strjust(h);
    % Replace any leading blanks and nulls by 0.
    h(cumsum(h ~= ' ' & h ~= 0,2) == 0) = '0';
  else
    h = reshape(h,m,n);
  end

  sixteen = 16;
  p = fliplr(cumprod([1 sixteen(ones(1,n-1))]));
  p = p(ones(m,1),:);

  d = h <= 64; % Numbers
  h(d) = h(d) - 48;

  d =  h > 64; % Letters
  h(d) = h(d) - 55;

  d = sum(h.*p,2);

  % MOD: Handle negative numbers by substracting the most positive
  d(d>(16^n)/2) = d(d>(16^n)/2) - 16^n;
  % modification: added endfunction to original code from author
end
