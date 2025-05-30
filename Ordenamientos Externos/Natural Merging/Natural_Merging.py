import os

# Obtener la ruta del directorio actual del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Crear carpetas para archivos temporales y de runs si no existen
runs_dir = os.path.join(BASE_DIR, "runs")
temp_dir = os.path.join(BASE_DIR, "temporal")
os.makedirs(runs_dir, exist_ok=True)
os.makedirs(temp_dir, exist_ok=True)

def detectar_runs_naturales(nombre_entrada):
    """
    Lee el archivo de entrada y detecta runs naturales (subsecuencias ordenadas).
    Alterna la escritura de cada run entre dos archivos: runA.txt y runB.txt.
    """
    with open(nombre_entrada, 'r') as archivo:
        datos = list(map(int, archivo.read().split()))

    runA = []
    runB = []
    usar_A = True  # Alterna entre runA y runB
    i = 0

    # Detectar runs naturales en los datos
    while i < len(datos):
        run = [datos[i]]
        i += 1
        while i < len(datos) and datos[i] >= datos[i - 1]:
            run.append(datos[i])
            i += 1
        if usar_A:
            runA.extend(run + ['|'])  # '|' separa los runs
        else:
            runB.extend(run + ['|'])
        usar_A = not usar_A

    # Guardar los runs en archivos separados
    with open(os.path.join(runs_dir, "runA.txt"), 'w') as f:
        f.write(' '.join(map(str, runA)))
    with open(os.path.join(runs_dir, "runB.txt"), 'w') as f:
        f.write(' '.join(map(str, runB)))

def mezclar_runs_naturales(nombre_salida):
    """
    Mezcla los runs de los archivos runA.txt y runB.txt hasta que todo esté ordenado.
    El resultado final se guarda en el archivo de salida especificado.
    """
    runA_path = os.path.join(runs_dir, "runA.txt")
    runB_path = os.path.join(runs_dir, "runB.txt")
    salida_temp = os.path.join(temp_dir, "salida1.txt")
    salida_final = os.path.join(BASE_DIR, nombre_salida)
    while True:
        # Leer los runs actuales de ambos archivos
        with open(runA_path, 'r') as fA, open(runB_path, 'r') as fB:
            datosA = fA.read().split()
            datosB = fB.read().split()

        # Si runB está vacío, todo está ordenado y se termina
        if not datosB:
            if os.path.exists(salida_final):
                os.remove(salida_final)
            os.rename(runA_path, salida_final)
            break

        iterA = iter(datosA)
        iterB = iter(datosB)

        runA = []
        runB = []

        def siguiente_run(it):
            """
            Extrae el siguiente run (subsecuencia hasta '|') del iterador.
            """
            run = []
            for x in it:
                if x == '|':
                    break
                run.append(int(x))
            return run

        # Mezclar runs de ambos archivos y escribirlos en un archivo temporal
        with open(salida_temp, 'w') as fout:
            while True:
                try:
                    if not runA:
                        runA = siguiente_run(iterA)
                    if not runB:
                        runB = siguiente_run(iterB)
                except StopIteration:
                    break

                if not runA and not runB:
                    break

                mezcla = merge(runA, runB)
                fout.write(' '.join(map(str, mezcla)) + ' | ')
                runA = []
                runB = []

        # Repartir los runs mezclados de nuevo entre runA.txt y runB.txt
        with open(salida_temp, 'r') as f:
            todos = f.read().strip().split('|')
            usar_A = True
            with open(runA_path, 'w') as fa, open(runB_path, 'w') as fb:
                for fragmento in todos:
                    fragmento = fragmento.strip()
                    if fragmento:
                        if usar_A:
                            fa.write(fragmento + ' | ')
                        else:
                            fb.write(fragmento + ' | ')
                        usar_A = not usar_A

def merge(lista1, lista2):
    """
    Mezcla dos listas ordenadas en una sola lista ordenada.
    """
    resultado = []
    i = j = 0
    while i < len(lista1) and j < len(lista2):
        if lista1[i] <= lista2[j]:
            resultado.append(lista1[i])
            i += 1
        else:
            resultado.append(lista2[j])
            j += 1
    resultado.extend(lista1[i:])
    resultado.extend(lista2[j:])
    return resultado

# Crear archivo de entrada en la misma carpeta que el script
entrada_path = os.path.join(BASE_DIR, "entrada.txt")
with open(entrada_path, "w") as f:
    f.write("5 10 12 3 4 20 25 1 2 30")

# Ejecutar Natural Merging: primero detectar runs, luego mezclar hasta ordenar
detectar_runs_naturales(entrada_path)
mezclar_runs_naturales("salida_ordenada.txt")

# Mostrar resultado de entrada y salida ordenada
with open(entrada_path, 'r') as f:
    print("Archivo entrada:", f.read().strip())
with open(os.path.join(BASE_DIR, "salida_ordenada.txt"), 'r') as f:
    print("Archivo final ordenado:", f.read().replace('|', '').strip())
