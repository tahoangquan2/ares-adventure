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

    def hash_state(self, state):
        """Convert state to a single hash value"""
        x, y = state.player_pos
        hash_val = (x << 8) | y

        for (stone_x, stone_y), weight in sorted(state.stones.items()):
            hash_val = (hash_val << 24) | (stone_x << 16) | (stone_y << 8) | weight

        return hash_val

    def solve(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

        # Get initial state hash and add to visited immediately
        initial_hash = self.hash_state(self.initial_state)
        visited = {initial_hash}
        queue = deque([(self.initial_state, [])])
        operations = 0

        while queue and operations < self.operation_limit:
            operations += 1
            current_state, path = queue.popleft()

            if current_state.is_solved():
                self.solution = path
                self.current_step = -1
                return True

            x, y = current_state.player_pos
            for dx, dy in directions:
                if self.character_move.can_move(current_state, x, y, dx, dy):
                    new_state = self.character_move.make_move(current_state, x, y, dx, dy)
                    new_hash = self.hash_state(new_state)

                    # Check and mark as visited before adding to queue
                    if new_hash not in visited:
                        visited.add(new_hash)  # Mark as visited immediately
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
