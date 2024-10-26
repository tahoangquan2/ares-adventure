class GameState:
    def __init__(self, map_data, weight_data):
        self.map = map_data
        self.weight = weight_data
        self.width = len(map_data)
        self.height = len(map_data[0]) if self.width > 0 else 0

    def get_weight(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.weight[x][y]
        return 0

    def find_player(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[x][y] in ['@', '+']:
                    return (x, y)
        return None

    def find_stones(self):
        stones = []
        for y in range(self.height):
            for x in range(self.width):
                if self.map[x][y] in ['$', '*']:
                    stones.append((x, y))
        return stones

    def find_switches(self):
        switches = []
        for y in range(self.height):
            for x in range(self.width):
                if self.map[x][y] in ['.', '*', '+']:
                    switches.append((x, y))
        return switches

    def is_solved(self):
        stones = self.find_stones()
        switches = self.find_switches()
        return all(stone in switches for stone in stones)

    def get_cell(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.map[x][y]
        return '#' # Out of bounds

    def to_string(self):
        return '\n'.join(''.join(row) for row in self.map)

    def create_new_state(self, new_map, stone_move = None):
        new_state = GameState(new_map, [])
        new_state.weight = [[0 for _ in range(self.height)] for _ in range(self.width)]

        # Copy all weights first
        for i in range(self.width):
            for j in range(self.height):
                new_state.weight[i][j] = self.weight[i][j]

        # If a stone was moved, update its position in weight map
        if stone_move:
            (old_x, old_y), (new_x, new_y) = stone_move
            new_state.weight[new_x][new_y] = self.weight[old_x][old_y]
            new_state.weight[old_x][old_y] = 0

        return new_state

    # Check if a stone can be pushed in the given direction
    def can_push_stone(self, x, y, dx, dy):
        # First check if given position is actually a stone
        if self.map[x][y] not in ['$', '*']:
            return False

        # Check the destination position
        new_x, new_y = x + dx, y + dy

        # Check bounds
        if not (0 <= new_y < self.height and 0 <= new_x < self.width):
            return False

        # Check if destination has stone or wall
        if self.map[new_x][new_y] in ['#', '$', '*']:
            return False

        return True
