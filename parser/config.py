from src.zones.Zone import Zone


def read_metadata(line):
    if '[' not in line or ']' not in line:
        return {}
    
    meta_part = line.split('[')[1].split(']')[0]
    
    for item in meta_part.split():
        if '=' in item:
            key, value = item.split('=')
    return key, value


def process_zones(line):
    color = "grey"
    capacity = 1
    type = "normal"
    z_type, rest = line.split(":", 1)
    z_type = z_type.strip()
    
    main_data = rest.split('[')[0].strip()
    parts = main_data.split()
    
    name = parts[0]
    x = parts[1]
    y = parts[2]
    key, value = read_metadata(line)
    if key == "color":
        color = value
    elif key == "max_drones":
        capacity = value
    elif key == "zone":
        type = value

    return Zone(name, x, y, type, color, capacity)


def get_config(map):
    result = {
        "nb_drones": 0,
        "zones": []
    }
    with open(map, "r") as f:
        for line in f:
            if "drone" in line:
                result["nb_drones"] = int(line.split(":", 1)[1].strip())
            if "hub" in line:
                result["zones"].append(process_zones(line))
            if "connections" in line:
                connect = line.split(":", 1)[1].split("-", 1)
                for element in result["zones"]:
                    if element.name == connect[1]:
                        element.connections.append(connect[0])
                    elif element.name == connect[0]:
                        element.connections.append(connect[1])

    print(result)
