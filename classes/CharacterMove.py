class CharacterMove:
    @staticmethod
    def can_move(state, x, y, dx, dy):
        new_x, new_y = x + dx, y + dy

        # Check bounds
        if not (0 <= new_x < state.width and 0 <= new_y < state.height):
            return False

        # Check if moving into a wall
        if (new_x, new_y) in state.walls:
            return False

        # Check if moving into a stone
        if (new_x, new_y) in state.stones:
            return state.can_push_stone(new_x, new_y, dx, dy)

        return True

    @staticmethod
    def make_move(state, x, y, dx, dy):
        new_x, new_y = x + dx, y + dy
        updates = {}

        # Handle stone pushing if needed
        stone_move = None
        if (new_x, new_y) in state.stones:
            push_x, push_y = new_x + dx, new_y + dy
            stone_move = ((new_x, new_y), (push_x, push_y))
            updates['stones'] = stone_move

        # Update player position
        updates['player_pos'] = (new_x, new_y)

        # Create new state with updates
        print("make move")
        return state.create_new_state(updates, stone_move)
