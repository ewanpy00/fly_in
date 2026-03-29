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
    drone_capacity = 1
    link_capacity = 8
    type = "normal"
    z_type, rest = line.split(":", 1)
    z_type = z_type.strip()
    
    main_data = rest.split('[')[0].strip()
    parts = main_data.split()
    
    name = parts[0]
    x = int(parts[1])
    y = int(parts[2])
    key, value = read_metadata(line)
    if key == "color":
        color = value
    elif key == "max_drones":
        drone_capacity = value
    elif key == "zone":
        type = value

    return Zone(name, x, y, type, color, drone_capacity, link_capacity)


def get_config(map):
    result = {
        "nb_drones": 0,
        "zones": []
    }
    with open(map, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("nb_drone"):
                result["nb_drones"] = int(line.split(":", 1)[1].strip())
            
            elif "hub" in line:
                result["zones"].append(process_zones(line))
            elif line.startswith("connection"):
                parts = line.split(":", 1)
                if len(parts) < 2: continue
                
                data = parts[1].strip()
                

                names_part = data.split("[")[0].strip()
                node_names = names_part.split("-")
                if len(node_names) < 2: continue
                n1, n2 = node_names[0].strip(), node_names[1].strip()
                link_meta = ""
                if "[" in data and "]" in data:
                    link_meta = data.split("[")[1].split("]")[0]

                for element in result["zones"]:
                    if element.name == n1:
                        element.connections.append(n2)
                    elif element.name == n2:
                        element.connections.append(n1)
    return result
