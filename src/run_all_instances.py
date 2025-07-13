import os
import subprocess

def run_all_instances():
    input_folder = "../input"
    output_folder = "../output"

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all .json files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f"result_{os.path.splitext(filename)[0]}.json")

            print(f"Running {filename}...")
            result = subprocess.run(
                ["python", "main.py", input_file, output_file],
                capture_output=True,
                text=True
            )

            print(result.stdout)
            if result.returncode != 0:
                print(f"Error running {filename}:")
                print(result.stderr)
            else:
                print(f"{filename} completed.\n")

if __name__ == "__main__":
    run_all_instances()