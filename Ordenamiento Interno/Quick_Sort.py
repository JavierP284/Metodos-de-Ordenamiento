# Algoritmo de Quick Sort

def quick_sort(lista):
    # Caso base: si la lista tiene 0 o 1 elemento, ya está ordenada
    if len(lista) <= 1:
        return lista
    else:
        # Elegimos el pivote como el elemento del medio
        pivot = lista[len(lista) // 2]
        # Sublista con los elementos menores al pivote
        left = [x for x in lista if x < pivot]
        # Sublista con los elementos iguales al pivote
        middle = [x for x in lista if x == pivot]
        # Sublista con los elementos mayores al pivote
        right = [x for x in lista if x > pivot]
        # Llamada recursiva para ordenar las sublistas y concatenarlas
        return quick_sort(left) + middle + quick_sort(right)

# Ejemplo de uso
lista = [3, 6, 8, 10, 1, 2, 1]
print("Lista original:", lista)
sorted_list = quick_sort(lista)
print("Lista ordenada:", sorted_list)