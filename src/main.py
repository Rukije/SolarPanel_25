import sys
import os
import json
from parser import load_instance
from solver import schedule_robots
from validator import validate_solution
from score import compute_score

def main(input_file, output_file):
    print(f"Loading instance from: {input_file}")
    instance = load_instance(input_file)

    print("Running solver...")
    schedules = schedule_robots(instance)

    print("Validating solution...")
    valid, message = validate_solution(instance, schedules)
    if not valid:
        print(f"Validation failed: {message}")
        return

    score = compute_score(instance, schedules)
    print(f"Solution score: {score}")

    # Save schedules to JSON output
    print(f"Saving output to: {output_file}")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(schedules, f, indent=2)
    print("Done!")

if __name__ == "__main__":
    # Check command line arguments, else use defaults
    if len(sys.argv) == 3:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
    else:
        print("Usage: python main.py <input_file.json> <output_file.json>")
        print("No arguments detected, using default input/output files for demo.")
        input_path = "../input/instance_small.json"  # adjust as needed
        output_path = "../output/result_small.json"  # adjust as needed

    # Run main process
    try:
        main(input_path, output_path)
    except Exception as e:
        print(f"Error during execution: {e}")
