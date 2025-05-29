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
