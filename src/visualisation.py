import matplotlib.pyplot as plt
import numpy as np

def visualize_robot_activity(robots, schedules, T, save=False, filename="robot_activity.png"):
    """
    Visualizes the robot activity (battery level, cleaning schedule) over time.

    Args:
        robots (list): List of robot states, containing energy, recharge times, etc.
        schedules (dict): Robot schedules, indicating the start and end time of each cleaning task.
        T (int): Maximum time available for scheduling.
        save (bool): If True, saves the visualization to a file.
        filename (str): The filename to save the image (if save=True).
    """
    num_robots = len(robots)
    times = np.arange(0, T + 1)

    # Initialize battery levels over time
    battery_levels = np.zeros((num_robots, len(times)))

    # Create an empty schedule plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, T)
    ax.set_ylim(0, num_robots)
    ax.set_xlabel("Time")
    ax.set_ylabel("Robot ID")
    ax.set_title("Robot Cleaning and Recharge Schedule")

    # Draw the robot activity (cleaning or recharging) for each robot
    for ridx, robot_schedule in schedules.items():
        # Track battery levels over time
        robot = robots[ridx]
        current_battery = robot['energy_left']

        for task in robot_schedule:
            start_time = task['start_time']
            end_time = task['end_time']
            panel = task['panel']

            # Update battery level based on cleaning
            cleaning_time = end_time - start_time
            energy_consumed = cleaning_time * robot['energy_rate']
            current_battery -= energy_consumed

            # Draw the cleaning activity as a colored bar
            ax.barh(ridx, end_time - start_time, left=start_time, color='blue', edgecolor='black')

            # Update battery level and draw recharge if necessary
            if current_battery < 0:
                current_battery = 0  # Ensure no negative battery levels
            battery_levels[ridx, start_time:end_time] = current_battery

        # Recharge if needed (for simplicity, add recharge after cleaning)
        recharge_start = end_time
        recharge_time = robot['recharge_time']
        recharge_end = recharge_start + recharge_time
        ax.barh(ridx, recharge_time, left=recharge_start, color='red', edgecolor='black')

    # Plot battery levels as a line chart
    for ridx in range(num_robots):
        ax.plot(times, battery_levels[ridx], label=f"Robot {ridx} Battery", linestyle='-', color='green')

    plt.legend(loc='best')
    plt.tight_layout()

    # Save the image if requested
    if save:
        plt.savefig(filename)
        print(f"Visualization saved as {filename}")
    else:
        plt.show()

    plt.close()

