class GameState:
	def __init__(self, map_data, weights):
		self.map = map_data
		self.height = len(map_data)
		self.width = len(map_data[0]) if self.height > 0 else 0

		# Initialize weight map with zeros
		self.weight_map = [[0 for _ in range(self.width)] for _ in range(self.height)]

		# Fill in weights where stones are located
		stone_index = 0
		for y in range(self.height):
			for x in range(self.width):
				if self.map[y][x] in ['$', '*'] and stone_index < len(weights):
					self.weight_map[y][x] = weights[stone_index]
					stone_index += 1

	def get_weight(self, y, x):
		if 0 <= y < self.height and 0 <= x < self.width:
			return self.weight_map[y][x]
		return 0

	def find_player(self):
		for y in range(self.height):
			for x in range(self.width):
				if self.map[y][x] in ['@', '+']:
					return (y, x)
		return None

	def find_stones(self):
		stones = []
		for y in range(self.height):
			for x in range(self.width):
				if self.map[y][x] in ['$', '*']:
					stones.append((y, x))
		return stones

	def find_switches(self):
		switches = []
		for y in range(self.height):
			for x in range(self.width):
				if self.map[y][x] in ['.', '*', '+']:
					switches.append((y, x))
		return switches

	def is_solved(self):
		stones = self.find_stones()
		switches = self.find_switches()
		return all(stone in switches for stone in stones)

	def get_cell(self, y, x):
		if 0 <= y < self.height and 0 <= x < self.width:
			return self.map[y][x]
		return '#'  # Treat out of bounds as walls

	def to_string(self):
		return '\n'.join(''.join(row) for row in self.map)

	def create_new_state(self, new_map):
		new_state = GameState(new_map, [])

		# Create new weight map
		new_state.weight_map = [[0 for _ in range(self.width)] for _ in range(self.height)]

		# Find stone movements and update weights
		old_stones = self.find_stones()
		new_stones = new_state.find_stones()

		# Copy weights to new positions
		for old_pos, new_pos in zip(old_stones, new_stones):
			old_y, old_x = old_pos
			new_y, new_x = new_pos
			new_state.weight_map[new_y][new_x] = self.weight_map[old_y][old_x]

		return new_state
