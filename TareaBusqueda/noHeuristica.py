from collections import deque
import copy

# Función para imprimir matriz en un formato legible
def print_matrix(current_board):
    for row in current_board:
        print(" ".join(str(cell) if cell is not None else '.' for cell in row))


def search_nonheuristic_solution(initial_state):
    # Inicializar lista de soluciones exploradas no repetidas
    explored = set()
    # Inicializar cola de soluciones a explorar
    frontier = deque([initial_state])

    # Inicializar número de iteraciones
    iteration = 0
    # Mientras a frontera no esté vacía
    while frontier:
        # Se toma elemento a la izquierda de la cola
        current_state = frontier.popleft()

        # Impresión de una iteración cada 500
        if iteration % 500 == 0:
            # Print the iteration and matrix to the console
            print(f"Iteration: {iteration}")
            print_matrix(current_state)
            print(iteration)
        
        # Se busca si el estado actual es solución
        if is_correct_state(current_state):
            print("Found it!")
            return current_state

        # Se agrega estado a lista de explorados
        explored.add(tuple(map(tuple, current_state)))

        # Se busca y devuelve los vecinos del estado actual
        neighbors = find_neighbors(current_state)

        # Se busca en los vecinos y si no han sido explorados o no están en la frontera, se agregan
        if neighbors:
            for neighbor in neighbors:
                if tuple(map(tuple, neighbor)) not in explored and neighbor not in frontier:
                    frontier.append(neighbor)
        iteration += 1

# Función para determinar si el estado es correcto
def is_correct_state(current_state):
    # Contador de cantidad de columnas vacías
    empty_columns = 0
    # Lista no repetida de colores ya explorados para la solución
    explored_colors = set(['G', 'Y', 'B', 'R'])

    # Obtención de filas y columnas
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
        # Si la base está vacía, significa que la columna también
        elif current_state[5][i] is None:
            # Se incrementa contador en 1
            empty_columns += 1
            # Se revisa si hay más de 2 columnas vacías
            if empty_columns > 2:
                return False
        else:
            return False

    return True

def find_neighbors(resident_state):
    # Inicialización de cola de vecinos
    neighbors = deque()
    # Se inicializa lista de tuplas de celdas vacías validas
    valid_empty_cells = []
    # Se inicializa lista de tuplas de colores a mover válidos
    valid_color_cells = []
    
    # Iterar sobre cada columna para verificar su validez
    valid_columns = [False] * len(resident_state[0])  # Lista que marca si una columna es válida o no
    
    # Verificar la validez de cada columna
    for col in range(len(resident_state[0])):  # Itera sobre las columnas
        if is_valid_column(resident_state, col, resident_state[5][col]):
            valid_columns[col] = True
    
    # Se itera fila
    for i in range(len(resident_state)):
        # Se itera columna
        for j in range(len(resident_state[i])):
            # Se revisa si la celda está vacía
            if resident_state[i][j] is None:
                # Si es la última fila, la posición actual es válida
                if i == (len(resident_state) - 1):
                    valid_empty_cells.append((i, j))
                # Si la celda debajo no está vacía, es válida
                elif resident_state[i+1][j] is not None:
                    valid_empty_cells.append((i, j))
            else:
                if valid_columns[j] == False:
                    # Si color está en el tope de la fila, se agrega
                    if i == 0:
                        valid_color_cells.append((i, j))
                    # Si color está en la 4ta fila y la celda de arriba está vacía
                    elif i == 3 and resident_state[i - 1][j] is None:
                        # Se revisa si no es una columna válida
                        if is_valid_column(resident_state, j, resident_state[i][j]) == False:
                            # Se agrega
                            valid_color_cells.append((i, j))
                    # Si la celda de arriba es vacía
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

# Función para revisar si la columna es una columna parte de una solución
def is_valid_column(matrix, col, color):
    # Se revisan celdas de abajo para arriba de col
    for index in range(5, 1, -1):
        # Si celda posee otro color
        if matrix[index][col] != color:
            return False

    # Si celda arriba del último supuesto color, no es valido
    if matrix[1][col] is not None:
        return False

    return True