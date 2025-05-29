def can_clean_panel(robot, energy_left, cleaning_time):
    return energy_left >= cleaning_time

def reset_energy(robot):
    return robot["energy_capacity"]

def sort_panels_by_score(panel_scores):
    return sorted(enumerate(panel_scores), key=lambda x: -x[1])

def print_schedule(schedule):
    for robot in schedule:
        print(f"Robot {robot['robot_id']}:")
        for task in robot['tasks']:
            print(f"  Day {task['day']}, Panel {task['panel_id']}")
