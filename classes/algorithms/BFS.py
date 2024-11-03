from collections import deque
from ..CharacterMove import CharacterMove

class BFSSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.solution = None
        self.current_step = -1
        self.operation_limit = 10**6
        self.character_move = CharacterMove()
        self.node_count = 0  

    def solve(self):
        # right, down, left, up
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
                if self.character_move.can_move(current_state, x, y, dx, dy):
                    new_state = self.character_move.make_move(current_state, x, y, dx, dy)
                    queue.append((new_state, path + [(dx, dy)]))
                    self.node_count += 1  

        # Operation limit exceeded or no solution found
        return False

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
