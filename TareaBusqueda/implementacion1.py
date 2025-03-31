from collections import deque
import copy

EMPTY = 0
GREEN = 1
YELLOW = 2
BLUE = 3
RED = 4

initial_state = [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                 [YELLOW, GREEN, GREEN, GREEN, EMPTY, EMPTY],
                 [BLUE, RED, RED, RED, EMPTY, EMPTY],
                 [BLUE, YELLOW, YELLOW, BLUE, EMPTY, EMPTY],
                 [RED, GREEN, YELLOW, BLUE, EMPTY, EMPTY]]

correct_state = [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                 [YELLOW, RED, GREEN, BLUE, EMPTY, EMPTY],
                 [YELLOW, RED, GREEN, BLUE, EMPTY, EMPTY],
                 [YELLOW, RED, GREEN, BLUE, EMPTY, EMPTY],
                 [YELLOW, RED, GREEN, BLUE, EMPTY, EMPTY]]


def search_solution(initial_state, output_file="search_output.txt"):
    explored = set()
    frontier = deque([initial_state])

    iteration = 0
    with open(output_file, 'w') as file:
        while frontier:
            current_state = frontier.popleft()

            if iteration % 500 == 0:
                file.write(f"Iteration: {iteration}\n")
                write_matrix_to_file(file, current_state)
                print(iteration)
                print_matrix(current_state)
            
            if is_correct_state(current_state):
                print("Found it!")
                return current_state

            explored.add(tuple(map(tuple, current_state)))

            neighbors = find_neighbors(current_state)

            if neighbors:
                for neighbor in neighbors:
                    if tuple(map(tuple, neighbor)) not in explored and neighbor not in frontier:
                        frontier.append(neighbor)
            iteration += 1


def is_correct_state(current_state):
    empty_rows = 0
    explored_colors = set([GREEN, YELLOW, BLUE, RED])

    rows = len(current_state)
    cols = len(current_state[0])

    for i in range(cols):
        if current_state[5][i] in explored_colors:
            explored_colors.discard(current_state[5][i])
            if is_valid_column(current_state, i, rows, current_state[5][i]) == False:
                return False
        elif current_state[5][i] == EMPTY:
            empty_rows += 1
            if empty_rows > 2:
                return False
        else:
            return False

    return True


def find_neighbors(state):
    neighbors = deque()
    valid_empty_cells = []
    valid_color_cells = []

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == EMPTY:
                if i == (len(state) - 1):
                    valid_empty_cells.append((i, j))
                elif state[i+1][j] != EMPTY:
                    valid_empty_cells.append((i, j))
            else:
                if i == 0:
                    valid_color_cells.append((i, j))
                elif state[i - 1][j] == EMPTY:
                    valid_color_cells.append((i, j))

    for row1, col1 in valid_empty_cells:
        for row2, col2 in valid_color_cells:
            if col1 != col2:
                new_state = copy.deepcopy(state)
                new_state[row1][col1], new_state[row2][col2] = new_state[row2][col2], new_state[row1][col1]
                neighbors.append(new_state)

    return neighbors


def print_matrix(matrix):
    for row in matrix:
        print(row)


def write_matrix_to_file(file, matrix):
    """Write the matrix to the output file"""
    for row in matrix:
        file.write(" ".join(str(cell) for cell in row) + "\n")


def is_valid_column(matrix, col, rows, color):
    for index in range(5, 1, -1):
        if matrix[index][col] != color:
            return False

    if matrix[1][col] != EMPTY:
        return False

    return True

solution = search_solution(correct_state, output_file="search_output.txt")
print_matrix(solution)
