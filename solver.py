from liquid_puzzle import LiquidPuzzle
import heapq
import itertools


class AStarSolver:
    def __init__(self, initial_state, size):
        """
        Initializes the AStarSolver instance.

        Args:
            initial_state (list): Initial state of the puzzle.
            size (int): Number of colors each tube can hold.
        """
        self.initial_state = tuple(map(tuple, initial_state))
        self.size = size

    def heuristic(self, state):
        """
        Calculates the heuristic score for a given state.

        Args:
            state (tuple): Current state of the puzzle.

        Returns:
            int: Heuristic score.
        """
        score = 0
        for tube in state:
            if tube:
                unique_colors = len(set(tube))
                non_consecutive = sum(
                    1 for i in range(len(tube) - 1) if tube[i] != tube[i + 1]
                )
                if len(tube) == self.size and unique_colors == 1:
                    score -= 10
                score += unique_colors * 3 + non_consecutive * 2
        return score

    def solve(self):
        """
        Solves the puzzle using the A* algorithm.

        Returns:
            tuple: Solution path and number of steps taken.
        """
        start_state = self.initial_state
        frontier = [(self.heuristic(start_state), 0, start_state, [])]
        visited = set()
        num_steps = 0

        while frontier:
            _, cost, state, path = heapq.heappop(frontier)
            if LiquidPuzzle(
                len(state) - self.size, self.size, self.size, self.size, state
            ).is_solved(state):
                return path, num_steps
            state_str = str(state)
            if state_str in visited:
                continue
            visited.add(state_str)
            num_steps += 1

            for from_idx, to_idx in itertools.permutations(range(len(state)), 2):
                if state[from_idx]:
                    puzzle = LiquidPuzzle(
                        len(state) - self.size, self.size, self.size, self.size, state
                    )
                    new_state, move_details = puzzle.move(state, from_idx, to_idx)
                    if new_state:
                        new_cost = cost + 1
                        new_path = path + [move_details]
                        heapq.heappush(
                            frontier,
                            (
                                self.heuristic(new_state) + new_cost,
                                new_cost,
                                new_state,
                                new_path,
                            ),
                        )
        return None, num_steps
