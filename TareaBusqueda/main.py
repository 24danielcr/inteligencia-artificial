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
    max_altura = max((len(col) for col in estado), default=0)
    
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

def opcion_3():
    print("Opcion3")

def opcion_4():
    print("Opcion4")

def todas():
    busqueda_sin_heuristica()

def salir():
    print("Saliendo del programa.")
    exit()

def main():
    while True:
        print("\nPor favor seleccione un metodo de busqueda:")
        print("1. Busqueda sin Heuristica con Lista Abierta y Lista Cerrada")
        print("2. Opcion 2")
        print("3. IDF*")
        print("4. Opcion 4")
        print("5. Opcion 5")
        print("6. Salir")

        try:
            user_choice = int(input("Seleccione una opcion (1-6): "))

            if user_choice == 1:
                busqueda_sin_heuristica()
            elif user_choice == 2:
                opcion_2()
            elif user_choice == 3:
                opcion_3()
            elif user_choice == 4:
                opcion_4()
            elif user_choice == 5:
                todas()
            elif user_choice == 6:
                salir()
            else:
                print("Invalid choice, please choose a number between 1 and 6.")
        except ValueError:
            print("Invalid input, please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
