from visualization import visualize_robot_activity
import json

# Sample function to load instance data (you should replace this with actual logic for your project)
def load_instance(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    # Load your instance data (replace 'input.json' with your actual input file)
    instance = load_instance("../input/instance_0.json")
    robots = instance['robots']
    schedules = {
        # Example: Add the actual schedules for robots here
        0: [{'start_time': 0, 'end_time': 3, 'panel': 1, 'action': 'clean'}],
        1: [{'start_time': 3, 'end_time': 6, 'panel': 2, 'action': 'clean'}]
    }
    T = 10  # Maximum available time for scheduling

    # Visualize and save the output
    visualize_robot_activity(robots, schedules, T, save=True, filename="robot_activity_output.png")

if __name__ == "__main__":
    main()
