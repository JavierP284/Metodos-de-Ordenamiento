# Algoritmo de ordenamiento Merge Sort

def merge_sort(lista):
    # Caso base: si la lista tiene 0 o 1 elemento, ya está ordenada
    if len(lista) <= 1:
        return lista

    # Dividir la lista en dos mitades
    mid = len(lista) // 2
    left_half = merge_sort(lista[:mid])   # Ordenar recursivamente la mitad izquierda
    right_half = merge_sort(lista[mid:])  # Ordenar recursivamente la mitad derecha
    
    # Combinar las dos mitades ordenadas
    return merge(left_half, right_half)

def merge(left, right):
    result = []  # Lista donde se almacenará el resultado ordenado
    i = j = 0    # Índices para recorrer las listas left y right
    
    # Combinar los elementos de ambas listas mientras haya elementos en ambas
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])  # Agrega el menor elemento a la lista resultado
            i += 1
        else:
            result.append(right[j])
            j += 1
            
    # Agregar los elementos restantes de la lista izquierda (si quedan)
    while i < len(left):
        result.append(left[i])
        i += 1
        
    # Agregar los elementos restantes de la lista derecha (si quedan)
    while j < len(right):
        result.append(right[j])
        j += 1
        
    return result  # Devuelve la lista combinada y ordenada

# Ejemplo de uso
lista = [38, 27, 43, 3, 9, 82, 10]
print("Lista original:", lista)
sorted_list = merge_sort(lista)  # Llama a la función de ordenamiento
print("Lista ordenada:", sorted_list)
