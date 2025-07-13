from collections import defaultdict

# def schedule_robots(instance):
#     N = instance['N']
#     M = instance['M']
#     T = instance['T']
#     panels = list(range(N))
#     panel_importance = instance['panel_importance']
#     cleaning_times = instance['cleaning_times']
#     robots = instance['robots']

#     # Initialize schedule dict: robot_id -> list of (time, action, panel_id)
#     schedules = {r: [] for r in range(M)}

#     # Track panels cleaned to avoid multiple counting
#     panels_cleaned = set()

#     # Example simple heuristic:
#     # Assign panels to robots by importance descending, respecting cleaning capacity and energy
#     panels_sorted = sorted(panels, key=lambda x: panel_importance[x], reverse=True)

#     # Track robot states: time available, energy left
#     robot_states = []
#     for r in robots:
#         robot_states.append({
#             'available_time': 0,
#             'energy_left': r['energy_capacity'],
#             'clean_capacity': r['clean_capacity'],
#             'recharge_time': r['recharge_time']
#         })

#     # Assign panels greedily
#     for panel in panels_sorted:
#         assigned = False
#         for ridx, robot in enumerate(robot_states):
#             # Check if robot can clean this panel
#             if panel not in panels_cleaned and robot['clean_capacity'] > 0:
#                 cleaning_time = cleaning_times[panel]

#                 # Check energy and time feasibility (simplified)
#                 if robot['energy_left'] >= cleaning_time and robot['available_time'] + cleaning_time <= T:
#                     # Schedule cleaning
#                     schedules[ridx].append({
#                         'start_time': robot['available_time'],
#                         'end_time': robot['available_time'] + cleaning_time,
#                         'panel': panel,
#                         'action': 'clean'
#                     })
#                     robot['available_time'] += cleaning_time
#                     robot['energy_left'] -= cleaning_time
#                     robot['clean_capacity'] -= 1
#                     panels_cleaned.add(panel)
#                     assigned = True
#                     break

#                 else:
#                     # Recharge before cleaning
#                     robot['available_time'] += robot['recharge_time']
#                     robot['energy_left'] = robots[ridx]['energy_capacity']

#         if not assigned:
#             # Panel could not be assigned due to capacity or energy/time constraints
#             continue

#     return schedules

#     visualize_robot_activity(robots, schedules, T)


# from collections import defaultdict

# def schedule_robots(instance):
#     N = instance['N']
#     M = instance['M']
#     T = instance['T']
#     panels = list(range(N))
#     panel_importance = instance['panel_importance']
#     cleaning_times = instance['cleaning_times']
#     robots = instance['robots']

#     # Initialize schedule dict: robot_id -> list of (time, action, panel_id)
#     schedules = {r: [] for r in range(M)}

#     # Track panels cleaned to avoid multiple counting
#     panels_cleaned = set()

#     # Example simple heuristic:
#     # Assign panels to robots by importance descending, respecting cleaning capacity and energy
#     panels_sorted = sorted(panels, key=lambda x: panel_importance[x], reverse=True)

#     # Track robot states: time available, energy left
#     robot_states = []
#     for r in robots:
#         robot_states.append({
#             'available_time': 0,
#             'energy_left': r['energy_capacity'],
#             'clean_capacity': r['clean_capacity'],
#             'recharge_time': r['recharge_time']
#         })

#     # Assign panels greedily
#     for panel in panels_sorted:
#         assigned = False
#         for ridx, robot in enumerate(robot_states):
#             # Check if robot can clean this panel
#             if panel not in panels_cleaned and robot['clean_capacity'] > 0:
#                 cleaning_time = cleaning_times[panel]

#                 # Check energy and time feasibility (simplified)
#                 if robot['energy_left'] >= cleaning_time and robot['available_time'] + cleaning_time <= T:
#                     # Schedule cleaning
#                     schedules[ridx].append({
#                         'start_time': robot['available_time'],
#                         'end_time': robot['available_time'] + cleaning_time,
#                         'panel': panel,
#                         'action': 'clean'
#                     })
#                     robot['available_time'] += cleaning_time
#                     robot['energy_left'] -= cleaning_time
#                     robot['clean_capacity'] -= 1
#                     panels_cleaned.add(panel)
#                     assigned = True
#                     break

#                 else:
#                     # Recharge before cleaning
#                     robot['available_time'] += robot['recharge_time']
#                     robot['energy_left'] = robots[ridx]['energy_capacity']

#         if not assigned:
#             # Panel could not be assigned due to capacity or energy/time constraints
#             continue

