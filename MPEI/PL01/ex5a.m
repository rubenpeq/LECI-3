%% exercicio 5a
N = [20 40 100]
for i=1:length(N)
    ncoins=15
    for k=0:ncoins
        prob(k+1) = coins(0.5,ncoins,k,N)
    end
end