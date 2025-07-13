import os
import json


def compute_score(instance, schedules):
    panel_importance = instance['panel_importance']

    cleaned_panels = set()
    # Collect all cleaned panels from schedules
    for robot_schedule in schedules.values():
        for task in robot_schedule:
            if task['action'] == 'clean':
                cleaned_panels.add(task['panel'])

    base_score = sum(panel_importance[p] for p in cleaned_panels)

    # Example cluster bonus: reward cleaning adjacent panels by same robot consecutively
    cluster_bonus = 0
    for robot_schedule in schedules.values():
        robot_schedule = sorted(robot_schedule, key=lambda x: x['start_time'])
        for i in range(1, len(robot_schedule)):
            prev_panel = robot_schedule[i-1]['panel']
            curr_panel = robot_schedule[i]['panel']
            # Simple adjacency check: panels differ by 1 index (assume line)
            if abs(curr_panel - prev_panel) == 1:
                cluster_bonus += 5  # arbitrary bonus points

    total_score = base_score + cluster_bonus
    return total_score


if __name__ == "__main__":
    input_folder = "../input"
    output_folder = "../output"

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_file = os.path.join(input_folder, filename)
            result_file = os.path.join(output_folder, f"result_{os.path.splitext(filename)[0]}.json")

            if not os.path.exists(result_file):
                print(f"Result file not found for {filename}")
                continue

            with open(input_file) as f:
                instance = json.load(f)
            with open(result_file) as f:
                result = json.load(f)

            schedules = result.get("schedules", {})
            score = compute_score(instance, schedules)
            print(f"{filename}: Score = {score}")