#     return schedules


import sys
import os
import json
from parser import load_instance
from validator import validate_solution
from score import compute_score


def schedule_robots(instance):
    N = instance['N']
    M = instance['M']
    T = instance['T']
    panels = list(range(N))
    panel_importance = instance['panel_importance']
    cleaning_times = instance['cleaning_times']
    robots = instance['robots']
    panel_positions = instance['panel_positions']
    move_energy_cost = instance.get('move_energy_cost', 1)
    standby_energy_cost = instance.get('standby_energy_cost', 0)

    panel_coords = {i: tuple(pos) for i, pos in enumerate(panel_positions)}

    schedules = {r: [] for r in range(M)}
    panels_cleaned = set()

    robot_states = []
    for r in robots:
        robot_states.append({
            'available_time': 0,
            'energy_left': r['energy_capacity'],
            'clean_capacity': r['clean_capacity'],
            'recharge_time': r['recharge_time'],
            'current_position': panel_coords[r['start_pos']],
            'start_position': panel_coords[r['start_pos']],
            'move_energy_used': 0,
            'clean_energy_used': 0
        })

    for ridx, robot in enumerate(robot_states):
        remaining_panels = [p for p in panels if p not in panels_cleaned]

        while robot['clean_capacity'] > 0 and robot['available_time'] < T and remaining_panels:
            def panel_score(panel):
                imp = panel_importance[panel]
                dist = abs(robot['current_position'][0] - panel_coords[panel][0]) + abs(robot['current_position'][1] - panel_coords[panel][1])
                return imp / (1 + dist)

            best_panel = max(remaining_panels, key=panel_score)
            panel_pos = panel_coords[best_panel]
            cleaning_time = cleaning_times[best_panel]

            curr_x, curr_y = robot['current_position']
            target_x, target_y = panel_pos
            manhattan_distance = abs(curr_x - target_x) + abs(curr_y - target_y)
            move_energy = manhattan_distance * move_energy_cost
            move_time = manhattan_distance

            total_energy_needed = move_energy + cleaning_time
            total_time_needed = move_time + cleaning_time

            if robot['energy_left'] >= total_energy_needed and robot['available_time'] + total_time_needed <= T:
                robot['energy_left'] -= move_energy
                robot['move_energy_used'] += move_energy
                robot['available_time'] += move_time
                robot['current_position'] = panel_pos

                schedules[ridx].append({
                    'start_time': robot['available_time'],
                    'end_time': robot['available_time'] + cleaning_time,
                    'panel': best_panel,
                    'action': 'clean'
                })
                robot['available_time'] += cleaning_time
                robot['energy_left'] -= cleaning_time
                robot['clean_energy_used'] += cleaning_time
                robot['clean_capacity'] -= 1

                panels_cleaned.add(best_panel)
                remaining_panels.remove(best_panel)
            else:
                home_x, home_y = robot['start_position']
                back_distance = abs(curr_x - home_x) + abs(curr_y - home_y)
                back_energy = back_distance * move_energy_cost

                if robot['energy_left'] >= back_energy:
                    robot['energy_left'] -= back_energy
                    robot['move_energy_used'] += back_energy
                    robot['available_time'] += back_distance
                    robot['current_position'] = (home_x, home_y)
                else:
                    robot['clean_capacity'] = 0
                    break

                robot['available_time'] += robot['recharge_time']
                robot['energy_left'] = robots[ridx]['energy_capacity']

    energy_used_per_robot = []
    for ridx, robot in enumerate(robot_states):
        active_time = sum([task['end_time'] - task['start_time'] for task in schedules[ridx]])
        idle_time = robot['available_time'] - active_time
        standby_energy = idle_time * standby_energy_cost

        total_energy_used = robot['move_energy_used'] + robot['clean_energy_used'] + standby_energy
        energy_used_per_robot.append({
            'robot_id': ridx,
            'total_energy_used': total_energy_used,
            'move_energy_used': robot['move_energy_used'],
            'clean_energy_used': robot['clean_energy_used'],
        })

    return schedules, energy_used_per_robot

    N = instance['N']
    M = instance['M']
    T = instance['T']
    panels = list(range(N))
    panel_importance = instance['panel_importance']
    cleaning_times = instance['cleaning_times']
    robots = instance['robots']
    panel_positions = instance['panel_positions']
    move_energy_cost = instance.get('move_energy_cost', 1)
    standby_energy_cost = instance.get('standby_energy_cost', 0)

    panel_coords = {i: tuple(pos) for i, pos in enumerate(panel_positions)}

    schedules = {r: [] for r in range(M)}
    panels_cleaned = set()
    panels_sorted = sorted(panels, key=lambda x: panel_importance[x], reverse=True)

    robot_states = []
    for r in robots:
        robot_states.append({
            'available_time': 0,
            'energy_left': r['energy_capacity'],
            'clean_capacity': r['clean_capacity'],
            'recharge_time': r['recharge_time'],
            'current_position': panel_coords[r['start_pos']],
            'start_position': panel_coords[r['start_pos']],
            'move_energy_used': 0,
            'clean_energy_used': 0
        })

    for panel in panels_sorted:
        assigned = False
        panel_pos = panel_coords[panel]
        cleaning_time = cleaning_times[panel]

        for ridx, robot in enumerate(robot_states):
            if panel in panels_cleaned or robot['clean_capacity'] <= 0:
                continue

            curr_x, curr_y = robot['current_position']
            target_x, target_y = panel_pos
            manhattan_distance = abs(curr_x - target_x) + abs(curr_y - target_y)
            move_energy = manhattan_distance * move_energy_cost
            move_time = manhattan_distance

            total_energy_needed = move_energy + cleaning_time
            total_time_needed = move_time + cleaning_time

            if robot['energy_left'] >= total_energy_needed and robot['available_time'] + total_time_needed <= T:
                robot['energy_left'] -= move_energy
                robot['move_energy_used'] += move_energy
                robot['available_time'] += move_time
                robot['current_position'] = panel_pos

                schedules[ridx].append({
                    'start_time': robot['available_time'],
                    'end_time': robot['available_time'] + cleaning_time,
                    'panel': panel,
                    'action': 'clean'
                })
                robot['available_time'] += cleaning_time
                robot['energy_left'] -= cleaning_time
                robot['clean_energy_used'] += cleaning_time
                robot['clean_capacity'] -= 1

                panels_cleaned.add(panel)
                assigned = True
                break
            else:
                home_x, home_y = robot['start_position']
                back_distance = abs(curr_x - home_x) + abs(curr_y - home_y)
                back_energy = back_distance * move_energy_cost

                if robot['energy_left'] >= back_energy:
                    robot['energy_left'] -= back_energy
                    robot['move_energy_used'] += back_energy
                    robot['available_time'] += back_distance
                    robot['current_position'] = (home_x, home_y)
                else:
                    robot['clean_capacity'] = 0
                    continue

                robot['available_time'] += robot['recharge_time']
                robot['energy_left'] = robots[ridx]['energy_capacity']

        if not assigned:
            continue

    energy_used_per_robot = []
    for ridx, robot in enumerate(robot_states):
        active_time = sum([task['end_time'] - task['start_time'] for task in schedules[ridx]])
        idle_time = robot['available_time'] - active_time
        standby_energy = idle_time * standby_energy_cost

        total_energy_used = robot['move_energy_used'] + robot['clean_energy_used'] + standby_energy
        energy_used_per_robot.append({
            'robot_id': ridx,
            'total_energy_used': total_energy_used,
            'move_energy_used': robot['move_energy_used'],
            'clean_energy_used': robot['clean_energy_used'],
        })

    return schedules, energy_used_per_robot

    N = instance['N']
    M = instance['M']
    T = instance['T']
    panels = list(range(N))
    panel_importance = instance['panel_importance']
    cleaning_times = instance['cleaning_times']
    robots = instance['robots']
    panel_positions = instance['panel_positions']
    move_energy_cost = instance.get('move_energy_cost', 1)
    standby_energy_cost = instance.get('standby_energy_cost', 0)

    panel_coords = {i: tuple(pos) for i, pos in enumerate(panel_positions)}

    schedules = {r: [] for r in range(M)}
    panels_cleaned = set()
    panels_sorted = sorted(panels, key=lambda x: panel_importance[x], reverse=True)

    robot_states = []
    for r in robots:
        robot_states.append({
            'available_time': 0,
            'energy_left': r['energy_capacity'],
            'clean_capacity': r['clean_capacity'],
            'recharge_time': r['recharge_time'],
            'current_position': panel_coords[r['start_pos']],
            'start_position': panel_coords[r['start_pos']]
        })

    for panel in panels_sorted:
        assigned = False
        panel_pos = panel_coords[panel]
        cleaning_time = cleaning_times[panel]

        for ridx, robot in enumerate(robot_states):
            if panel in panels_cleaned or robot['clean_capacity'] <= 0:
                continue

            curr_x, curr_y = robot['current_position']
            target_x, target_y = panel_pos
            manhattan_distance = abs(curr_x - target_x) + abs(curr_y - target_y)
            move_energy = manhattan_distance * move_energy_cost
            move_time = manhattan_distance

            total_energy_needed = move_energy + cleaning_time
            total_time_needed = move_time + cleaning_time

            if robot['energy_left'] >= total_energy_needed and robot['available_time'] + total_time_needed <= T:
                robot['energy_left'] -= move_energy
                robot['available_time'] += move_time
                robot['current_position'] = panel_pos

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
                # Return to base before recharge
                home_x, home_y = robot['start_position']
                back_distance = abs(curr_x - home_x) + abs(curr_y - home_y)
                back_energy = back_distance * move_energy_cost

                if robot['energy_left'] >= back_energy:
                    robot['energy_left'] -= back_energy
                    robot['available_time'] += back_distance
                    robot['current_position'] = (home_x, home_y)
                else:
                    # Can't return to base, robot stops operating
                    robot['clean_capacity'] = 0
                    continue

                # Recharge
                robot['available_time'] += robot['recharge_time']
                robot['energy_left'] = robots[ridx]['energy_capacity']

        if not assigned:
            continue

    # Apply standby energy consumption
    energy_used_per_robot = []
    for ridx, robot in enumerate(robot_states):
        active_time = sum([task['end_time'] - task['start_time'] for task in schedules[ridx]])
        idle_time = robot['available_time'] - active_time
        standby_energy = idle_time * standby_energy_cost

        total_energy_used = (robots[ridx]['energy_capacity'] - robot['energy_left']) + standby_energy
        energy_used_per_robot.append({
            'robot_id': ridx,
            'energy_used': total_energy_used
        })

    return schedules, energy_used_per_robot

    N = instance['N']
    M = instance['M']
    T = instance['T']
    panels = list(range(N))
    panel_importance = instance['panel_importance']
    cleaning_times = instance['cleaning_times']
    robots = instance['robots']
    panel_positions = instance['panel_positions']
    move_energy_cost = instance.get('move_energy_cost', 1)  # default to 1 if missing

    # Map panel ID to its position (x, y)
    panel_coords = {i: tuple(pos) for i, pos in enumerate(panel_positions)}

    # Initialize schedules per robot
    schedules = {r: [] for r in range(M)}
    panels_cleaned = set()

    # Sort panels by descending importance
    panels_sorted = sorted(panels, key=lambda x: panel_importance[x], reverse=True)

    # Initialize robot states
    robot_states = []
    for r in robots:
        robot_states.append({
            'available_time': 0,
            'energy_left': r['energy_capacity'],
            'clean_capacity': r['clean_capacity'],
            'recharge_time': r['recharge_time'],
            'current_position': panel_coords[r['start_pos']]
        })

    # Assign panels greedily
    for panel in panels_sorted:
        assigned = False
        panel_pos = panel_coords[panel]
        cleaning_time = cleaning_times[panel]

        for ridx, robot in enumerate(robot_states):
            if panel in panels_cleaned or robot['clean_capacity'] <= 0:
                continue

            curr_x, curr_y = robot['current_position']
            target_x, target_y = panel_pos
            manhattan_distance = abs(curr_x - target_x) + abs(curr_y - target_y)
            move_energy = manhattan_distance * move_energy_cost
            move_time = manhattan_distance  # assume 1 time unit per panel moved

            total_energy_needed = move_energy + cleaning_time
            total_time_needed = move_time + cleaning_time

            if robot['energy_left'] >= total_energy_needed and robot['available_time'] + total_time_needed <= T:
                # Deduct movement energy and update position
                robot['energy_left'] -= move_energy
                robot['available_time'] += move_time
                robot['current_position'] = panel_pos

                # Schedule cleaning only
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
                # Recharge: increase available time, restore energy, keep position unchanged
                robot['available_time'] += robot['recharge_time']
                robot['energy_left'] = robots[ridx]['energy_capacity']

        if not assigned:
            # Could not assign panel due to constraints
            continue

    # Calculate total energy used per robot
    energy_used_per_robot = []
    for ridx, robot in enumerate(robot_states):
        energy_used = robots[ridx]['energy_capacity'] - robot['energy_left']
        energy_used_per_robot.append({
            'robot_id': ridx,
            'energy_used': energy_used
        })

    return schedules, energy_used_per_robot