import copy

class Node:
  def __init__(self, state, parent=None):
    self.state = state
    self.parent = parent
    self.cost = 0
    self.heuristic_cost = 0

  def set_cost(self, cost):
    self.cost = cost

  def set_heuristic_cost(self, h_cost):
    self.heuristic_cost = h_cost

  def get_total_cost(self):
    return self.cost + self.heuristic_cost

  def get_state(self):
    return self.state

  def get_cost(self):
    return self.cost

class OpenList:
  def __init__(self):
    self.nodes = []

  def add(self, node):
    self.nodes.append(node)

  def pop_lowest_cost(self):
    if not self.nodes:
      return None
    lowest_node = min(self.nodes, key=lambda nd: nd.get_total_cost())
    self.nodes.remove(lowest_node)
    return lowest_node

  def is_empty(self):
    return len(self.nodes) == 0

  def contains_state(self, state_str):
    for node in self.nodes:
      if AStar.state_to_string(node.get_state()) == state_str:
        return True
    return False

  def get_node_by_state(self, state_str):
    for node in self.nodes:
      if AStar.state_to_string(node.get_state()) == state_str:
        return node
    return None

class ClosedList:
  def __init__(self):
    self.visited = set()

  def add(self, state_str):
    self.visited.add(state_str)

  def contains(self, state_str):
    return (state_str in self.visited)

class AStar:
  def __init__(self):
    self.open_list = OpenList()
    self.closed_list = ClosedList()

  @staticmethod
  def state_to_string(state):
    # Convert each column to comma-separated, then columns to '|' separated
    return "|".join(",".join(col) for col in state)

  def heuristic(self, state):
    # Heuristic: sum of (k - 1) for each column, where k is distinct colors
    h_val = 0
    for column in state:
      distinct_colors = set(column)
      if len(distinct_colors) > 1:
        h_val += (len(distinct_colors) - 1)
    return h_val

  def is_goal_state(self, state):
    color_columns_count = {}

    for column in state:
      if len(column) > 0:
        first_color = column[0]
        for tile in column:
          if tile != first_color:
            return False

        if first_color not in color_columns_count:
          color_columns_count[first_color] = 1
        else:
          color_columns_count[first_color] += 1
          if color_columns_count[first_color] > 1:
            return False
    return True

  def get_possible_moves(self, current_state):
      """
      Generate successor states by moving the top tile of one column
      to either an empty column or onto a tile of the same color, 
      if that column isn't already full (max 6).
      """
      next_states = []
      for i in range(len(current_state)):
        if len(current_state[i]) == 0:
          continue
        tile_to_move = current_state[i][-1]

        for j in range(len(current_state)):
          if i == j:
            continue
          if len(current_state[j]) < 6:  # not full
            # valid if empty or top tile is the same color
            if (len(current_state[j]) == 0) or (current_state[j][-1] == tile_to_move):
              new_state = copy.deepcopy(current_state)
              new_state[i].pop()
              new_state[j].append(tile_to_move)
              next_states.append(new_state)
      return next_states

  def search(self, initial_state):
    start_node = Node(state=initial_state, parent=None)
    start_node.set_cost(0)
    start_node.set_heuristic_cost(self.heuristic(initial_state))
    self.open_list.add(start_node)

    while not self.open_list.is_empty():
      current_node = self.open_list.pop_lowest_cost()
      current_state = current_node.get_state()

      if self.is_goal_state(current_state):
        return current_node

      current_state_str = self.state_to_string(current_state)
      self.closed_list.add(current_state_str)

      successors = self.get_possible_moves(current_state)

      for succ_state in successors:
        succ_state_str = self.state_to_string(succ_state)
        if self.closed_list.contains(succ_state_str):
          continue

        g_cost = current_node.get_cost() + 1
        h_cost = self.heuristic(succ_state)
        f_cost = g_cost + h_cost

        if self.open_list.contains_state(succ_state_str):
          existing_node = self.open_list.get_node_by_state(succ_state_str)
          if existing_node.get_total_cost() > f_cost:
            existing_node.set_cost(g_cost)
            existing_node.set_heuristic_cost(h_cost)
            existing_node.parent = current_node
        else:
          succ_node = Node(state=succ_state, parent=current_node)
          succ_node.set_cost(g_cost)
          succ_node.set_heuristic_cost(h_cost)
          self.open_list.add(succ_node)

    return None  # no solution
