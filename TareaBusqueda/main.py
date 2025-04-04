import time
import noHeuristica
import IDS

import random

# Funcion que cambia lista de columnas a matriz 6x6, tambien rellena espacios vacios con None
def convertir_a_matriz(columnas):
    matriz = [[None for _ in range(6)] for _ in range(6)]

    for col_idx, columna in enumerate(columnas):
        for row_idx, ficha in enumerate(columna):
            matriz[5 - row_idx][col_idx] = ficha

    return matriz

def crear_estado_inicial():
    """
    Crea un estado inicial aleatorio con 6 columnas, asegurando que cada columna
    tenga como máximo 6 fichas y se distribuyan las 16 fichas disponibles (4 por cada color).
    """
    # Creamos la lista de todas las fichas disponibles
    fichas_disponibles = ['R', 'R', 'R', 'R',  # 4 fichas rojas
                         'G', 'G', 'G', 'G',   # 4 fichas verdes
                         'Y', 'Y', 'Y', 'Y',   # 4 fichas amarillas
                         'B', 'B', 'B', 'B']   # 4 fichas azules
    
    # Mezclamos las fichas
    random.shuffle(fichas_disponibles)

    # Seleccionamos 4 columnas al azar para ser ocupadas (de las 6 disponibles)
    columnas_ocupadas = random.sample(range(6), 4)
    
    # Inicializamos las 6 columnas vacías
    columnas = [[] for _ in range(6)]
    
    # Distribuimos las 16 fichas en las 6 columnas de forma aleatoria
    for ficha in fichas_disponibles:
        columnas_disponibles = [idx for idx in columnas_ocupadas if len(columnas[idx]) < 6]
        
        if not columnas_disponibles:
            raise Exception("No hay columnas disponibles con espacio. Esto no debería pasar con 16 fichas.")
        # Elegimos una columna aleatoria que no haya alcanzado el límite de 6 fichas
        
        columna_idx = random.choice(columnas_disponibles)
        columnas[columna_idx].append(ficha)
    
    return columnas

def imprimir_estado(estado):
    """Imprime el estado actual del tablero"""
    # Encontrar la altura máxima
    max_altura = len(estado)

    # Imprimir el tablero de arriba hacia abajo
    for i in range(max_altura-1, -1, -1):
        fila = ""

        for col in estado:
            if i < len(col):
                fila += f" {col[i]} "
            else:
                fila += " . "
        print(fila)
    
    # Imprimir los números de columna
    print(" 1  2  3  4  5  6 ")

def busqueda_sin_heuristica(estado_inicial):
    inicio = time.time()
    solucion_sin_heristica = noHeuristica.search_nonheuristic_solution(estado_inicial)
    fin = time.time()
    tiempo_total = fin - inicio  # Tiempo transcurrido en segundos
    print(f"Solucion encontrada en {tiempo_total:.4f} segundos:")
    noHeuristica.print_solution_path(solucion_sin_heristica)

def heuristic_search(initial_state):
    print("\n")

def busqueda_ids(estado_inicial):
    estado_inicial = IDS.Estado(estado_inicial)

    # Medir el tiempo antes de la búsqueda
    inicio = time.time()
    
    # Buscar solución sin límite de tiempo
    solucion = IDS.ids_con_heuristica(estado_inicial)
    
    # Medir el tiempo después de la búsqueda
    fin = time.time()
    
    tiempo_total = fin - inicio  # Tiempo transcurrido en segundos
    
    if solucion:
        print(f"{len(solucion.movimientos)} movimientos de la solucion:")
        
        # Mostrar los movimientos
        for i, mov in enumerate(solucion.movimientos):
            print(f"Paso {i+1}: {mov}")
        
        print("\nEstado final:")
        imprimir_estado(solucion.columnas)
    else:
        print(f"\nNo se encontró solución.")
    
    # Mostrar el tiempo total que tardó en encontrar la solución
    print(f"\nTiempo de ejecución: {tiempo_total:.4f} segundos.")

def todas(estado_inicial):
    busqueda_sin_heuristica(convertir_a_matriz(estado_inicial))
    heuristic_search(estado_inicial)
    busqueda_ids(estado_inicial)

def salir():
    print("Saliendo del programa.")
    exit()

def main():
    # Crear estados iniciales
    estados_iniciales = []
    for i in range(10):
        estados_iniciales.append(crear_estado_inicial())

    numero_estado = 0
    while numero_estado < len(estados_iniciales):
        print("\nPor favor seleccione un metodo de busqueda:")
        print("1. Busqueda sin Heuristica con Lista Abierta y Lista Cerrada")
        print("2. Búsqueda por A*")
        print("3. IDS con heuristica")
        print("4. Todas juntas")
        print("5. Salir")

        try:
            user_choice = int(input("Seleccione una opcion (1-6): "))
            print()

            if user_choice == 5:
                salir()
            elif user_choice > 5 or user_choice < 1 :
                print("Invalid choice, please choose a number between 1 and 6.")

            print(f"Estado inicial {numero_estado+1}:")
            imprimir_estado(estados_iniciales[numero_estado])   

            if user_choice == 1:
                busqueda_sin_heuristica(convertir_a_matriz(estados_iniciales[numero_estado]))
            elif user_choice == 2:
                heuristic_search(estados_iniciales[numero_estado])
            elif user_choice == 3:
                busqueda_ids(estados_iniciales[numero_estado])
            elif user_choice == 4:
                todas(estados_iniciales[numero_estado])

            numero_estado += 1
        except ValueError:
            print("Invalid input, please enter a number between 1 and 6.")
        except MemoryError as e:
            print("Memory out of bounds:",e)

if __name__ == "__main__":
    main()
