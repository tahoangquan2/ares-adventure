class GameState:
    def __init__(self, map_data=None, weight_data=None):
        # If initialized with map_data, convert from string representation
        if map_data:
            self.width = len(map_data)
            self.height = len(map_data[0]) if self.width > 0 else 0
            self._init_from_map(map_data, weight_data)
        else:
            self.width = 0
            self.height = 0
            self.walls = set()  # Set of (x, y) wall positions
            self.switches = set()  # Set of (x, y) switch positions
            self.stones = {}  # Dictionary of (x, y) -> weight for stones
            self.player_pos = None  # (x, y) tuple for player position
            self.player_on_switch = False

    def _init_from_map(self, map_data, weight_data):
        self.walls = set()
        self.switches = set()
        self.stones = {}
        self.player_pos = None
        self.player_on_switch = False

        weight_idx = 0
        for x in range(self.width):
            for y in range(self.height):
                cell = map_data[x][y]
                if cell == '#':
                    self.walls.add((x, y))
                elif cell == '.':
                    self.switches.add((x, y))
                elif cell in ['$', '*']:
                    weight = weight_data[x][y] if weight_data else 1
                    self.stones[(x, y)] = weight
                    if cell == '*':
                        self.switches.add((x, y))
                elif cell == '@':
                    self.player_pos = (x, y)
                elif cell == '+':
                    self.player_pos = (x, y)
                    self.player_on_switch = True
                    self.switches.add((x, y))

    def get_weight(self, x, y):
        return self.stones.get((x, y), 0)

    def find_player(self):
        return self.player_pos

    def find_stones(self):
        return list(self.stones.keys())

    def find_switches(self):
        return list(self.switches)

    def is_solved(self):
        return all(pos in self.switches for pos in self.stones.keys())

    def get_cell(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return '#'

        pos = (x, y)
        if pos in self.walls:
            return '#'
        elif pos in self.stones:
            return '*' if pos in self.switches else '$'
        elif pos == self.player_pos:
            return '+' if self.player_on_switch else '@'
        elif pos in self.switches:
            return '.'
        return ' '

    def to_string(self):
        """Returns a minimal string representation containing only essential state information:
        format: "px py s1x s1y s1w s2x s2y s2w ..." where:
        - px py: player position coordinates
        - sNx sNy: stone N position coordinates
        - sNw: stone N weight
        """
        # Start with player position
        parts = [str(self.player_pos[0]), str(self.player_pos[1])]

        # Add stone positions and weights, sorted to ensure consistent representation
        stone_data = []
        for pos, weight in sorted(self.stones.items()):
            stone_data.extend([str(pos[0]), str(pos[1]), str(weight)])

        return ' '.join(parts + stone_data)

    def __eq__(self, other):
        """Implement equality check for states"""
        if not isinstance(other, GameState):
            return False
        return (self.player_pos == other.player_pos and
                self.stones == other.stones)

    def __hash__(self):
        """Implement hash for use in sets and as dictionary keys"""
        # Convert stones dict to tuple of tuples for hashing
        stones_tuple = tuple(sorted((pos, weight) for pos, weight in self.stones.items()))
        return hash((self.player_pos, stones_tuple))

    def create_new_state(self, updates, stone_move=None):
        new_state = GameState()
        new_state.width = self.width
        new_state.height = self.height
        new_state.walls = self.walls.copy()
        new_state.switches = self.switches.copy()
        new_state.stones = self.stones.copy()
        new_state.player_pos = self.player_pos
        new_state.player_on_switch = self.player_on_switch

        # Apply updates
        if 'player_pos' in updates:
            new_pos = updates['player_pos']
            new_state.player_pos = new_pos
            new_state.player_on_switch = new_pos in new_state.switches

        if 'stones' in updates:
            old_pos, new_pos = updates['stones']
            if old_pos in new_state.stones:
                weight = new_state.stones.pop(old_pos)
                new_state.stones[new_pos] = weight

        return new_state

    def can_push_stone(self, x, y, dx, dy):
        pos = (x, y)
        if pos not in self.stones:
            return False

        new_pos = (x + dx, y + dy)

        # Check bounds
        if not (0 <= new_pos[0] < self.width and 0 <= new_pos[1] < self.height):
            return False

        # Check if destination has wall or another stone
        if new_pos in self.walls or new_pos in self.stones:
            return False

        return True

    def get_boxes(self):
        return list(self.stones.keys())

    def get_goals(self):
        return list(self.switches)
