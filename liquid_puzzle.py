class LiquidPuzzle:
    def __init__(self, empty, full, size, colors, initial_state):
        self.empty = empty
        self.full = full
        self.size = size
        self.colors = colors
        self.state = tuple(tuple(tube) for tube in initial_state)

    def is_solved(self, state=None):
        if state is None:
            state = self.state
        for tube in state:
            if tube and (len(tube) != self.size or len(set(tube)) != 1):
                return False
        return True

    def can_move(self, state, from_idx, to_idx, num_colors=1):
        if not state[from_idx] or len(state[to_idx]) + num_colors > self.size:
            return False
        if not state[to_idx]:
            return True
        return all(c == state[to_idx][-1] for c in state[from_idx][-num_colors:])

    def move(self, state, from_idx, to_idx, num_colors=1):
        if self.can_move(state, from_idx, to_idx, num_colors):
            new_state = [list(tube) for tube in state]
            new_state[to_idx].extend(new_state[from_idx][-num_colors:])
            del new_state[from_idx][-num_colors:]
            return tuple(tuple(tube) for tube in new_state)
        return None

    def __str__(self):
        return '\n'.join([' '.join(map(str, tube)) for tube in self.state])
