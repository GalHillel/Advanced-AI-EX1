import json
import time
import signal
from solver import AStarSolver
from Instances import instances


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    """
    Signal handler for timeouts.

    Args:
        signum (int): Signal number.
        frame (frame): Current stack frame.
    """
    raise TimeoutException


def run_tests(instances):
    """
    Runs test instances and logs results.

    Args:
        instances (list): List of test instances.
    """
    results = []

    for idx, instance in enumerate(instances):
        print(f"Running test instance {idx}...")
        init_state = instance["init"]
        size = instance["size"]

        solver = AStarSolver(init_state, size)
        start_time = time.time()

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(600)  # Set the alarm for 600 seconds

        try:
            solution, num_steps = solver.solve()
            signal.alarm(0)  # Cancel the alarm
            end_time = time.time()

            runtime = end_time - start_time
            solution_length = len(solution) if solution else 0
            solution_steps = solution if solution else "N/A"
            result = {
                "instance": idx,
                "runtime": runtime,
                "num_steps": num_steps,
                "solution_length": solution_length,
                "solution": solution_steps,
            }
            print(f"Instance {idx}:")
            print(f"Runtime: {runtime:.4f} seconds")
            print(
                f"Number of steps taken: {num_steps if num_steps is not None else 'N/A'}"
            )
            print(
                f"Length of solution: {solution_length if solution_length > 0 else 'N/A'}"
            )
            print(f"Solution steps: {solution_steps}")
            print("=" * 50)
        except TimeoutException:
            end_time = time.time()
            runtime = end_time - start_time
            result = {
                "instance": idx,
                "runtime": runtime,
                "num_steps": None,
                "solution_length": None,
                "solution": None,
                "timeout": True,
            }
            print(
                f"Test instance {idx} exceeded the time limit of 600 seconds and was stopped."
            )
            print("=" * 50)

        results.append(result)
        with open("results.txt", "w") as file:
            for result in results:
                if isinstance(result["solution"], list):
                    result["solution"] = json.dumps(
                        result["solution"]
                    )  # Convert solution to a JSON string
            json.dump(results, file, indent=4)


if __name__ == "__main__":
    run_tests(instances)
