import os
import heapq

# Obtener la ruta del directorio donde está el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Definir carpetas para los archivos temporales y de runs
RUNS_DIR = os.path.join(BASE_DIR, "runs")
TEMP_DIR = os.path.join(BASE_DIR, "temporal")

# Crear carpetas si no existen
os.makedirs(RUNS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def crear_runs(nombre_entrada, tamaño_run):
    """
    Divide el archivo de entrada en varios archivos 'run' ordenados de tamaño fijo.
    """
    with open(os.path.join(BASE_DIR, nombre_entrada), 'r') as archivo:
        datos = list(map(int, archivo.read().split()))

    i = 0
    run_num = 0
    # Crear runs de tamaño 'tamaño_run'
    while i < len(datos):
        run = datos[i:i + tamaño_run]
        run.sort()  # Ordenar cada run individualmente
        with open(os.path.join(RUNS_DIR, f'run{run_num}.txt'), 'w') as f:
            f.write(' '.join(map(str, run)))
        run_num += 1
        i += tamaño_run

def multiway_merge(k, nombre_salida):
    """
    Realiza la mezcla balanceada de múltiples caminos (k-way merge) sobre los archivos run.
    """
    # Obtener lista de archivos run
    run_files = sorted([f for f in os.listdir(RUNS_DIR) if f.startswith('run')])
    
    # Continuar mientras haya más de un archivo run
    while len(run_files) > 1:
        num_runs = len(run_files)
        # Agrupar los archivos en grupos de tamaño k
        grupos = [run_files[i:i + k] for i in range(0, num_runs, k)]
        nueva_generacion = []
        temp_index = 0

        for grupo in grupos:
            # Abrir los archivos del grupo y leer sus datos
            archivos = [open(os.path.join(RUNS_DIR, nombre), 'r') for nombre in grupo]
            listas = [list(map(int, archivo.read().split())) for archivo in archivos]

            # Usar un heap para mezclar los k archivos
            heap = []
            indices = [0] * len(listas)  # Índices para cada lista
            resultado = []

            # Inicializar el heap con el primer elemento de cada lista
            for i, lista in enumerate(listas):
                if lista:
                    heapq.heappush(heap, (lista[0], i))

            # Extraer el menor elemento y reponer del mismo origen
            while heap:
                valor, origen = heapq.heappop(heap)
                resultado.append(valor)
                indices[origen] += 1
                if indices[origen] < len(listas[origen]):
                    heapq.heappush(heap, (listas[origen][indices[origen]], origen))

            # Guardar el resultado mezclado en un archivo temporal
            nombre_temp = os.path.join(TEMP_DIR, f"temp{temp_index}.txt")
            with open(nombre_temp, 'w') as f:
                f.write(' '.join(map(str, resultado)))
            nueva_generacion.append(nombre_temp)
            temp_index += 1

            # Cerrar archivos abiertos
            for archivo in archivos:
                archivo.close()

        # Borrar los archivos run anteriores
        for f in run_files:
            os.remove(os.path.join(RUNS_DIR, f))

        # Mover los archivos temporales a la carpeta runs y renombrarlos como nuevos runs
        for i, archivo in enumerate(nueva_generacion):
            with open(archivo, 'r') as f_in:
                contenido = f_in.read()
            nuevo_nombre = os.path.join(RUNS_DIR, f"run{i}.txt")
            with open(nuevo_nombre, 'w') as f_out:
                f_out.write(contenido)
            os.remove(archivo)

        # Actualizar la lista de archivos run para la siguiente iteración
        run_files = sorted([f for f in os.listdir(RUNS_DIR) if f.startswith('run')])

    # Renombrar el único archivo restante como archivo de salida final
    salida_final = os.path.join(BASE_DIR, nombre_salida)
    if os.path.exists(salida_final):
        os.remove(salida_final)
    os.rename(os.path.join(RUNS_DIR, run_files[0]), salida_final)

# Crear archivo de entrada (ejemplo)
with open(os.path.join(BASE_DIR, 'entrada.txt'), 'w') as f:
    f.write('90 10 20 80 70 40 30 50 60 100 15 5 25 35 45 55 65 75 85 95')

# Mostrar entrada
with open(os.path.join(BASE_DIR, 'entrada.txt'), 'r') as f:
    print("Archivo de entrada:", f.read())

# Ejecutar Balanced Multiway Merging con K=3
crear_runs('entrada.txt', tamaño_run=4)
multiway_merge(k=3, nombre_salida='salida_ordenada.txt')

# Mostrar resultado
with open(os.path.join(BASE_DIR, 'salida_ordenada.txt'), 'r') as f:
    print("Archivo final ordenado:", f.read())
