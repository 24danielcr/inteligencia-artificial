import time
import noHeuristica
import IDF

import random

correct_state = [[None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 ['Y', 'G', 'B', 'R', None, None],
                 ['Y', 'B', 'G', 'R', None, None],
                 ['Y', 'B', 'R', 'G', None, None],
                 ['Y', 'B', 'R', 'G', None, None]]

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
    
    # Inicializamos las 6 columnas vacías
    columnas = [[] for _ in range(6)]
    
    # Distribuimos las 16 fichas en las 6 columnas de forma aleatoria
    for ficha in fichas_disponibles:
        # Elegimos una columna aleatoria que no haya alcanzado el límite de 6 fichas
        columna_idx = random.choice([i for i in range(6) if len(columnas[i]) < 6])
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

def busqueda_sin_heuristica():
    solucion_sin_heristica = noHeuristica.search_nonheuristic_solution(correct_state)
    print("Solution")
    noHeuristica.print_matrix(solucion_sin_heristica)

def opcion_2():
    print("Opcion2")

def busqueda_idf(estado_inicial):
    estado_inicial = IDF.Estado(estado_inicial)

    # Medir el tiempo antes de la búsqueda
    inicio = time.time()
    
    # Buscar solución sin límite de tiempo
    solucion = IDF.idf_star(estado_inicial)
    
    # Medir el tiempo después de la búsqueda
    fin = time.time()
    
    tiempo_total = fin - inicio  # Tiempo transcurrido en segundos
    
    if solucion:
        print(f"\n¡Solución encontrada en {len(solucion.movimientos)} movimientos!")
        
        # Mostrar los movimientos
        print("\nSecuencia de movimientos:")
        for i, mov in enumerate(solucion.movimientos):
            print(f"Paso {i+1}: {mov}")
        
        print("\nEstado final:")
        imprimir_estado(solucion.columnas)
    else:
        print(f"\nNo se encontró solución.")
    
    # Mostrar el tiempo total que tardó en encontrar la solución
    print(f"\nTiempo de ejecución: {tiempo_total:.4f} segundos.")

def todas():
    busqueda_sin_heuristica()

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
        print("2. Opcion 2")
        print("3. IDF*")
        print("4. Todas juntas")
        print("5. Salir")

        try:
            user_choice = int(input("Seleccione una opcion (1-6): "))
            print()

            print(f"Estado inicial {numero_estado+1}:")
            imprimir_estado(estados_iniciales[numero_estado])

            if user_choice == 1:
                busqueda_sin_heuristica()
            elif user_choice == 2:
                opcion_2()
            elif user_choice == 3:
                busqueda_idf(estados_iniciales[0])
            elif user_choice == 4:
                todas()
            elif user_choice == 5:
                salir()
            else:
                print("Invalid choice, please choose a number between 1 and 6.")

            numero_estado += 1
        except ValueError:
            print("Invalid input, please enter a number between 1 and 6.")
        except MemoryError as e:
            print("Memory out of bounds:",e)

if __name__ == "__main__":
    main()
