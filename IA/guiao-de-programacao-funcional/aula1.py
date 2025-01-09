#Exercicio 1.1
def comprimento(lista):
	# Base case: If the list is empty, its length is 0
    if lista == []:
        return 0
    # Recursive case: Otherwise, count the first element and recurse on the rest of the list
    return 1 + comprimento(lista[1:])

#Exercicio 1.2
def soma(lista):
	# Base case: If the list is empty, the sum has finished
    if lista == []:
        return 0
    # Recursive case: Otherwise, sum the first element and recurse on the rest of the list
    return lista[0] + soma(lista[1:])

#Exercicio 1.3
def existe(lista, elem):
    # Base case: If the list is empty, the element is not present
    if lista == []:
        return False
    # Base case: If the first element matches, return True
    if lista[0] == elem:
        return True
    # Recursive case: Check the rest of the list
    return existe(lista[1:], elem)

#Exercicio 1.4
def concat(l1, l2):
    # Base case: If the first list is empty, return the second list
    if l1 == []:
        return l2
    # Recursive case: Append the first element of lst1 to the result of concatenating the rest
    return [l1[0]] + concat(l1[1:], l2)

#Exercicio 1.5
def inverte(lista):
    # Base case: If the list is empty or has one element, return it
    if len(lista) == 0:
        return []
    # Recursive case: Reverse the rest of the list and append the first element at the end
    return inverte(lista[1:]) + [lista[0]]

#Exercicio 1.6
def capicua(lista):
    # Base case: If the list has 0 or 1 element, it is a palindrome
    if len(lista) <= 1:
        return True
    # Check if the first and last elements are the same
    if lista[0] != lista[-1]:
        return False
    # Recursive case: Check the inner portion of the list (exclude first and last elements)
    return capicua(lista[1:-1])

#Exercicio 1.7
def concat_listas(lista):
    # Base case: If the list of lists is empty, return an empty list
    if lista == []:
        return []
    # Recursive case: Concatenate the first list with the result of recursively concatenating the rest
    return lista[0] + concat_listas(lista[1:])

#Exercicio 1.8
def substitui(lista, original, novo):
    # Base case: If the list is empty or has one element, return it
    if len(lista) == 0:
        return []
    # Base case: If original occurres, exchange it for novo element
    if lista[0] == original:
        return [novo] + substitui(lista[1:],original, novo)
    # Recursive case: Concatenate the first list with the result of recursively concatenating the rest
    return [lista[0]] + substitui(lista[1:], original, novo)

#Exercicio 1.9
def fusao_ordenada(lista1, lista2):
	# Base cases: If either list is empty, return the other
    if not lista1:
        return lista2
    if not lista2:
        return lista1

    # Recursive case: Compare the first elements and merge accordingly
    if lista1[0] < lista2[0]:
        return [lista1[0]] + fusao_ordenada(lista1[1:], lista2)
    else:
        return [lista2[0]] + fusao_ordenada(lista1, lista2[1:])

#Exercicio 1.10
def lista_subconjuntos(lista):
    # Base case: If the list is empty, return a list with an empty list (the empty set)
    if len(lista) == 0:
        return [[]]
    
    # Recursive case: Get subsets of the rest of the list
    smaller_subsets = lista_subconjuntos(lista[1:])
    
    # Combine subsets with and without the first element of the set
    return smaller_subsets + [[lista[0]] + subset for subset in smaller_subsets]


#Exercicio 2.1
def separar(lista):
	    # Base case: If the list is empty, return two empty lists
    if not lista:
        return ([], [])
    
    # Recursive case: Unpack the first pair and recursively process the rest
    (first_a, first_b) = lista[0]
    rest_a, rest_b = separar(lista[1:])
    
    # Combine the first elements with the results from the recursive call
    return ([first_a] + rest_a, [first_b] + rest_b)

#Exercicio 2.2
def remove_e_conta(lista, elem):
    # Base case: If the list is empty, return an empty list and count of 0
    if not lista:
        return ([], 0)
    
    # Recursive case: Process the first element and then the rest of the list
    rest_list, rest_count = remove_e_conta(lista[1:], elem)
    
    if lista[0] == elem:
        # If the first element is x, exclude it from the list and increment the count
        return (rest_list, rest_count + 1)
    else:
        # If the first element is not x, include it in the list and keep the count unchanged
        return ([lista[0]] + rest_list, rest_count)

#Exercicio 2.3
def contar_ocurrencias(lista):
    # Helper function to count occurrences of a specific element
    def count_element(element, lista):
        if not lista:
            return 0
        return (1 if lista[0] == element else 0) + count_element(element, lista[1:])

    # Base case: If the list is empty, return an empty list
    if not lista:
        return []
    
    # Recursive case: Count occurrences of the first element, and proceed with the rest
    first_element = lista[0]
    count = count_element(first_element, lista)
    
    # Remove all occurrences of the first element from the list
    remaining_list = [x for x in lista if x != first_element]
    
    # Return the pair (element, count) and continue with the remaining list
    return [(first_element, count)] + contar_ocurrencias(remaining_list)

#Exercicio 3.1
def cabeca(lista):
    # If the list is empty, return None
    if not lista:
        return None
    # Otherwise, return the first element
    return lista[0]

#Exercicio 3.2
def cauda(lista):
	    # If the list is empty or has only one element, return an empty list
    if not lista:
        return None
    # Otherwise, return the list excluding the first element
    return lista[1:]

#Exercicio 3.3
def juntar(l1, l2):
    # Check if the lists have the same length
    if len(l1) != len(l2):
        return None

    # Base case: If either list is empty, return an empty list
    if not l1 or not l2:
        return []
    
    # Recursive case: Pair the first elements and recurse on the rest
    return [(l1[0], l2[0])] + juntar(l1[1:], l2[1:])

#Exercicio 3.4
def menor(lista):
	    # Base case: If the list is empty, return None
    if not lista:
        return None
    
    # Base case: If the list has only one element, return that element
    if len(lista) == 1:
        return lista[0]
    
    # Recursive case: Find the minimum in the rest of the list
    menor_que_resto = menor(lista[1:])
    
    # Compare the first element with the minimum of the rest of the list
    return min(lista[0], menor_que_resto)

#Exercicio 3.5 -- TO DO
def menorElem_lista(lista):
    # Base case: If the list is empty, return None
    if not lista:
        return None
    
    # Base case: 

    # Recursive case: 
    return lista[1:]

#Exercicio 3.6
def max_min(lista):
    # Base case: If the list is empty, return None
    if not lista:
        return None
    
    # Base case: If the list has only one element, return it as both max and min
    if len(lista) == 1:
        return (lista[0], lista[0])
    
    # Process two elements at a time
    if len(lista) == 2:
        return (max(lista[0], lista[1]), min(lista[0], lista[1]))
    
    # Get the max and min of the first two elements
    current_max, current_min = max(lista[0], lista[1]), min(lista[0], lista[1])
    
    # Recursively get the max and min for the rest of the list
    rest_max, rest_min = max_min(lista[2:])
    
    # Combine the results
    overall_max = max(current_max, rest_max)
    overall_min = min(current_min, rest_min)

    return (overall_max, overall_min)
