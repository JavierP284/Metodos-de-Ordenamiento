# Algoritmo Radix Sort

def counting_sort_por_digito(arr, exp):
    n = len(arr)
    output = [0] * n  # Array de salida donde se almacenarán los números ordenados temporalmente
    count = [0] * 10  # Array para contar la frecuencia de cada dígito (0-9)

    # Contar ocurrencias de cada dígito en la posición actual (exp)
    for i in range(n):
        index = (arr[i] // exp) % 10  # Extrae el dígito correspondiente
        count[index] += 1

    # Modificar count[i] para que contenga la posición real de este dígito en output[]
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Construir el array de salida usando count[] para ubicar cada número en su posición correcta
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1  # Disminuir el contador para el siguiente número igual

    # Copiar el array de salida a arr[], para que arr[] contenga los números ordenados por el dígito actual
    for i in range(n):
        arr[i] = output[i]
    
def radix_sort(arr):
    # Encuentra el número máximo para saber el número de dígitos
    max_num = max(arr)

    # Aplica counting_sort para cada dígito, empezando por el menos significativo
    exp = 1  # Exponente para acceder a cada dígito (1, 10, 100, ...)
    while max_num // exp > 0:
        counting_sort_por_digito(arr, exp)
        exp *= 10  # Mover al siguiente dígito (decena, centena, etc.)
    return arr

# Ejemplo de uso
arr = [170, 45, 75, 90, 802, 24, 2, 66]
print("Array original:", arr)
sorted_arr = radix_sort(arr)
print("Array ordenado:", sorted_arr)