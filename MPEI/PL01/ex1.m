%(a) Crie um vetor linha com uma sequência de números pares com início em 4 e a terminar no número 100.

v1=4:2:100;

%(b) Crie um vetor linha com uma sequˆencia decrescente de n´umeros inteiros com in´ıcio em 5 e a terminar em -5.

v2=5:-1:-5;
length(v2)
v2b=linspace(5,-5,10) %de 5 a -5 em 10 elementos
length(v2b)

%(c) Crie um vetor linha com uma sequˆencia de n´umeros reais igualmente espac¸ados com 100 elementos pertencentes ao intervalo [0 ... 1].

v3= linspace(0,1,100)

%(d) Crie uma matriz aleat´oria usando o comando >> B= rand(20,30) (20 linhas e 30 colunas).
%Construa um comando que permita extrair para uma matriz C uma sub-matriz de B constitu´ıda pela linhas de 10 a 15 e as colunas de 9 a 12.

format short
B= rand(20,30)

%(e) Gere uma sequˆencia, x, a comec¸ar em −π e a acabar em π com um passo de π/15.

x= -pi:pi/15:pi

%(f) Corra o comando >> plot(x, sin(4*pi*x). A que corresponde o gr´afico obtido?

plot(x, sin(4*pi*x))
plot(x, sin(2*pi/3*x))