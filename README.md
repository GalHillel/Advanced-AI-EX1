# Liquid Puzzle Solver

## Introduction
This project implements a solver for the Liquid Puzzle game using the A* algorithm. The game involves moving colors between test tubes to achieve a state where each test tube contains only one color.

## Files

### `liquid_puzzle.py`
This file defines the `LiquidPuzzle` class, which represents the state of the puzzle and provides methods for moving colors between test tubes.

### `problem_generator.py`
This file includes a function to generate random, solvable initial states for the puzzle by starting from a solved state and performing random moves.

### `solver.py`
This file implements the A* algorithm to solve the puzzle. It includes an improved heuristic to guide the search more efficiently.

### `README.md`
This file provides an overview of the project, instructions for running the code, and explanations of the implemented methods.

## How to Run

1. **Running the `liquid_puzzle.py` for Manual Control**:
    ```bash
    python liquid_puzzle.py
    ```
   This will initialize a puzzle and demonstrate a manual move.

2. **Running the `problem_generator.py` to Generate a Random Puzzle**:
    ```bash
    python problem_generator.py
    ```
   This will generate a random but solvable initial state for the puzzle.

3. **Running the `solver.py` to Solve a Given Puzzle**:
    ```bash
    python solver.py
    ```
   This will solve the given puzzle instance and print the runtime, number of steps, length of the solution, and the solved puzzle state.

## Explanation

### LiquidPuzzle Class
- **Initialization**: The puzzle is initialized with a given number of empty and full test tubes, the size of each test tube, and the initial state.
- **Move Method**: Colors can be moved from one test tube to another if the move is valid. The validity check ensures there is enough space and that colors can only be moved onto identical colors or empty spaces.
- **Solving Check**: The puzzle is considered solved when each test tube contains only one color.

### AStarSolver Class
- **Heuristic Function**: The heuristic function rewards fully sorted tubes and penalizes mixed tubes to guide the search more effectively.
- **Solve Method**: The A* algorithm is used to find the optimal solution. The search explores possible moves and uses the heuristic to prioritize promising states.

## Variables
You can easily modify the puzzle parameters by changing the following variables in `solver.py`:
- `empty`: Number of empty test tubes.
- `full`: Number of full test tubes.
- `size`: Size of each test tube.
- `colors`: Number of different colors.
- `init`: Initial state of the puzzle.

## Example
The provided example in `solver.py` demonstrates solving the following puzzle:
```python
empty = 1
full = 3
size = 3
colors = 3
init = [[], [0, 1, 1], [2, 0, 1], [0, 2, 2]]
