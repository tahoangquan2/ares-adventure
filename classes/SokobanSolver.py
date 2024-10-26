from collections import deque

class SokobanSolver:
	def __init__(self, initial_state):
		self.initial_state = initial_state
		self.solution = None
		self.current_step = -1
		self.operation_limit = 5

	def can_move(self, state, y, x, dy, dx):
		new_y, new_x = y + dy, x + dx
		target_cell = state.get_cell(new_y, new_x)

		if target_cell == '#':
			return False

		if target_cell in ['$', '*']:
			# Check if we can push the stone
			push_y, push_x = new_y + dy, new_x + dx
			push_cell = state.get_cell(push_y, push_x)
			return push_cell not in ['#', '$', '*']

		return True

	def make_move(self, state, y, x, dy, dx):
		new_map = [list(row) for row in state.map]
		new_y, new_x = y + dy, x + dx

		# Get the current cell type (with or without switch)
		current_cell = state.get_cell(y, x)
		is_on_switch = current_cell == '+'

		# Get the target cell type
		target_cell = state.get_cell(new_y, new_x)
		target_has_switch = target_cell in ['.', '*', '+']

		# Update the player's current position
		new_map[y][x] = '.' if is_on_switch else ' '

		if target_cell in ['$', '*']:
			# Moving a stone
			push_y, push_x = new_y + dy, new_x + dx
			push_cell = state.get_cell(push_y, push_x)
			push_has_switch = push_cell in ['.', '*', '+']

			# Update the stone's position
			new_map[push_y][push_x] = '*' if push_has_switch else '$'

		# Update the player's new position
		new_map[new_y][new_x] = '+' if target_has_switch else '@'

		return state.create_new_state(new_map)

	def solve_bfs(self):
		directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
		queue = deque([(self.initial_state, [])])
		visited = set()
		operations = 0

		while queue and operations < self.operation_limit:
			operations += 1
			current_state, path = queue.popleft()
			state_string = current_state.to_string()

			if current_state.is_solved():
				self.solution = path
				self.current_step = -1
				return True

			if state_string in visited:
				continue

			visited.add(state_string)
			player_pos = current_state.find_player()

			if not player_pos:
				continue

			y, x = player_pos
			for dy, dx in directions:
				if self.can_move(current_state, y, x, dy, dx):
					new_state = self.make_move(current_state, y, x, dy, dx)
					queue.append((new_state, path + [(dy, dx)]))

		return False  # Operation limit exceeded or no solution found

	def solve_dfs(self):
		directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
		stack = [(self.initial_state, [])]
		visited = set()
		state_paths = {}
		operations = 0

		while stack and self.operation_limit:
			operations += 1
			current_state, path = stack.pop()
			state_string = current_state.to_string()

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

			y, x = player_pos
			for dy, dx in directions:
				if self.can_move(current_state, y, x, dy, dx):
					new_state = self.make_move(current_state, y, x, dy, dx)
					new_state_string = new_state.to_string()

					if new_state_string not in state_paths or len(path) + 1 < len(state_paths[new_state_string]):
						stack.append((new_state, path + [(dy, dx)]))

		return False  # Operation limit exceeded or no solution found

	def get_next_step(self):
		if not self.solution:
			return None

		self.current_step += 1
		if self.current_step >= len(self.solution):
			return None

		return self.solution[self.current_step]
