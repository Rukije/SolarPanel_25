import os
import subprocess

def run_all_instances():
    input_folder = "../input"
    output_folder = "../output"

    for i in range(1, 7):  
        input_file = os.path.join(input_folder, f"instance_{i}.json")
        output_file = os.path.join(output_folder, f"result_{i}.json")

        print(f"Running instance {i}...")
        result = subprocess.run(
            ["python", "main.py", input_file, output_file],
            capture_output=True,
            text=True
        )

        print(result.stdout)
        if result.returncode != 0:
            print(f"Error running instance {i}:")
            print(result.stderr)
        else:
            print(f"Instance {i} completed.\n")

if __name__ == "__main__":
    run_all_instances()
