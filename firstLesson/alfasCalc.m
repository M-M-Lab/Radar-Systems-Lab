function [alfaGO,alfaSO] = alfasCalc(N,pFA)
    alfa_vect = 0:0.01:10;
    eCell = round(N/2);
    pFA_GO = zeros(1,length(alfa_vect));
    pFA_SO = zeros(1,length(alfa_vect));
    for tt = 1:length(alfa_vect)
        tempGO = 0;
        tempSO = 0;
        for jj = 0:eCell - 1
            tempGO = tempGO + nchoosek(eCell + jj - 1,jj)*(2 + alfa_vect(tt))^(-eCell - jj);
            tempSO = tempSO + nchoosek(eCell + jj - 1,jj)*(2 + alfa_vect(tt))^(-jj);
        end
        pFA_GO(tt) = 2*(1 + alfa_vect(tt))^(-eCell) - 2*tempGO;
        pFA_SO(tt) = 2*((2 + alfa_vect(tt))^(-eCell))*tempSO;
    end
    [~,iGO] = min(abs(pFA_GO - pFA));
    [~,iSO] = min(abs(pFA_SO - pFA));
    alfaGO = alfa_vect(iGO);
    alfaSO = alfa_vect(iSO);
end