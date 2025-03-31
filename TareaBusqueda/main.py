import noHeuristica

correct_state = [[None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 ['Y', 'G', 'B', 'R', None, None],
                 ['Y', 'B', 'G', 'R', None, None],
                 ['Y', 'B', 'R', 'G', None, None],
                 ['Y', 'B', 'R', 'G', None, None]]

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
        print("3. Opcion 3")
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
