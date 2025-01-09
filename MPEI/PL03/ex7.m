%% PL3 ex7

%% a

A=1; B=2; C=3; D=4; E=5; F=6

H(B,A) = 1
H(C,B) = 1/2
H(E,B) = 1/2
H(D,C) = 1
H(C,D) = 1
H(A,E) = 1/3
H(B,E) = 1/3
H(F,E) = 1/3

H(isnan(H))=0
% equivalente a H(:,6) = 0

%% c

H(:,6)=1/6

%% d
v = ones(1,6)/6

beta = 0.8

A = beta*H + (1-beta)*v


pr = ones(6,1)/6

for i = 1:10
    pr= A*pr
end

%% e

%r0=1/6
%r_anterior = r0
%r=r0
%epsilon = 1e-4
%iter = 0
%
%while 1
%    r_anterior = r
%    r = A*r
%    iter = iter +1
%    if(max(r-r_anterior))<epsilon
%        break
%    end
%end