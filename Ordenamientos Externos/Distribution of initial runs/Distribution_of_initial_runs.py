import os

# Obtener la ruta base donde está el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Crear carpeta 'tapes' en la misma carpeta que el código para simular las cintas
TAPES_DIR = os.path.join(BASE_DIR, "tapes")
os.makedirs(TAPES_DIR, exist_ok=True)

def generar_runs_ordenados(archivo_entrada, tamaño_run):
    """
    Lee el archivo de entrada y divide los datos en runs de tamaño 'tamaño_run',
    ordenando cada run individualmente.
    """
    with open(archivo_entrada, 'r') as f:
        datos = list(map(int, f.read().split()))

    runs = []
    # Divide los datos en bloques de tamaño 'tamaño_run' y los ordena
    for i in range(0, len(datos), tamaño_run):
        run = sorted(datos[i:i + tamaño_run])
        runs.append(run)
    return runs

def distribuir_runs_en_tapes(runs):
    """
    Distribuye los runs ordenados alternadamente entre dos archivos (T1.txt y T2.txt)
    simulando dos cintas.
    """
    tape1 = open(os.path.join(TAPES_DIR, "T1.txt"), 'w')
    tape2 = open(os.path.join(TAPES_DIR, "T2.txt"), 'w')

    for i, run in enumerate(runs):
        destino = tape1 if i % 2 == 0 else tape2
        destino.write(' '.join(map(str, run)) + '\n')

    tape1.close()
    tape2.close()

def mezclar_runs():
    """
    Mezcla los runs de las dos cintas (T1 y T2) de forma iterativa.
    En cada ronda, toma un run de cada cinta, los mezcla y los distribuye de nuevo
    alternadamente en las cintas, hasta que solo queda un run final ordenado.
    """
    while True:
        # Leer los runs actuales de ambas cintas
        with open(os.path.join(TAPES_DIR, "T1.txt"), 'r') as t1, open(os.path.join(TAPES_DIR, "T2.txt"), 'r') as t2:
            lines1 = [list(map(int, line.split())) for line in t1 if line.strip()]
            lines2 = [list(map(int, line.split())) for line in t2 if line.strip()]

        resultado = []
        # Mientras haya runs en alguna de las cintas
        while lines1 or lines2:
            if not lines1:
                resultado.extend(lines2)
                break
            if not lines2:
                resultado.extend(lines1)
                break

            # Tomar un run de cada cinta y mezclarlos
            run1 = lines1.pop(0)
            run2 = lines2.pop(0)

            i = j = 0
            mergeado = []

            # Mezcla tipo merge-sort de los dos runs
            while i < len(run1) and j < len(run2):
                if run1[i] < run2[j]:
                    mergeado.append(run1[i])
                    i += 1
                else:
                    mergeado.append(run2[j])
                    j += 1
            # Añadir los elementos restantes de ambos runs
            mergeado.extend(run1[i:])
            mergeado.extend(run2[j:])
            resultado.append(mergeado)

        # Si solo queda un run, ya está todo ordenado y se escribe el resultado final
        if len(resultado) == 1:
            with open(os.path.join(BASE_DIR, "salida_ordenada.txt"), 'w') as f:
                f.write(' '.join(map(str, resultado[0])) + '\n')
            break
        else:
            # Si quedan varios runs, se distribuyen de nuevo alternadamente en las cintas para la siguiente ronda
            with open(os.path.join(TAPES_DIR, "T1.txt"), 'w') as t1, open(os.path.join(TAPES_DIR, "T2.txt"), 'w') as t2:
                for i, run in enumerate(resultado):
                    destino = t1 if i % 2 == 0 else t2
                    destino.write(' '.join(map(str, run)) + '\n')

def ordenamiento_externo_por_runs():
    """
    Función principal que ejecuta el proceso completo:
    1. Genera los runs ordenados.
    2. Los distribuye en las cintas.
    3. Mezcla los runs hasta obtener el resultado final ordenado.
    """
    archivo_entrada = os.path.join(BASE_DIR, "entrada.txt")
    tamaño_run = 4  # Puedes cambiar este valor para simular memoria limitada

    runs = generar_runs_ordenados(archivo_entrada, tamaño_run)
    distribuir_runs_en_tapes(runs)
    mezclar_runs()

# Crear archivo de entrada con los datos a ordenar
entrada = "45 12 78 3 9 56 1 34 88 21 11 67"
with open(os.path.join(BASE_DIR, "entrada.txt"), 'w') as f:
    f.write(entrada)

# Mostrar la entrada original
print("Entrada original:\n", entrada)

# Ejecutar el algoritmo de ordenamiento externo
ordenamiento_externo_por_runs()

# Mostrar el resultado final ordenado
with open(os.path.join(BASE_DIR, "salida_ordenada.txt"), 'r') as f:
    print("Resultado final ordenado:\n", f.read())
