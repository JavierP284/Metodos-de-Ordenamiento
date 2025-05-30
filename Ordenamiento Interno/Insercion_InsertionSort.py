def insertion_sort(lista):
    for i in range(1, len(lista)):
        clave = lista[i]
        j = i - 1
        # Mover los elementos de lista[0..i-1], que son mayores que clave,
        # a una posición adelante de su posición actual
        while j >= 0 and clave < lista[j]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = clave
    return lista
# Ejemplo de uso
numeros = [12, 11, 13, 5, 6, 90, 76, 23, 45, 67]
print("Lista desordenada:", numeros)
ordenados = insertion_sort(numeros)
print("Lista ordenada:", ordenados)