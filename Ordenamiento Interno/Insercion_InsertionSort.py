#Insertion Sort

def insertion_sort(lista):
    # Recorre la lista desde el segundo elemento hasta el final
    for i in range(1, len(lista)):
        clave = lista[i]  # Elemento actual a insertar en la parte ordenada
        j = i - 1
        # Mueve los elementos de la parte ordenada que sean mayores que 'clave'
        # una posición adelante para hacer espacio a 'clave'
        while j >= 0 and clave < lista[j]:
            lista[j + 1] = lista[j]  # Desplaza el elemento hacia la derecha
            j -= 1
        lista[j + 1] = clave  # Inserta 'clave' en la posición correcta
    return lista

# Ejemplo de uso
numeros = [12, 11, 13, 5, 6, 90, 76, 23, 45, 67]
print("Lista desordenada:", numeros)
ordenados = insertion_sort(numeros)
print("Lista ordenada:", ordenados)