from ..CharacterMove import CharacterMove

class DFSSolver:
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
        stack = [(self.initial_state, [])]
        visited = set()
        state_paths = {}
        operations = 0

        while stack and operations < self.operation_limit:
            operations += 1
            current_state, path = stack.pop()
            state_string = current_state.to_string()

            # Check if we already found a shorter path to this state
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
                if self.character_move.can_move(current_state, x, y, dx, dy):
                    new_state = self.character_move.make_move(current_state, x, y, dx, dy)
                    new_state_string = new_state.to_string()

                    # Only add to stack if we haven't found this state yet or if this path is shorter
                    if new_state_string not in state_paths or len(path) + 1 < len(state_paths[new_state_string]):
                        stack.append((new_state, path + [(dx, dy)]))
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
