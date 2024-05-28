import heapq
from collections import defaultdict
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
                    score -= 100  # Reward completely filled and uniform tubes
                else:
                    # Prioritize moving colors closer to their correct positions
                    for i in range(len(tube)):
                        if tube[i] != i:
                            distance = abs(tube[i] - i)
                            score += distance * 10
            elif not tube:
                score -= 10  # Reward empty tubes
            else:
                # Penalize tubes with more colors and diverse colors
                score += len(tube) * 5
                score += len(set(tube)) * 2
        return score

    def solve(self):
        start_state = self.initial_state
        frontier = []
        heapq.heappush(frontier, (self.heuristic(start_state), 0, start_state, []))
        visited = defaultdict(lambda: float('inf'))
        num_steps = 0

        while frontier:
            heuristic, cost, state, path = heapq.heappop(frontier)
            if LiquidPuzzle(len(state) - self.size, self.size, self.size, self.size, state).is_solved(state):
                return path, num_steps
            state_str = str(state)
            if cost >= visited[state_str]:  # Prune states with higher cost
                continue
            visited[state_str] = cost
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
                            if new_state:
                                new_cost = cost + 1
                                new_path = path + [(from_idx, to_idx, num_colors)]
                                heapq.heappush(frontier, (self.heuristic(new_state) + new_cost, new_cost, new_state, new_path))
        return None, num_steps
