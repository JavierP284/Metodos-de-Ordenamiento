import os
import heapq

# Carpeta base donde se guardarán los archivos temporales
BASE_DIR = os.path.dirname(__file__)

# Divide el archivo de entrada en "runs" (sublistas ordenadas) de tamaño run_size
def create_initial_runs(filename, run_size):
    runs = []
    with open(filename, 'r') as f:
        data = []
        for line in f:
            data.append(int(line.strip()))
            if len(data) == run_size:
                runs.append(sorted(data))  # Ordena cada run individualmente
                data = []
        if data:
            runs.append(sorted(data))  # Añade el último run si quedó incompleto
    return runs

# Calcula la distribución de los runs iniciales usando la secuencia de Fibonacci
def fibonacci_distribution(n):
    fib = [1, 1]
    while fib[-1] < n:
        fib.append(fib[-1] + fib[-2])
    return fib[-3], fib[-2]  # Devuelve los dos números anteriores al último

# Escribe los runs en un archivo, cada run en una línea
def write_runs_to_file(filename, runs):
    with open(filename, 'w') as f:
        for run in runs:
            f.write(' '.join(map(str, run)) + '\n')

# Lee los runs desde un archivo y los devuelve como listas de enteros
def read_runs_from_file(filename):
    runs = []
    if not os.path.exists(filename):
        return runs
    with open(filename, 'r') as f:
        for line in f:
            run = list(map(int, line.strip().split()))
            if run:
                runs.append(run)
    return runs

# Fusiona los runs de dos listas (simula la fusión de dos cintas)
def merge_runs(tape1_runs, tape2_runs):
    merged_runs = []
    max_len = max(len(tape1_runs), len(tape2_runs))
    for i in range(max_len):
        r1 = tape1_runs[i] if i < len(tape1_runs) else []
        r2 = tape2_runs[i] if i < len(tape2_runs) else []
        merged_runs.append(list(heapq.merge(r1, r2)))  # Fusión ordenada de los runs
    return merged_runs

# Algoritmo principal de Polyphase Sort
def polyphase_sort_file(input_file, run_size=4):
    # 1. Crear los runs iniciales a partir del archivo de entrada
    runs = create_initial_runs(input_file, run_size)
    total_runs = len(runs)

    # 2. Calcular la distribución Fibonacci para repartir los runs entre las cintas
    f1, f2 = fibonacci_distribution(total_runs)
    if f1 + f2 < total_runs:
        f2 = total_runs - f1  # Ajuste si hay más runs que la suma de Fibonacci

    # 3. Definir rutas de archivos para las tres cintas simuladas
    tapeA_path = os.path.join(BASE_DIR, 'tapeA.txt')
    tapeB_path = os.path.join(BASE_DIR, 'tapeB.txt')
    tapeC_path = os.path.join(BASE_DIR, 'tapeC.txt')

    # 4. Escribir los runs iniciales en las dos primeras cintas
    tapeA = runs[:f1]
    tapeB = runs[f1:f1+f2]
    write_runs_to_file(tapeA_path, tapeA)
    write_runs_to_file(tapeB_path, tapeB)
    write_runs_to_file(tapeC_path, [])  # La tercera cinta inicia vacía

    # 5. Lista para rotar las cintas en cada iteración
    current = [tapeA_path, tapeB_path, tapeC_path]

    # 6. Proceso de fusión iterativa
    while True:
        source1 = read_runs_from_file(current[0])  # Leer runs de la primera cinta
        source2 = read_runs_from_file(current[1])  # Leer runs de la segunda cinta

        if not source1 and not source2:
            break  # Si ambas cintas están vacías, termina

        merged = merge_runs(source1, source2)  # Fusionar los runs de ambas cintas
        write_runs_to_file(current[2], merged)  # Escribir el resultado en la tercera cinta

        write_runs_to_file(current[0], [])  # Vaciar la cinta fuente 1
        write_runs_to_file(current[1], [])  # Vaciar la cinta fuente 2

        current = [current[1], current[2], current[0]]  # Rotar las cintas

        # Si solo queda una cinta con datos, termina el proceso
        non_empty = [f for f in current if os.path.exists(f) and os.path.getsize(f) > 0]
        if len(non_empty) == 1:
            break

    # 7. Leer el resultado final de la cinta no vacía y fusionar todos los runs restantes
    result_file = [f for f in current if os.path.exists(f) and os.path.getsize(f) > 0][0]
    with open(result_file, 'r') as f:
        runs = []
        for line in f:
            run = list(map(int, line.strip().split()))
            if run:
                runs.append(run)
        result = list(heapq.merge(*runs))  # Fusión final para obtener la lista ordenada

    # 8. Eliminar los archivos temporales de las cintas
    for fname in [tapeA_path, tapeB_path, tapeC_path]:
        if os.path.exists(fname):
            os.remove(fname)
    return result

# Crea un archivo de entrada con los datos proporcionados
def create_input_file(filename, data):
    with open(filename, 'w') as f:
        for num in data:
            f.write(f"{num}\n")

# EJEMPLO DE USO
data = [19, 5, 9, 1, 12, 3, 8, 15, 7, 11, 6, 4, 2, 14, 10, 13]
input_path = os.path.join(BASE_DIR, 'input.txt')
create_input_file(input_path, data)
print("Entrada:", data)
ordenado = polyphase_sort_file(input_path, run_size=4)
print("Resultado ordenado:", ordenado)
