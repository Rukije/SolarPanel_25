def validate_solution(instance, schedules):
    N = instance['N']
    T = instance['T']
    cleaning_times = instance['cleaning_times']
    robots = instance['robots']

    # Check no simultaneous cleaning on same panel
    panel_times = {}

    for ridx, robot_schedule in schedules.items():
        for task in robot_schedule:
            if task['action'] != 'clean':
                continue
            start, end, panel = task['start_time'], task['end_time'], task['panel']

            # Check times within total time T
            if start < 0 or end > T:
                return False, f"Task on panel {panel} by robot {ridx} outside time bounds"

            # Check cleaning time matches
            if end - start != cleaning_times[panel]:
                return False, f"Incorrect cleaning duration on panel {panel} by robot {ridx}"

            # Check overlapping cleaning on same panel
            if panel not in panel_times:
                panel_times[panel] = []
            for s, e in panel_times[panel]:
                if not (end <= s or start >= e):  # overlap
                    return False, f"Panel {panel} cleaned simultaneously"
            panel_times[panel].append((start, end))

    # Additional validation: battery, cleaning capacity, recharge times etc. to be implemented as needed

    return True, "Solution valid"
