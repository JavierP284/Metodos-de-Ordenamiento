# Algoritmo de Bubble Sort (Ordenamiento burbuja)

def bubble_sort(lista):
    n = len(lista)  # Obtenemos la longitud de la lista
    for i in range(n):
        # Bandera para detectar si hubo algún intercambio
        intercambiado = False
        # Recorremos la lista hasta el último elemento no ordenado
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:  # Si el elemento actual es mayor que el siguiente
                # Intercambiamos los elementos
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                intercambiado = True  # Marcamos que hubo un intercambio
        if not intercambiado:  # Si no hubo intercambios, la lista ya está ordenada
            break
    return lista  # Retornamos la lista ya ordenada

# Ejemplo de uso
numeros = [64, 34, 25, 12, 22, 11, 90]
print("Lista desordenada:", numeros)
ordenados = bubble_sort(numeros)  # Ordenamos la lista
print("Lista ordenada:", ordenados)
