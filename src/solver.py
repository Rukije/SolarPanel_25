from collections import defaultdict

def schedule_robots(instance):
    N = instance['N']
    M = instance['M']
    T = instance['T']
    panels = list(range(N))
    panel_importance = instance['panel_importance']
    cleaning_times = instance['cleaning_times']
    robots = instance['robots']

    # Initialize schedule dict: robot_id -> list of (time, action, panel_id)
    schedules = {r: [] for r in range(M)}

    # Track panels cleaned to avoid multiple counting
    panels_cleaned = set()

    # Example simple heuristic:
    # Assign panels to robots by importance descending, respecting cleaning capacity and energy
    panels_sorted = sorted(panels, key=lambda x: panel_importance[x], reverse=True)

    # Track robot states: time available, energy left
    robot_states = []
    for r in robots:
        robot_states.append({
            'available_time': 0,
            'energy_left': r['energy_capacity'],
            'clean_capacity': r['clean_capacity'],
            'recharge_time': r['recharge_time']
        })

    # Assign panels greedily
    for panel in panels_sorted:
        assigned = False
        for ridx, robot in enumerate(robot_states):
            # Check if robot can clean this panel
            if panel not in panels_cleaned and robot['clean_capacity'] > 0:
                cleaning_time = cleaning_times[panel]

                # Check energy and time feasibility (simplified)
                if robot['energy_left'] >= cleaning_time and robot['available_time'] + cleaning_time <= T:
                    # Schedule cleaning
                    schedules[ridx].append({
                        'start_time': robot['available_time'],
                        'end_time': robot['available_time'] + cleaning_time,
                        'panel': panel,
                        'action': 'clean'
                    })
                    robot['available_time'] += cleaning_time
                    robot['energy_left'] -= cleaning_time
                    robot['clean_capacity'] -= 1
                    panels_cleaned.add(panel)
                    assigned = True
                    break

                else:
                    # Recharge before cleaning
                    robot['available_time'] += robot['recharge_time']
                    robot['energy_left'] = robots[ridx]['energy_capacity']

        if not assigned:
            # Panel could not be assigned due to capacity or energy/time constraints
            continue

    return schedules
