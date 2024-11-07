from ..CharacterMove import CharacterMove
from ..GameState import GameState
from ..AlgorithmMetrics import AlgorithmMetrics
from heapq import heappop, heappush

class UCSSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.solution = None
        self.current_step = -1
        self.operation_limit = 10**6
        self.character_move = CharacterMove()
        self.dir_to_char = {
            (0, 1): 'D', (1, 0): 'R',
            (0, -1): 'U', (-1, 0): 'L'
        }
        self.char_to_dir = {
            'D': (0, 1), 'U': (0, -1), 'L': (-1, 0), 'R': (1, 0),
            'd': (0, 1), 'u': (0, -1), 'l': (-1, 0), 'r': (1, 0)
        }

        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.index = 0
        self.metrics = AlgorithmMetrics()
        self.reset_solver()

    def reset_solver(self):
        compressed_initial = self.compress_state(self.initial_state)
        # Initialize with (cost, index, state, path, total_weight)
        self.priority_queue = [(0, 0, compressed_initial, "", 0)]
        self.visited = {compressed_initial}
        self.index = 0
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
        if not self.priority_queue:
            return False

        cost, _, compressed_current, path, total_weight = heappop(self.priority_queue)
        current_state = self.decompress_state(compressed_current)
        self.metrics.nodes_explored += 1

        # Update peak memory after processing each state
        self.metrics.update_peak_memory()

        if current_state.is_solved():
            self.solution = [self.char_to_dir[c] for c in path]
            self.current_step = -1
            self.metrics.stop_tracking()
            self.metrics.total_steps = len(path)
            self.metrics.total_weight = total_weight
            self.metrics.solution_path = path
            return True

        x, y = current_state.player_pos
        for dx, dy in self.directions:
            if self.character_move.can_move(current_state, x, y, dx, dy):
                new_state = self.character_move.make_move(current_state, x, y, dx, dy)
                compressed_new = self.compress_state(new_state)

                if compressed_new not in self.visited:
                    self.visited.add(compressed_new)

                    # Determine if this move is a push
                    new_pos = (x + dx, y + dy)
                    is_push = new_pos in current_state.stones

                    # Get the direction character
                    dir_char = self.dir_to_char[(dx, dy)]
                    dir_char = dir_char.upper() if is_push else dir_char.lower()
                    new_path = path + dir_char

                    # Calculate weight
                    move_weight = 1
                    if is_push:
                        move_weight += current_state.get_weight(*new_pos)

                    new_total_weight = total_weight + move_weight
                    heappush(self.priority_queue, (new_total_weight, self.index, compressed_new, new_path, new_total_weight))

        return False

    def solve(self):
        self.reset_solver()
        operations = 0

        while operations < self.operation_limit:
            operations += 1
            if self.process_one_state():
                return True
            if not self.priority_queue:
                return False

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

    def save_metrics(self, level_number):
        self.metrics.save_to_file("UCS", level_number)
