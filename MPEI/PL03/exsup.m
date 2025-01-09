%% PL3 suplementar 1

...

N = 1e3


for inic = 1:3
    num_passos=0;
    for i =  1:N
        state = crawl(T, 1, [4 5]);
    
        num_passos = num_passos + len(state) -1;
    end
    media = num_passos/N
    fprintf(1, "Inicio = %d -> %.4f\n", inic, media)
end
