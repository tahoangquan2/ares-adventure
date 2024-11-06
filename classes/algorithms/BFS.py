from collections import deque
from ..CharacterMove import CharacterMove
from ..GameState import GameState
import asyncio

class BFSSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.solution = None
        self.current_step = -1
        self.operation_limit = 10**6
        self.character_move = CharacterMove()
        self.dir_to_char = {
            (0, 1): 'R',   # right
            (1, 0): 'D',   # down
            (0, -1): 'L',  # left
            (-1, 0): 'U'   # up
        }
        self.char_to_dir = {v: k for k, v in self.dir_to_char.items()}

        # Initialize solver state
        self.queue = deque()
        self.visited = set()
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.reset_solver()

    def reset_solver(self):
        """Reset solver to initial state"""
        compressed_initial = self.compress_state(self.initial_state)
        self.queue = deque([(compressed_initial, "")])
        self.visited = {compressed_initial}

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
        """Process one state from the queue. Returns True if solution found."""
        if not self.queue:
            return False

        compressed_current, path = self.queue.popleft()
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
                    new_path = path + self.dir_to_char[(dx, dy)]
                    if len(self.queue) % 1000 == 0:
                        print(len(self.queue), compressed_new, new_path)
                    self.queue.append((compressed_new, new_path))

        return False

    async def solve_async(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        compressed_initial = self.compress_state(self.initial_state)
        visited = {compressed_initial}
        queue = deque([(compressed_initial, "")])
        operations = 0
        chunk_size = 1000  # Process this many states before yielding

        while queue and operations < self.operation_limit:
            # Process a chunk of states
            for _ in range(chunk_size):
                if not queue or operations >= self.operation_limit:
                    break

                operations += 1
                compressed_current, path = queue.popleft()
                current_state = self.decompress_state(compressed_current)

                if current_state.is_solved():
                    self.solution = [self.char_to_dir[c] for c in path]
                    self.current_step = -1
                    yield {'solved': True, 'operations': operations}
                    return

                x, y = current_state.player_pos
                for dx, dy in directions:
                    if self.character_move.can_move(current_state, x, y, dx, dy):
                        new_state = self.character_move.make_move(current_state, x, y, dx, dy)
                        compressed_new = self.compress_state(new_state)

                        if compressed_new not in visited:
                            visited.add(compressed_new)
                            new_path = path + self.dir_to_char[(dx, dy)]
                            queue.append((compressed_new, new_path))

            # Yield control after processing the chunk
            yield {'solved': False, 'operations': operations}
            await asyncio.sleep(0)

        yield {'solved': False, 'operations': operations}

    def solve(self):
        """Original synchronous solve method"""
        self.reset_solver()
        operations = 0

        while self.queue and operations < self.operation_limit:
            operations += 1
            if self.process_one_state():
                return True

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
