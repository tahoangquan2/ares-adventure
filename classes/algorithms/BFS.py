from collections import deque
from ..CharacterMove import CharacterMove

class BFSSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.solution = None
        self.current_step = -1
        self.operation_limit = 10**6
        self.character_move = CharacterMove()

    def state_to_tuple(self, state):
        """Convert a state to a minimal tuple representation
        Returns: tuple(player_pos, ((stone1_pos, weight1), (stone2_pos, weight2), ...))
        """
        stones_tuple = tuple(sorted((pos, weight) for pos, weight in state.stones.items()))
        return (state.player_pos, stones_tuple)

    def solve(self):
        # right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        queue = deque([(self.initial_state, [])])
        visited = set()  # Will store tuples instead of strings
        operations = 0

        while queue and operations < self.operation_limit:
            operations += 1
            current_state, path = queue.popleft()

            # Convert current state to tuple for comparison
            state_tuple = self.state_to_tuple(current_state)

            if state_tuple in visited:
                continue

            if current_state.is_solved():
                self.solution = path
                self.current_step = -1
                return True

            visited.add(state_tuple)  # Add tuple to visited set
            # if operations % 10000 == 0:
            #     print(len(visited), len(queue))
            x, y = current_state.player_pos

            for dx, dy in directions:
                if self.character_move.can_move(current_state, x, y, dx, dy):
                    new_state = self.character_move.make_move(current_state, x, y, dx, dy)
                    queue.append((new_state, path + [(dx, dy)]))

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
