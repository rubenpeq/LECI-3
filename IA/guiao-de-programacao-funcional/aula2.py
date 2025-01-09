import math

#Exercicio 4.1
impar = lambda x: x%2 != 0

#Exercicio 4.2
positivo = lambda x: x>0

#Exercicio 4.3
comparar_modulo = lambda x,y: x*x<y*y

#Exercicio 4.4 -- TO DO
cart2pol = lambda x,y: (math.sqrt(x*x + y*y), )

#Exercicio 4.5 -- TO DO
ex5 = lambda f,g,h: h

#Exercicio 4.6 -- EXPLAIN
def quantificador_universal(lista, f):
    if lista == []:
        return True
    return f(lista[0]) and quantificador_universal(lista[1:], f)

#Exercicio 4.8
def subconjunto(lista1, lista2):
    pass

#Exercicio 4.9 -- EXPLAIN
def menor_ordem(lista, f):
    # Base case: If the list is empty, return None
    if not lista:
        return None
    
    # Recursive case: 
    r0 = menor_ordem(lista[1:], f)
    if r0 == None or f(lista[0],r0):
        return lista[0]
    return r0

#Exercicio 4.10
def menor_e_resto_ordem(lista, f):
    pass

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    pass
