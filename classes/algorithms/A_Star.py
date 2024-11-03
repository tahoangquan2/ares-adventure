from collections import deque
from ..CharacterMove import CharacterMove
from heapq import heappop, heappush

class AStarSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.solution = None
        self.current_step = -1
        self.operation_limit = 10**6
        self.character_move = CharacterMove()
        self.node_count = 0  

    def solve(self):
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
                    self.node_count += 1  

        return False  # Operation limit exceeded or no solution found

    def can_move(self, state, x, y, dx, dy):
        return self.character_move.can_move(state, x, y, dx, dy)

    def make_move(self, state, x, y, dx, dy):
        return self.character_move.make_move(state, x, y, dx, dy)

    def get_next_step(self):
        if not self.solution:
            return None

        self.current_step += 1
        if self.current_step >= len(self.solution):
            return None

        return self.solution[self.current_step]
    
    def heuristic(self, state):
        box_positions = state.get_boxes()
        goal_positions = state.get_goals()

        # Calculate Manhattan distance for each box to its closest goal, factoring in weights
        box_goal_distance = sum(
            min((abs(box[0] - goal[0]) + abs(box[1] - goal[1])) * state.get_weight(box[0], box[1]) for goal in goal_positions)
            for box_index, box in enumerate(box_positions)
        )

        return box_goal_distance