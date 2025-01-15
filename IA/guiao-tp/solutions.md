# II - Agentes Reactivos

## II.1

### (a)
- Variáveis de estado:
	- A: Arpões disponíveis [0,10].
	- P: Peixes no depósito [0,20].
	- S: Sensor de peixe {0,1}.
	- D: Disparo do arpão acertou peixe {0,1}.

### (b)
        

# III - Representaçâo do Conhecimento

## III.8
```
p(a) = 0.2
p(b|a) = 0.3
p(b|¬a) = 0.2
p(c|b) = 0.2
p(c|¬b) = 0.9
p(d|b) = 0.1
p(d|¬b) = 0.2

p(a^b^¬c^¬d) = p(a)*p(b|a)*p(¬c|b)*p(¬d|b)
			 = 0.2*0.3*(1-0.2)*(1-0.1)
			 = 0.0432
```

## III.10
	
Predicados: A(a), E(a,e), V(a,t), Ext(e,t), P(p,a)<br>
...

## III.11

- Variaveis independentes
	
	- ST - Sobrecarga de trabalho
	- PT - Processador de texto

- Variáveis dependentes
	
	- PA - Precisa de ajuda
	- CP - Cara preocupada
	- FER - Frequência exagerada do rato
	- CNL - Correio não lido

- Tipologia
```
	    	ST           PT
	       /  \         /  \
	      /    \       /    \
	    CNL     \    _PA ___ \
		         \  /       \ |
		          CP         FER
```

- Probabilidades
```
P(ST) = 0.6

P(PT) = 0.05

P(CP|ST,PA) = 0.02
P(CP|ST,~PA) = 0.01
P(CP|~ST,PA) = 0.011
P(CP|~ST,~PA) = 0.001

P(FER|PT,PA) = 0.9
P(FER|PT,~PA) = 0.9
P(FER|~PT,PA) = 0.1
P(FER|~PT,~PA) = 0.01

P(PA|PT) = 0.25
P(PA|~PT) = 0.004

P(CNL|ST) = 0.9
P(CNL|~ST) = 0.001
```
# IV - Técnicas de resolução automática de problemas

## IV.1

### (a)
Não é admissível.<br>
F: 10 --> 8<br>
E: 7 --> 6<br>
G: 8 --> 6

### (b) 
```
1/F/10
-- 2/C/6
-- -- 5/B/6
-- -- -- 8/A/8 <-- SOLUÇÃO
-- -- 6/D/9
-- -- 7/E/11
-- 3/H/6
-- -- 9/E/16
-- --10/I/9
-- --11/G/16
-- 4/G/11
```
Estado final imediatamente antes de encontrar a solucão<br>
[8,10,6,7,4,9,11]

### (c)
N - nº de nós da árvore = 11<br>
X - nº de nós expandidos = 4<br>

FRM = (N-1)/X = 2.5
	
### (d)
```
B - factor de ramificação efectivo
d - profundidade da solução = 3
N - nº total de nós = 11

B^(d+1)-1
--------- = N
	B-1
	
B?		N?
----------
2		15	(2^4-1)/(2-1) = 15
1.5		8	(1.5^4-1)/(1.5-1) ~= 8
1.7		11	(1.7^4-1)/(1.7-1) ~= 11	<-- solução
```
## IV.2
Min = g+1
Max = SUM_(i=0...d){r^i} - SUM_(i=0...d-g){r^i} + 1(do nó solução)

## IV.4
### (a)
```py
[ (A,B), (A,D), (A,E)
(B,A), (B,C), (B,E)
(C,B), (C,D), (C,E)
(D,A), (D,C), (D,E)
(E,A), (E,B), (E,C), (E,D) ]

min(cores) = 3
```

### (b)
```py
[ (A,B), (A,D), (A,E),
(B,A), (B,C), (B,E),
(C,B), (C,F), (C,E),
(F,C), (F,D), (F,E),
(D,A), (D,F), (D,E),
(E,A), (E,B), (E,C), (E,D) ]

min(cores) = ...
```

### (C)
```py
[

]

min(cores) = ...
```
## IV.5
### (a) 
```py
	domain = 
	{ 'Andre': [('Bernardo', 'Claudio'), ('Claudio', 'Bernardo')], 
	'Bernardo': [('Andre', 'Claudio'), ('Claudio', 'Andre')], 
	'Claudio': [('Andre', 'Bernardo'), ('Bernardo', 'Andre')] }
	
	constraints = 
```
## IV.6
```py
vars = V(i,j), i = 1..9, j = 1..9

domain = V(i,j) in {1,2,3,4,5,6,7,8,9}

unary constraints
	V(4,1) = 5
	V(6,1) = 7
	V(9,1) = 3
	V(3,2) = 5
	V(7,2) = 8
	V(9,2) = 2
	...

binary constraints
	r(v1,x1,v2,x2) = x1!=x2
	
	V(i,j), V(i,k), i=1..9, j=1..9, k=1..9, j!=k (columns)
		r constraint
	
	V(i,j), V(k,j), i=1..9, j=1..9, k=1..9, i!=k (lines)
		r constraint
		
	... (3x3)
```

# V - Aprendizagem automática

## V.1