%% PL3 ex6

%% a

T = zeros(5)

e1= 1; e2= 2, e3= 4; e4= 3; e5= 5

% linha <- coluna
T(e1,e1) = 0.8
T(e2,e1) = 0.2

T(e2,e2) = 0.6
T(e4,e2) = 0.3
T(e3,e2) = 0.1

T(e4,e4) = 1

T(e1,e3) = 0.3
T(e2,e3) = 0.2
T(e3,e3) = 0.4
T(e5,e3) = 0.1

T(e5,e5) = 1

%% b, c

v0 = [1 0 0 0 0]'

for n = 1:100
    
    vn = T^n * v0
    p2(n) = vn(e2)
    p3(n) = vn(e4)
    p5(n) = vn(e5)
end

%plot(1:100, p2, 'bo:')

plot(1:100, p3, 'bo:', 1:100, p5, 'gx-')

%% d

Tcan = T
num_estados_transientes = 3

Q = T(1:num_estados_transientes, 1:num_estados_transientes)

%% e

% F = (I-Q)^-1

F = inv(eye(3)- Q)

%% f

sum(F)

%% g

R=Tcan(num_estados_transientes+1:end, 1:num_estados_transientes)

B = R*F
B
[p3(end) p5(end)]