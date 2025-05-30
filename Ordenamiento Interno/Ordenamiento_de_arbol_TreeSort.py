# Algoritmo de Tree Sort (Ordenamiento por árbol)

# Definición de la clase Nodo para el árbol binario de búsqueda
class Nodo:
    def __init__(self, valor):
        self.valor = valor         # Valor almacenado en el nodo
        self.izquierda = None      # Referencia al hijo izquierdo
        self.derecha = None        # Referencia al hijo derecho

# Función para insertar un valor en el árbol binario de búsqueda
def insertar(nodo, valor):
    if nodo is None:
        return Nodo(valor)        # Si el nodo es nulo, crea uno nuevo
    if valor < nodo.valor:
        nodo.izquierda = insertar(nodo.izquierda, valor)  # Inserta en el subárbol izquierdo si es menor
    else:
        nodo.derecha = insertar(nodo.derecha, valor)      # Inserta en el subárbol derecho si es mayor o igual
    return nodo                   # Devuelve el nodo raíz actualizado

# Función para realizar el recorrido inorden del árbol (izquierda, raíz, derecha)
def recorrido_inorden(nodo, lista):
    if nodo is not None:
        recorrido_inorden(nodo.izquierda, lista)  # Recorre el subárbol izquierdo
        lista.append(nodo.valor)                  # Agrega el valor del nodo actual
        recorrido_inorden(nodo.derecha, lista)    # Recorre el subárbol derecho

# Función principal para ordenar una lista usando Tree Sort
def tree_sort(lista):
    if not lista:
        return []                # Si la lista está vacía, retorna una lista vacía
    
    raiz = None
    # Inserta cada elemento de la lista en el árbol binario de búsqueda
    for valor in lista:
        raiz = insertar(raiz, valor)
    
    lista_ordenada = []
    # Realiza el recorrido inorden para obtener los elementos ordenados
    recorrido_inorden(raiz, lista_ordenada)
    return lista_ordenada

# Ejemplo de uso
numeros = [64, 34, 25, 12, 22, 11, 90]
print("Lista desordenada:", numeros)
ordenados = tree_sort(numeros)  # Ordena la lista usando Tree Sort
print("Lista ordenada:", ordenados)
