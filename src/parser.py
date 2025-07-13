import json

def load_instance(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    required_keys = ['N', 'M', 'T', 'panel_importance', 'robots', 'cleaning_times']
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing key {key} in input file.")
    
    if len(data['panel_importance']) != data['N']:
        raise ValueError("panel_importance length does not match N.")
    if len(data['cleaning_times']) != data['N']:
        raise ValueError("cleaning_times length does not match N.")
    if len(data['robots']) != data['M']:
        raise ValueError("robots length does not match M.")
    
    for idx, robot in enumerate(data['robots']):
        for rkey in ['clean_capacity', 'recharge_time', 'energy_capacity', 'start_pos']:
            if rkey not in robot:
                raise ValueError(f"Robot {idx} missing key {rkey}.")
    
    return data
