from ..CharacterMove import CharacterMove
from ..GameState import GameState
from heapq import heappop, heappush

class AStarSolver:
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

        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.index = 0
        self.reset_solver()

    def reset_solver(self):
        compressed_initial = self.compress_state(self.initial_state)
        initial_h = self.heuristic(self.initial_state)
        self.priority_queue = [(initial_h, 0, 0, compressed_initial, "")]
        self.visited = {compressed_initial}
        self.index = 0

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

    def heuristic(self, state):
        box_positions = state.get_boxes()
        goal_positions = state.get_goals()

        total_distance = 0
        for box in box_positions:
            min_distance = float('inf')
            box_weight = state.get_weight(box[0], box[1])
            for goal in goal_positions:
                distance = (abs(box[0] - goal[0]) + abs(box[1] - goal[1])) * box_weight
                min_distance = min(min_distance, distance)
            total_distance += min_distance

        return total_distance

    def process_one_state(self):
        if not self.priority_queue:
            return False

        f, g, _, compressed_current, path = heappop(self.priority_queue)
        current_state = self.decompress_state(compressed_current)

        if current_state.is_solved():
            self.solution = [self.char_to_dir[c] for c in path]
            self.current_step = -1
            return True

        x, y = current_state.player_pos
        for dx, dy in self.directions:
            if self.character_move.can_move(current_state, x, y, dx, dy):
                new_state = self.character_move.make_move(current_state, x, y, dx, dy)
                compressed_new = self.compress_state(new_state)

                if compressed_new not in self.visited:
                    self.visited.add(compressed_new)
                    self.index += 1
                    new_g = g + 1
                    new_h = self.heuristic(new_state)
                    new_f = new_g + new_h
                    new_path = path + self.dir_to_char[(dx, dy)]
                    heappush(self.priority_queue, (new_f, new_g, self.index, compressed_new, new_path))

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
