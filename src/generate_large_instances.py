import json
import random

N = 100000
M = 1000
T = 100000

instance = {
    "N": N,
    "M": M,
    "T": T,
    "panel_importance": [random.randint(1, 1000) for _ in range(N)],
    "robots": [
        {
            "clean_capacity": random.randint(5, 10),
            "recharge_time": random.randint(2, 5),
            "energy_capacity": random.randint(20, 30),
            "start_pos": random.randint(0, N-1)
        }
        for _ in range(M)
    ],
    "cleaning_times": [random.randint(1, 5) for _ in range(N)]
}

with open("../input/SolarSweep_Alpha_1.json", "w") as f:
    json.dump(instance, f)