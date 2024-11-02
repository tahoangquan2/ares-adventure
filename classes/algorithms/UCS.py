from collections import deque
from ..CharacterMove import CharacterMove
from heapq import heappop, heappush

class UCSSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.solution = None
        self.current_step = -1
        self.operation_limit = 10**6
        self.character_move = CharacterMove()
        self.node_count = 0  

    def solve(self):
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
                    self.node_count += 1  # Tăng node_count mỗi khi thêm một trạng thái mới

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
