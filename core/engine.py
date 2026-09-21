import json
import os

def build_scenario_list(modules, difficulty):
    scenarios = []
    # Loop through each module the user selected
    for mod in modules:
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', f'{mod}.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Only add scenarios that match the selected difficulty
                for item in data:
                    if item.get("difficulty") == difficulty:
                        scenarios.append(item)
    return scenarios

def get_scenario_by_index(modules, difficulty, index):
    scenarios = build_scenario_list(modules, difficulty)
    if 0 <= index < len(scenarios):
        return scenarios[index]
    return None

def validate_command(user_input, modules, difficulty, index):
    scenario = get_scenario_by_index(modules, difficulty, index)
    if not scenario:
        return {"correct": False, "message": "Scenario not found."}

    val = scenario.get("validation", {})
    user_parts = user_input.split()

    for forbidden in val.get("forbidden", []):
        if forbidden in user_parts:
            hint = val.get("hints", {}).get(forbidden, f"Remove the '{forbidden}' command.")
            return {"correct": False, "message": hint}

    if "192.168.1.0/24" not in user_parts and "192.168.1.0" in user_parts:
        return {"correct": False, "message": val.get("hints", {}).get("192.168.1.0", "Check your IP/CIDR.")}

    if "-sT" in user_parts:
        return {"correct": False, "message": val.get("hints", {}).get("-sT", "Wrong scan type.")}

    missing = [req for req in val.get("required", []) if req not in user_parts]
    if missing:
        return {"correct": False, "message": "[-] Error: Missing required flags, incorrect IP, or invalid syntax."}

    return {"correct": True, "message": "[+] Command successful. Executing scan..."}