%% PL3 ex4

%% a

p = 0.4
q = 0.6

n = 4
T = zeros(4)
% estados e linhas/colunas
A=1; B=2; C=3; D=4

T(A,A) = p^2
T(B,A) = (1-p)^2
T(C,A) = p*(1-p)
T(D,A) = p*(1-p)

T(D,B) = 1

T(A,D) = q^2
T(B,D) = q*(1-q)
T(D,D) = (1-q)^2
T(C,D) = q*(1-q)

T(D,C) = 1

%% b

v0 = [1,zeros(1,3)]'

for ntr = [5 10 100 200]
    Tn = T^ntr
    fprintf(1, "%4d - %6.3f, %6.3f, %6.3f, %6.3f \n", ntr, Tn(1:4))
end

%% c

ncols = size(T,2)
nlines = size(T,1)

M = [T - eye(size(T))
    ones(1, ncols)]

b = [zeros(nlines, 1); 1]

u = M\b
