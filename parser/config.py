from utils.exceptions import DroneValueError, ZoneFormatError, ZoneValueError, ConfigError
from src.zones.Zone import Zone

import os

def read_metadata(line):
    if '[' not in line or ']' not in line:
        return {}
    
    try:
        meta_part = line.split('[')[1].split(']')[0]
        meta = {}
        for item in meta_part.split():
            if '=' not in item:
                raise ZoneFormatError(
                    f"Error format of metadata in '[]': {item}"
                    )
            key, value = item.split('=', 1)
            meta[key] = value
        return meta
    except IndexError:
        raise ZoneFormatError(
            f"Invalid structure in [] in string: {line}"
            )

def process_zones(line):
    if ":" not in line:
        raise ZoneFormatError(f" ':' symbol is missing {line}")

    z_type, rest = line.split(":", 1)
    main_data = rest.split('[')[0].strip()
    parts = main_data.split()
    
    if len(parts) < 3:
        raise ZoneFormatError(
            f"Not enough data for the Zone required (Name, X, Y): {line}"
            )

    name = parts[0]

    try:
        x = int(parts[1])
        y = int(parts[2])
    except ValueError:
        raise ZoneValueError(
            f"Invalid Zone coordinates. Int value required: '{name}': {parts[1]}, {parts[2]}"
            )

    metadata = read_metadata(line)
    color = metadata.get("color", "grey")
    z_kind = metadata.get("zone", "normal")
    
    try:
        raw_cap = metadata.get("max_drones", 1)
        drone_capacity = int(raw_cap)
        if drone_capacity < 0:
            raise ZoneValueError(
                f"Capacity of the Zone '{name}' can't be negative: {drone_capacity}"
                )
    except ValueError:
        raise ZoneValueError(
            f"An amount of drones should be integer value: {raw_cap}"
            )

    if "goal" in name or z_kind == "end_hub":
        drone_capacity = 100

    return Zone(name, x, y, z_kind, color, drone_capacity, 8)

def get_config(map_path):
    if not os.path.exists(map_path):
        raise ConfigError(f"Invalid file path: {map_path}")

    result = {"nb_drones": 0, "zones": []}
    zones_by_name = {}
    
    try:
        with open(map_path, "r") as f:
            lines = [l.strip() for l in f if l.strip()]

        for line in lines:
            if line.startswith("nb_drone"):
                if ":" not in line:
                    raise DroneValueError(
                        f"Invalid format for drones: {line}"
                        )
                try:
                    val = int(line.split(":")[1].strip())
                    if val <= 0:
                        raise DroneValueError(
                            f"Amount of drones should be positive: {val}"
                            )
                    result["nb_drones"] = val
                except ValueError:
                    raise DroneValueError(
                        f"Amount of drones should be integer Value."
                        )
            
            elif "hub" in line:
                zone_obj = process_zones(line)
                if zone_obj.name in zones_by_name:
                    raise ZoneValueError(
                        f"Duplicated Zone name: {zone_obj.name}"
                        )
                result["zones"].append(zone_obj)
                zones_by_name[zone_obj.name] = zone_obj

        if not result["zones"]:
            raise ConfigError("No zones found in config file")

        for line in lines:
            if line.startswith("connection"):
                if ":" not in line or "-" not in line:
                    raise ZoneFormatError(
                        f"Invalid connection format: {line}"
                        )
                
                data = line.split(":", 1)[1].strip()
                names_part = data.split("[")[0].strip()
                
                try:
                    n1, n2 = [n.strip() for n in names_part.split("-")]
                except ValueError:
                    raise ZoneFormatError(
                        f"Connection should contain 2 Zones connected with '-': {line}"
                        )

                z1, z2 = zones_by_name.get(n1), zones_by_name.get(n2)
                if not z1 or not z2:
                    missing = n1 if not z1 else n2
                    raise ZoneValueError(
                        f"Attemp to connect not existing Zone: {missing}"
                        )
                
                z1.connections.append(z2)

    except IOError as e:
        raise ConfigError(f"Error with reading file: {e}")

    return result