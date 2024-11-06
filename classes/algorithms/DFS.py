from ..CharacterMove import CharacterMove
from ..GameState import GameState
from ..AlgorithmMetrics import AlgorithmMetrics

class DFSSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.solution = None
        self.current_step = -1
        self.operation_limit = 10**6
        self.character_move = CharacterMove()
        self.dir_to_char = {
            (0, 1): 'R', (1, 0): 'D',
            (0, -1): 'L', (-1, 0): 'U'
        }
        self.char_to_dir = {v: k for k, v in self.dir_to_char.items()}

        self.metrics = AlgorithmMetrics()
        self.stack = []
        self.visited = set()
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.reset_solver()

    def reset_solver(self):
        compressed_initial = self.compress_state(self.initial_state)
        self.stack = [(compressed_initial, "", 0)]
        self.visited = {compressed_initial}
        self.metrics = AlgorithmMetrics()
        self.metrics.start_tracking()

    def compress_state(self, state):
        stones = tuple(sorted((pos, weight) for pos, weight in state.stones.items()))
        return (state.player_pos, stones)

    def decompress_state(self, compressed):
        player_pos, stones = compressed
        new_state = GameState()
        new_state.width = self.initial_state.width
        new_state.height = self.initial_state.height
        new_state.walls = self.initial_state.walls
        new_state.switches = self.initial_state.switches
        new_state.player_pos = player_pos
        new_state.stones = dict(stones)
        new_state.player_on_switch = player_pos in new_state.switches
        return new_state

    def process_one_state(self):
        if not self.stack:
            return False

        compressed_current, path, current_weight = self.stack.pop()
        current_state = self.decompress_state(compressed_current)
        self.metrics.nodes_explored += 1

        # Update peak memory after processing each state
        self.metrics.update_peak_memory()

        if current_state.is_solved():
            self.solution = [self.char_to_dir[c] for c in path]
            self.current_step = -1
            self.metrics.stop_tracking()
            self.metrics.total_steps = len(path)
            self.metrics.total_weight = current_weight
            self.metrics.solution_path = path
            return True

        x, y = current_state.player_pos
        for dx, dy in self.directions:
            if self.character_move.can_move(current_state, x, y, dx, dy):
                new_state = self.character_move.make_move(current_state, x, y, dx, dy)
                compressed_new = self.compress_state(new_state)

                if compressed_new not in self.visited:
                    self.visited.add(compressed_new)
                    new_path = path + self.dir_to_char[(dx, dy)]

                    # Calculate weight for this move
                    additional_weight = 1
                    new_pos = (x + dx, y + dy)
                    if new_pos in current_state.stones:
                        additional_weight += current_state.get_weight(*new_pos)
                    self.stack.append((compressed_new, new_path, current_weight + additional_weight))

        return False

    def solve(self):
        self.reset_solver()
        operations = 0

        while self.stack and operations < self.operation_limit:
            operations += 1
            if self.process_one_state():
                return True

        return False

    def save_metrics(self, level_number):
        self.metrics.save_to_file("DFS", level_number)

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
