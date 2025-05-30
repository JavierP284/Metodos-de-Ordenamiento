import os

# Devuelve la ruta absoluta del archivo en la misma carpeta que este script
def ruta_local(nombre_archivo):
    return os.path.join(os.path.dirname(__file__), nombre_archivo)

# Divide el archivo de entrada en runs (fragmentos) ordenados de tamaño fijo
def dividir_en_runs(nombre_entrada, tamaño_run):
    with open(ruta_local(nombre_entrada), 'r') as archivo:
        datos = list(map(int, archivo.read().split()))
    
    i = 0
    run_num = 1
    while i < len(datos):
        # Toma un fragmento de tamaño 'tamaño_run' y lo ordena
        run = datos[i:i + tamaño_run]
        run.sort()  # Ordena el fragmento en memoria
        # Guarda el fragmento ordenado en un archivo runX.txt
        with open(ruta_local(f'run{run_num}.txt'), 'w') as f:
            f.write(' '.join(map(str, run)))
        run_num += 1
        i += tamaño_run

# Mezcla los runs de dos en dos hasta que solo quede uno (el archivo ordenado final)
def mezclar_runs(nombre_salida, num_runs):
    while num_runs > 1:
        nuevo_num_runs = 0
        i = 1
        while i <= num_runs:
            try:
                # Intenta abrir dos runs consecutivos para mezclarlos
                with open(ruta_local(f'run{i}.txt'), 'r') as f1, open(ruta_local(f'run{i+1}.txt'), 'r') as f2:
                    datos1 = list(map(int, f1.read().split()))
                    datos2 = list(map(int, f2.read().split()))
                    mezcla = merge(datos1, datos2)  # Mezcla ordenada de ambos runs
                    nuevo_num_runs += 1
                    # Guarda el resultado en un archivo temporal
                    with open(ruta_local(f'run_temp{nuevo_num_runs}.txt'), 'w') as fout:
                        fout.write(' '.join(map(str, mezcla)))
            except FileNotFoundError:
                # Si hay un run sin pareja, lo copia tal cual al siguiente ciclo
                with open(ruta_local(f'run{i}.txt'), 'r') as f:
                    datos = f.read()
                    nuevo_num_runs += 1
                    with open(ruta_local(f'run_temp{nuevo_num_runs}.txt'), 'w') as fout:
                        fout.write(datos)
            i += 2
        
        # Renombra los archivos temporales como nuevos runs y elimina los temporales
        for j in range(1, nuevo_num_runs + 1):
            temp_path = ruta_local(f'run_temp{j}.txt')
            run_path = ruta_local(f'run{j}.txt')
            with open(temp_path, 'r') as f_in, open(run_path, 'w') as f_out:
                f_out.write(f_in.read())
            os.remove(temp_path)  # Elimina el archivo temporal

        # Elimina archivos runX.txt sobrantes de la ronda anterior
        j = nuevo_num_runs + 1
        while os.path.exists(ruta_local(f'run{j}.txt')):
            os.remove(ruta_local(f'run{j}.txt'))
            j += 1

        # Actualiza el número de runs para la siguiente ronda
        num_runs = nuevo_num_runs

    # Renombra el último archivo como salida final, eliminando si ya existe
    salida_path = ruta_local(nombre_salida)
    run1_path = ruta_local('run1.txt')
    if os.path.exists(salida_path):
        os.remove(salida_path)
    os.rename(run1_path, salida_path)

# Mezcla dos listas ordenadas en una sola lista ordenada
def merge(lista1, lista2):
    resultado = []
    i = j = 0
    while i < len(lista1) and j < len(lista2):
        if lista1[i] <= lista2[j]:
            resultado.append(lista1[i])
            i += 1
        else:
            resultado.append(lista2[j])
            j += 1
    resultado.extend(lista1[i:])  # Agrega lo que queda de lista1
    resultado.extend(lista2[j:])  # Agrega lo que queda de lista2
    return resultado

# ----------------- Ejemplo de uso -----------------

# Paso 1: Crear archivo con datos de ejemplo
with open(ruta_local('entrada.txt'), 'w') as f:
    f.write('90 10 20 80 70 40 30 50 60 100')

# Paso 2: Dividir en runs de tamaño 2 (puedes ajustar el tamaño según la RAM disponible)
dividir_en_runs('entrada.txt', tamaño_run=2)

# Paso 3: Mezclar los runs en un solo archivo ordenado
mezclar_runs('salida_ordenada.txt', num_runs=5)

# Mostrar el resultado
with open(ruta_local('entrada.txt'), 'r') as f:
    print("Archivo entrada:", f.read())
with open(ruta_local('salida_ordenada.txt'), 'r') as f:
    print("Archivo ordenado:", f.read())
