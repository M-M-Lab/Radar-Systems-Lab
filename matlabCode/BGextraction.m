bg=[];
for i=1:60
    nome=strcat('data_2022_12_1_18_49_',string(i),'.mat');
    if isfile(nome)
        close all
        load(nome)
        R=real(complexData);
        Q=imag(complexData*exp(1i));
        plot(R)
        hold on
        plot(Q)
        plot(mean([R;Q],1))
        pause
    end
end

%media nel tempo
nfft=1024;

bgM=mean(bg,1);
BG=fftshift(fft(bgM,nfft));

plot(log10(abs(BG(end/2+1:end))))
grid on

hold on

BG=(BG(end/2+1:end)+flip(BG(1:end/2)))/2;
plot(log10(abs(BG)))
grid on

hold on

bgM=mean(bg,1);
BG=fftshift(fft(abs(bgM),nfft));
BG=BG(end/2+1:end);
plot(log10(abs(BG)))
grid on
