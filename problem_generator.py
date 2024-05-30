import random
import copy
from liquid_puzzle import LiquidPuzzle


def generate_solvable_puzzle(empty, full, size, colors):
    """
    Generates a solvable puzzle instance.

    Args:
        empty (int): Number of empty tubes.
        full (int): Number of full tubes.
        size (int): Number of colors each tube can hold.
        colors (int): Number of distinct colors.

    Returns:
        tuple: Initial state of the puzzle.
    """
    solved_state = []
    for color in range(colors):
        solved_state.extend([[color] * size])
    solved_state.extend([[] for _ in range(empty)])
    state = copy.deepcopy(solved_state)

    puzzle = LiquidPuzzle(empty, full, size, colors, state)

    for _ in range(100):  # Shuffle 100 moves to create initial state
        from_idx = random.randint(0, len(state) - 1)
        to_idx = random.randint(0, len(state) - 1)
        num_colors = random.randint(1, size)
        if from_idx != to_idx and puzzle.can_move(state, from_idx, to_idx):
            puzzle.move(state, from_idx, to_idx, num_colors)

    return puzzle.state


if __name__ == "__main__":
    initial_state = generate_solvable_puzzle(empty=1, full=4, size=4, colors=4)
    puzzle = LiquidPuzzle(
        empty=1, full=4, size=4, colors=4, initial_state=initial_state
    )
    print("Generated Initial State:")
    print(puzzle)
