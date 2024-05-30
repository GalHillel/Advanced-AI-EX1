class LiquidPuzzle:
    def __init__(self, empty, full, size, colors, initial_state):
        """
        Initializes the LiquidPuzzle instance.

        Args:
            empty (int): Number of empty tubes.
            full (int): Number of full tubes.
            size (int): Number of colors each tube can hold.
            colors (int): Number of distinct colors.
            initial_state (list): Initial state of the puzzle.
        """
        self.empty = empty
        self.full = full
        self.size = size
        self.colors = colors
        self.state = tuple(tuple(tube) for tube in initial_state)

    def is_solved(self, state=None):
        """
        Checks if the puzzle is solved.

        Args:
            state (tuple): Current state of the puzzle.

        Returns:
            bool: True if the puzzle is solved, False otherwise.
        """
        if state is None:
            state = self.state
        for tube in state:
            if tube and (len(tube) != self.size or len(set(tube)) != 1):
                return False
        return True

    def can_move(self, state, from_idx, to_idx):
        """
        Checks if a move is possible.

        Args:
            state (tuple): Current state of the puzzle.
            from_idx (int): Index of the tube to move from.
            to_idx (int): Index of the tube to move to.

        Returns:
            bool: True if the move is possible, False otherwise.
        """
        if not state[from_idx] or len(state[to_idx]) >= self.size:
            return False
        if not state[to_idx]:
            return True
        return (
            state[to_idx][-1] == state[from_idx][-1] and len(state[to_idx]) < self.size
        )

    def move(self, state, from_idx, to_idx):
        """
        Executes a move if possible.

        Args:
            state (tuple): Current state of the puzzle.
            from_idx (int): Index of the tube to move from.
            to_idx (int): Index of the tube to move to.

        Returns:
            tuple: New state after the move, and move details.
        """
        if self.can_move(state, from_idx, to_idx):
            new_state = [list(tube) for tube in state]
            move_color = new_state[from_idx][-1]
            move_count = 1
            for color in reversed(new_state[from_idx][:-1]):
                if color == move_color:
                    move_count += 1
                else:
                    break
            move_count = min(move_count, self.size - len(new_state[to_idx]))
            new_state[to_idx].extend(new_state[from_idx][-move_count:])
            new_state[from_idx] = new_state[from_idx][:-move_count]
            return tuple(tuple(tube) for tube in new_state), (
                from_idx,
                to_idx,
                move_count,
            )
        return None, None
