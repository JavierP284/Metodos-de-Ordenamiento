import os

def ruta_local(nombre_archivo):
    return os.path.join(os.path.dirname(__file__), nombre_archivo)

def dividir_en_runs(nombre_entrada, tamaño_run):
    with open(ruta_local(nombre_entrada), 'r') as archivo:
        datos = list(map(int, archivo.read().split()))
    
    i = 0
    run_num = 1
    while i < len(datos):
        run = datos[i:i + tamaño_run]
        run.sort()  # ordenar el fragmento en memoria
        with open(ruta_local(f'run{run_num}.txt'), 'w') as f:
            f.write(' '.join(map(str, run)))
        run_num += 1
        i += tamaño_run

def mezclar_runs(nombre_salida, num_runs):
    while num_runs > 1:
        nuevo_num_runs = 0
        i = 1
        while i <= num_runs:
            try:
                with open(ruta_local(f'run{i}.txt'), 'r') as f1, open(ruta_local(f'run{i+1}.txt'), 'r') as f2:
                    datos1 = list(map(int, f1.read().split()))
                    datos2 = list(map(int, f2.read().split()))
                    mezcla = merge(datos1, datos2)
                    nuevo_num_runs += 1
                    with open(ruta_local(f'run_temp{nuevo_num_runs}.txt'), 'w') as fout:
                        fout.write(' '.join(map(str, mezcla)))
            except FileNotFoundError:
                # Si hay un run sin par, lo copiamos sin mezclar
                with open(ruta_local(f'run{i}.txt'), 'r') as f:
                    datos = f.read()
                    nuevo_num_runs += 1
                    with open(ruta_local(f'run_temp{nuevo_num_runs}.txt'), 'w') as fout:
                        fout.write(datos)
            i += 2
        
        # Renombrar archivos temporales como nuevos runs y eliminar temporales
        for j in range(1, nuevo_num_runs + 1):
            temp_path = ruta_local(f'run_temp{j}.txt')
            run_path = ruta_local(f'run{j}.txt')
            with open(temp_path, 'r') as f_in, open(run_path, 'w') as f_out:
                f_out.write(f_in.read())
            os.remove(temp_path)  # Elimina el archivo temporal

        # Eliminar archivos runX.txt sobrantes de la ronda anterior
        j = nuevo_num_runs + 1
        while os.path.exists(ruta_local(f'run{j}.txt')):
            os.remove(ruta_local(f'run{j}.txt'))
            j += 1

        num_runs = nuevo_num_runs

    # Renombrar el último archivo como salida final, eliminando si ya existe
    salida_path = ruta_local(nombre_salida)
    run1_path = ruta_local('run1.txt')
    if os.path.exists(salida_path):
        os.remove(salida_path)
    os.rename(run1_path, salida_path)

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
    resultado.extend(lista1[i:])
    resultado.extend(lista2[j:])
    return resultado

# Simulación de uso
# Paso 1: Crear archivo con datos
with open(ruta_local('entrada.txt'), 'w') as f:
    f.write('90 10 20 80 70 40 30 50 60 100')

# Paso 2: Dividir en runs de tamaño 2 (puedes ajustar según RAM disponible)
dividir_en_runs('entrada.txt', tamaño_run=2)

# Paso 3: Mezclar runs en un solo archivo
mezclar_runs('salida_ordenada.txt', num_runs=5)

# Ver resultado
with open(ruta_local('entrada.txt'), 'r') as f:
    print("Archivo entrada:", f.read())
with open(ruta_local('salida_ordenada.txt'), 'r') as f:
    print("Archivo ordenado:", f.read())
