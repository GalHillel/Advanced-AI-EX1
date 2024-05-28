import time
import signal
from Instances import instances
from solver import AStarSolver  # Assuming your solver is defined in solver.py

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

def run_tests():
    results = []

    for idx, instance in enumerate(instances):
        print(f"Running test instance {idx}...")
        init_state = instance["init"]
        size = instance["size"]

        solver = AStarSolver(init_state, size)
        start_time = time.time()

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(20)  # Set the alarm for 50 seconds

        try:
            solution, num_steps = solver.solve()
            signal.alarm(0)  # Cancel the alarm
            end_time = time.time()

            runtime = end_time - start_time
            result = {
                "instance": idx,
                "runtime": runtime,
                "num_steps": num_steps,
                "solution_length": len(solution) if solution else None,
                "solution": solution
            }
        except TimeoutException:
            end_time = time.time()
            runtime = end_time - start_time
            result = {
                "instance": idx,
                "runtime": runtime,
                "num_steps": None,
                "solution_length": None,
                "solution": None,
                "timeout": True
            }
            print(f"Test instance {idx} exceeded the time limit of 20 seconds and was stopped.")
            break

        results.append(result)

    for result in results:
        print(f"Instance {result['instance']}:")
        print(f"Runtime: {result['runtime']:.4f} seconds")
        print(f"Number of steps taken: {result['num_steps'] if result['num_steps'] is not None else 'N/A'}")
        print(f"Length of solution: {result['solution_length'] if result['solution_length'] is not None else 'N/A'}")
        print(f"Solution steps: {result['solution'] if result['solution'] is not None else 'N/A'}")
        if result.get('timeout'):
            print("Status: Timeout")
        print("="*50)

if __name__ == "__main__":
    run_tests()
