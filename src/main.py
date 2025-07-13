import sys
import json
from parser import load_instance
from solver import schedule_robots

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    instance = load_instance(input_file)
    result = schedule_robots(instance)

    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
