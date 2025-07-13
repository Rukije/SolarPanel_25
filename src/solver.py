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
    panel_importance = instance['panel_importance']
    cleaning_times = instance['cleaning_times']
    robots = instance['robots']

    # Shembull: panel_coords = [(x, y) për çdo panel]
    panel_coords = [(0, i) for i in range(N)]  # ose merr nga instance nëse ka

    schedules = {r: [] for r in range(M)}
    panels_cleaned = set()
    energy_used_per_robot = []

    move_energy_cost = 1  # ose merr nga instance nëse ka
    clean_energy_cost = 1  # ose merr nga instance nëse ka

    for ridx, robot in enumerate(robots):
        energy_left = robot['energy_capacity']
        clean_capacity = robot['clean_capacity']
        recharge_time = robot['recharge_time']
        current_pos = panel_coords[robot['start_pos']]
        positions = [current_pos]  # fillon me pozicionin fillestar
        move_energy = 0
        clean_energy = 0
        time = 0

        for panel_id in sorted(range(N), key=lambda x: -panel_importance[x]):
            if panel_id in panels_cleaned or clean_capacity <= 0 or time >= T:
                continue
            target_pos = panel_coords[panel_id]
            dist = abs(current_pos[0] - target_pos[0]) + abs(current_pos[1] - target_pos[1])
            move_e = move_energy_cost * dist
            clean_e = clean_energy_cost

            if energy_left < move_e + clean_e:
                # Recharge
                time += recharge_time
                energy_left = robot['energy_capacity']
                continue

            # Move
            move_energy += move_e
            energy_left -= move_e
            time += dist
            current_pos = target_pos
            positions.append(current_pos)

            # Clean
            clean_energy += clean_e
            energy_left -= clean_e
            time += cleaning_times[panel_id]
            clean_capacity -= 1
            panels_cleaned.add(panel_id)

            schedules[ridx].append({
                "action": "clean",
                "panel": panel_id,
                "start_time": time - cleaning_times[panel_id],
                "end_time": time,
                "position": current_pos
            })

        energy_used_per_robot.append({
            "robot_id": ridx,
            "total_energy_used": move_energy + clean_energy,
            "move_energy_used": move_energy,
            "clean_energy_used": clean_energy,
            "positions": positions,
            "start_position": panel_coords[robot['start_pos']],
            "solar_energy_needed": robot['energy_capacity']
        })

    return {
        "schedules": schedules,
        "energy_used_per_robot": energy_used_per_robot
    }



