class CharacterMove:
    @staticmethod
    def can_move(state, x, y, dx, dy):
        new_x, new_y = x + dx, y + dy
        target_cell = state.get_cell(new_x, new_y)

        if target_cell == '#':
            return False

        if target_cell in ['$', '*']:
            return state.can_push_stone(new_x, new_y, dx, dy)

        return True

    @staticmethod
    def make_move(state, x, y, dx, dy):
        new_map = [list(row) for row in state.map]
        new_x, new_y = x + dx, y + dy

        current_cell = state.get_cell(x, y)
        is_on_switch = current_cell == '+'

        target_cell = state.get_cell(new_x, new_y)
        target_has_switch = target_cell in ['.', '*', '+']

        new_map[x][y] = '.' if is_on_switch else ' '

        stone_move = None
        if target_cell in ['$', '*']:
            push_x, push_y = new_x + dx, new_y + dy
            push_cell = state.get_cell(push_x, push_y)
            push_has_switch = push_cell in ['.', '*', '+']

            new_map[push_x][push_y] = '*' if push_has_switch else '$'
            stone_move = ((new_x, new_y), (push_x, push_y))

        new_map[new_x][new_y] = '+' if target_has_switch else '@'

        return state.create_new_state(new_map, stone_move)
