class GameState:
	def __init__(self, map_data, weights):
		self.map = map_data
		self.height = len(map_data)
		self.width = len(map_data[0]) if self.height > 0 else 0

		# Initialize stone positions and weights
		self.stone_weights = {}
		stone_index = 0
		for y in range(self.height):
			for x in range(self.width):
				if self.map[y][x] in ['$', '*']:
					if stone_index < len(weights):
						self.stone_weights[(y, x)] = weights[stone_index]
						stone_index += 1

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
		new_state = GameState(new_map, [])  # Pass empty weights as we'll copy the dictionary
		new_state.stone_weights = {}

		# Update stone positions while maintaining their weights
		old_positions = list(self.stone_weights.keys())
		old_weights = list(self.stone_weights.values())

		# Find new stone positions
		new_positions = []
		for y in range(len(new_map)):
			for x in range(len(new_map[0])):
				if new_map[y][x] in ['$', '*']:
					new_positions.append((y, x))

		# Match old stones to new positions
		for i in range(len(old_weights)):
			if i < len(new_positions):
				new_state.stone_weights[new_positions[i]] = old_weights[i]

		return new_state
