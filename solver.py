import copy
import heapq
import time
from liquid_puzzle import LiquidPuzzle

class AStarSolver:
    def __init__(self, initial_state, size):
        self.initial_state = tuple(tuple(tube) for tube in initial_state)
        self.size = size

    def heuristic(self, state):
        # Heuristic function to estimate distance to goal state
        score = 0
        for tube in state:
            if len(tube) == self.size:
                if len(set(tube)) == 1:
                    score -= 10  # Reward completely filled and uniform tubes
                else:
                    score += 1  # Penalize mixed color tubes
            elif not tube:
                score -= 1  # Reward empty tubes
            else:
                score += len(tube)  # Penalize partial tubes
        return score

    def solve(self):
        start_state = self.initial_state
        frontier = []
        heapq.heappush(frontier, (self.heuristic(start_state), 0, start_state, []))
        visited = set()
        num_steps = 0

        while frontier:
            heuristic, cost, state, path = heapq.heappop(frontier)
            if LiquidPuzzle(len(state) - self.size, self.size, self.size, self.size, state).is_solved(state):
                return path, num_steps
            state_str = str(state)
            if state_str in visited:
                continue
            visited.add(state_str)
            num_steps += 1
            for from_idx in range(len(state)):
                for to_idx in range(len(state)):
                    if from_idx != to_idx:
                        if not state[from_idx]:
                            continue  # Skip empty tubes
                        colors = [state[from_idx][-1]]
                        for color in reversed(state[from_idx][:-1]):
                            if color == colors[-1]:
                                colors.append(color)
                            else:
                                break
                        for num_colors in range(1, min(self.size - len(state[to_idx]), len(colors)) + 1):
                            puzzle = LiquidPuzzle(len(state) - self.size, self.size, self.size, self.size, state)
                            new_state = puzzle.move(state, from_idx, to_idx, num_colors)
                            if new_state and str(new_state) not in visited:
                                new_path = path + [(from_idx, to_idx, num_colors)]
                                heapq.heappush(frontier, (self.heuristic(new_state) + cost + 1, cost + 1, new_state, new_path))
        return None, num_steps



if __name__ == "__main__":
    # Given puzzle instance
    empty = 4
    full = 10
    size = 10
    colors = 10
    init = [[], [], [2, 2, 0, 0, 7, 3, 1, 1, 9, 0], [3, 3, 9, 7, 2, 8, 4, 0, 3, 6], [3, 5, 8, 5, 7, 0, 2, 9, 0, 0], [5, 0, 6, 4, 9, 2, 3, 7, 3, 9], [6, 4, 4, 9, 3, 1, 3, 3, 4, 4], [5, 7, 6, 7, 1, 8, 7, 2, 1, 7], [6, 8, 8, 4, 2, 6, 4, 5, 8, 1], [9, 9, 1, 7, 5, 0, 5, 1, 9, 1], [2, 5, 8, 1, 2, 4, 6, 7, 4, 6], [5, 0, 6, 8, 8, 5, 6, 8, 9, 2]]
    solver = AStarSolver(init, size=size)

    # Measure runtime
    start_time = time.time()
    solution, num_steps = solver.solve()
    end_time = time.time()
    runtime = end_time - start_time

    if solution is not None:
        print("Solution found!")
        print(f"Runtime: {runtime:.4f} seconds")
        print(f"Number of steps taken: {num_steps}")
        print(f"Length of solution: {len(solution)}")
        print("Solution steps:", solution)

        # Apply the solution to get the final state
        puzzle = LiquidPuzzle(empty=empty, full=full, size=size, colors=colors, initial_state=copy.deepcopy(init))
        for move in solution:
            puzzle.state = puzzle.move(puzzle.state, *move)
        
        print("Solved Puzzle State:")
        print(puzzle)
    else:
        print("No solution found.")
