from collections import deque
import copy

# Funci�n para imprimir matriz en un formato legible
def print_matrix(current_board):
    for row in current_board:
        print(" ".join(str(cell) if cell is not None else '.' for cell in row))


def search_nonheuristic_solution(initial_state):
    # Inicializar lista de soluciones exploradas no repetidas
    explored = set()
    # Inicializar cola de soluciones a explorar
    frontier = deque([initial_state])

    # Inicializar n�mero de iteraciones
    iteration = 0
    # Mientras a frontera no est� vac�a
    while frontier:
        # Se toma elemento a la izquierda de la cola
        current_state = frontier.popleft()

        # Impresi�n de una iteraci�n cada 500
        if iteration % 500 == 0:
            # Print the iteration and matrix to the console
            print(f"Iteration: {iteration}")
            print_matrix(current_state)
            print(iteration)
        
        # Se busca si el estado actual es soluci�n
        if is_correct_state(current_state):
            print("Found it!")
            return current_state

        # Se agrega estado a lista de explorados
        explored.add(tuple(map(tuple, current_state)))

        # Se busca y devuelve los vecinos del estado actual
        neighbors = find_neighbors(current_state)

        # Se busca en los vecinos y si no han sido explorados o no est�n en la frontera, se agregan
        if neighbors:
            for neighbor in neighbors:
                if tuple(map(tuple, neighbor)) not in explored and neighbor not in frontier:
                    frontier.append(neighbor)
        iteration += 1

# Funci�n para determinar si el estado es correcto
def is_correct_state(current_state):
    # Contador de cantidad de columnas vac�as
    empty_columns = 0
    # Lista no repetida de colores ya explorados para la soluci�n
    explored_colors = set(['G', 'Y', 'B', 'R'])

    # Obtenci�n de filas y columnas
    rows = len(current_state)
    cols = len(current_state[0])

    # Se cicla por columna
    for i in range(cols):
        # Se ve el elemento base de la columna y se revisa si ya fue explorado
        if current_state[5][i] in explored_colors:
            # Se elimina de la lista
            explored_colors.discard(current_state[5][i])
            # Se verifica si la columna es valida
            if is_valid_column(current_state, i, current_state[5][i]) == False:
                # No es valida
                return False
        # Si la base est� vac�a, significa que la columna tambi�n
        elif current_state[5][i] is None:
            # Se incrementa contador en 1
            empty_columns += 1
            # Se revisa si hay m�s de 2 columnas vac�as
            if empty_columns > 2:
                return False
        else:
            return False

    return True

def find_neighbors(resident_state):
    # Inicializaci�n de cola de vecinos
    neighbors = deque()
    # Se inicializa lista de tuplas de celdas vac�as validas
    valid_empty_cells = []
    # Se inicializa lista de tuplas de colores a mover v�lidos
    valid_color_cells = []
    
    # Iterar sobre cada columna para verificar su validez
    valid_columns = [False] * len(resident_state[0])  # Lista que marca si una columna es v�lida o no
    
    # Verificar la validez de cada columna
    for col in range(len(resident_state[0])):  # Itera sobre las columnas
        if is_valid_column(resident_state, col, resident_state[5][col]):
            valid_columns[col] = True
    
    # Se itera fila
    for i in range(len(resident_state)):
        # Se itera columna
        for j in range(len(resident_state[i])):
            # Se revisa si la celda est� vac�a
            if resident_state[i][j] is None:
                # Si es la �ltima fila, la posici�n actual es v�lida
                if i == (len(resident_state) - 1):
                    valid_empty_cells.append((i, j))
                # Si la celda debajo no est� vac�a, es v�lida
                elif resident_state[i+1][j] is not None:
                    valid_empty_cells.append((i, j))
            else:
                if valid_columns[j] == False:
                    # Si color est� en el tope de la fila, se agrega
                    if i == 0:
                        valid_color_cells.append((i, j))
                    # Si color est� en la 4ta fila y la celda de arriba est� vac�a
                    elif i == 3 and resident_state[i - 1][j] is None:
                        # Se revisa si no es una columna v�lida
                        if is_valid_column(resident_state, j, resident_state[i][j]) == False:
                            # Se agrega
                            valid_color_cells.append((i, j))
                    # Si la celda de arriba es vac�a
                    elif resident_state[i - 1][j] is None:
                        valid_color_cells.append((i, j))

    # Procesar los vecinos
    for row1, col1 in valid_empty_cells:
        for row2, col2 in valid_color_cells:
            if col1 != col2:
                new_state = copy.deepcopy(resident_state)
                new_state[row1][col1], new_state[row2][col2] = new_state[row2][col2], new_state[row1][col1]
                neighbors.append(new_state)

    return neighbors

# Funci�n para revisar si la columna es una columna parte de una soluci�n
def is_valid_column(matrix, col, color):
    # Se revisan celdas de abajo para arriba de col
    for index in range(5, 1, -1):
        # Si celda posee otro color
        if matrix[index][col] != color:
            return False

    # Si celda arriba del �ltimo supuesto color, no es valido
    if matrix[1][col] is not None:
        return False

    return True