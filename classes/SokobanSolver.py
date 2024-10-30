from collections import deque
from heapq import heappop, heappush

class SokobanSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.solution = None
        self.current_step = -1
        self.operation_limit = 10**6

    def can_move(self, state, x, y, dx, dy):
        new_x, new_y = x + dx, y + dy
        target_cell = state.get_cell(new_x, new_y)

        if target_cell == '#':
            return False

        if target_cell in ['$', '*']:
            return state.can_push_stone(new_x, new_y, dx, dy)

        return True

    def make_move(self, state, x, y, dx, dy):
        new_map = [list(row) for row in state.map]
        new_x, new_y = x + dx, y + dy

        # Get the current cell type with or without switch
        current_cell = state.get_cell(x, y)
        is_on_switch = current_cell == '+'

        # Get the target cell type
        target_cell = state.get_cell(new_x, new_y)
        target_has_switch = target_cell in ['.', '*', '+']

        # Update the player's current position
        new_map[x][y] = '.' if is_on_switch else ' '

        stone_move = None
        if target_cell in ['$', '*']:
            # Moving a stone
            push_x, push_y = new_x + dx, new_y + dy
            push_cell = state.get_cell(push_x, push_y)
            push_has_switch = push_cell in ['.', '*', '+']

            # Update the stone's position
            new_map[push_x][push_y] = '*' if push_has_switch else '$'
            stone_move = ((new_x, new_y), (push_x, push_y))

        # Update the player's new position
        new_map[new_x][new_y] = '+' if target_has_switch else '@'

        return state.create_new_state(new_map, stone_move)

    def get_next_step(self):
        if not self.solution:
            return None

        self.current_step += 1
        if self.current_step >= len(self.solution):
            return None

        return self.solution[self.current_step]

    def solve_bfs(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        queue = deque([(self.initial_state, [])])
        visited = set()
        operations = 0

        while queue and operations < self.operation_limit:
            operations += 1
            current_state, path = queue.popleft()
            state_string = current_state.to_string()

            if current_state.is_solved():
                self.solution = path
                self.current_step = -1
                return True

            if state_string in visited:
                continue

            visited.add(state_string)
            player_pos = current_state.find_player()

            if not player_pos:
                continue

            x, y = player_pos
            for dx, dy in directions:
                if self.can_move(current_state, x, y, dx, dy):
                    new_state = self.make_move(current_state, x, y, dx, dy)
                    queue.append((new_state, path + [(dx, dy)]))

        return False # Operation limit exceeded or no solution found

    def solve_dfs(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        stack = [(self.initial_state, [])]
        visited = set()
        state_paths = {}
        operations = 0

        while stack and self.operation_limit:
            operations += 1
            current_state, path = stack.pop()
            state_string = current_state.to_string()

            if state_string in state_paths and len(state_paths[state_string]) <= len(path):
                continue

            state_paths[state_string] = path
            visited.add(state_string)

            if current_state.is_solved():
                self.solution = path
                self.current_step = -1
                return True

            player_pos = current_state.find_player()
            if not player_pos:
                continue

            x, y = player_pos
            for dx, dy in directions:
                if self.can_move(current_state, x, y, dx, dy):
                    new_state = self.make_move(current_state, x, y, dx, dy)
                    new_state_string = new_state.to_string()

                    if new_state_string not in state_paths or len(path) + 1 < len(state_paths[new_state_string]):
                        stack.append((new_state, path + [(dx, dy)]))

        return False # Operation limit exceeded or no solution found

 
    def solve_ucs(self):
        # Directions for up, down, left, right movements
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        # Priority queue with initial state (cost, index, state, path)
        priority_queue = [(0, 0, self.initial_state, [])]
        visited = set()
        operations = 0
        index = 0  # Tie-breaker index for heapq

        while priority_queue and operations < self.operation_limit:
            operations += 1
            cost, _, current_state, path = heappop(priority_queue)
            state_string = current_state.to_string()

            if current_state.is_solved():
                self.solution = path
                self.current_step = -1
                return True

            if state_string in visited:
                continue

            visited.add(state_string)
            player_pos = current_state.find_player()

            if not player_pos:
                continue

            x, y = player_pos
            for dx, dy in directions:
                if self.can_move(current_state, x, y, dx, dy):
                    new_state = self.make_move(current_state, x, y, dx, dy)
                    index += 1
                    heappush(priority_queue, (cost + 1, index, new_state, path + [(dx, dy)]))

        return False  # Operation limit exceeded or no solution found
    
    

    def solve_a_star(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        # Priority queue with initial state (f(n), g(n), index, state, path)
        priority_queue = [(0, 0, 0, self.initial_state, [])]
        visited = set()
        operations = 0
        index = 0  # Tie-breaker index for heapq

        while priority_queue and operations < self.operation_limit:
            operations += 1
            f, g, _, current_state, path = heappop(priority_queue)
            state_string = current_state.to_string()

            if current_state.is_solved():
                self.solution = path
                self.current_step = -1
                return True

            if state_string in visited:
                continue

            visited.add(state_string)
            player_pos = current_state.find_player()

            if not player_pos:
                continue

            x, y = player_pos
            for dx, dy in directions:
                if self.can_move(current_state, x, y, dx, dy):
                    new_state = self.make_move(current_state, x, y, dx, dy)
                    new_g = g + 1  # Incremental cost for the move
                    new_h = self.heuristic(new_state)  # Heuristic estimate to goal
                    new_f = new_g + new_h  # Total estimated cost
                    index += 1
                    heappush(priority_queue, (new_f, new_g, index, new_state, path + [(dx, dy)]))

        return False  # Operation limit exceeded or no solution found

    def heuristic(self, state):
        box_positions = state.get_boxes()
        goal_positions = state.get_goals()
        player_pos = state.find_player()

        # Calculate Manhattan distance for each box to its closest goal
        box_goal_distance = sum(
            min(abs(box[0] - goal[0]) + abs(box[1] - goal[1]) for goal in goal_positions)
            for box in box_positions
        )

        # Calculate Manhattan distance from the player to the closest box
        player_box_distance = min(
            abs(player_pos[0] - box[0]) + abs(player_pos[1] - box[1])
            for box in box_positions
        )

        # Combine both distances as the heuristic value
        return box_goal_distance + player_box_distance

