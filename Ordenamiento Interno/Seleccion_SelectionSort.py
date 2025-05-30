# Algoritmo de Selection Sort (Ordenamiento por selección)

def selection_sort(lista):
    n = len(lista)  # Obtenemos la longitud de la lista
    for i in range(n):
        # Suponemos que el elemento actual (posición i) es el mínimo
        min_index = i
        # Buscamos en el resto de la lista un elemento menor
        for j in range(i + 1, n):
            if lista[j] < lista[min_index]:
                min_index = j  # Si encontramos uno menor, actualizamos el índice del mínimo
        # Intercambiamos el elemento actual con el elemento mínimo encontrado
        lista[i], lista[min_index] = lista[min_index], lista[i]
    return lista  # Retornamos la lista ya ordenada

# Ejemplo de uso
numeros = [12, 11, 13, 5, 6, 90, 76, 23, 45, 67]
print("Lista desordenada:", numeros)
ordenados = selection_sort(numeros)  # Ordenamos la lista
print("Lista ordenada:", ordenados)
