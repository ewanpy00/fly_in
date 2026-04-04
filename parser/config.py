import utils. exceptions as e
from src.Zone import Zone
import os


def read_metadata(line):
    if '[' not in line or ']' not in line:
        return {}

    try:
        meta_part = line.split('[')[1].split(']')[0]
        meta = {}
        for item in meta_part.split():
            if '=' not in item:
                raise e.ZoneFormatError(
                    f"Error format of metadata in '[]': {item}"
                    )
            key, value = item.split('=', 1)
            meta[key] = value
        return meta
    except IndexError:
        raise e.ZoneFormatError(
            f"Invalid structure in [] in string: {line}"
            )


def process_zones(line):
    if ":" not in line:
        raise e.ZoneFormatError(f" ':' symbol is missing {line}")

    rest = line.split(":", 1)[1]
    main_data = rest.split('[')[0].strip()
    p = main_data.split()

    if len(p) < 3:
        raise e.ZoneFormatError(
            f"Not enough data for the Zone required (Name, X, Y): {line}"
            )

    name = p[0]
    try:
        x = int(p[1])
        y = int(p[2])
    except ValueError:
        raise e.ZoneValueError(
            f"Zone coords should be in value: '{name}': {p[1]}, {p[2]}"
            )

    metadata = read_metadata(line)
    color = metadata.get("color", "grey")
    z_kind = metadata.get("zone", "normal")

    try:
        raw_cap = metadata.get("drone_capacity", 1)
        drone_capacity = int(raw_cap)
        if drone_capacity < 0:
            raise e.ZoneValueError(
                f"Capacity of the Zone '{name}' can't be < 0: {drone_capacity}"
                )
    except ValueError:
        raise e.ZoneValueError(
            f"An amount of drones should be integer value: {raw_cap}"
            )

    if "goal" in name or z_kind == "end_hub":
        drone_capacity = 100

    return Zone(name, x, y, z_kind, color, drone_capacity)


def get_config(map_path):
    if not os.path.exists(map_path):
        raise e.ConfigError(f"Invalid file path: {map_path}")

    result = {"nb_drones": 0, "zones": []}
    zones_by_name = {}

    try:
        with open(map_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        for line in lines:
            if line.startswith("nb_drone"):
                if ":" not in line:
                    raise e.DroneValueError(
                        f"Invalid format for drones: {line}"
                        )
                try:
                    val = int(line.split(":")[1].strip())
                    if val <= 0 or val > 100:
                        raise e.DroneValueError(
                            f"nb_drones val should be in range 0 to 100: {val}"
                            )
                    result["nb_drones"] = val
                except ValueError:
                    raise e.DroneValueError(
                        "Amount of drones should be integer Value."
                        )

            elif "hub" in line:
                zone_obj = process_zones(line)
                if zone_obj.name in zones_by_name:
                    raise e.ZoneValueError(
                        f"Duplicated Zone name: {zone_obj.name}"
                        )
                result["zones"].append(zone_obj)
                zones_by_name[zone_obj.name] = zone_obj

        if not result["zones"]:
            raise e.ConfigError("No zones found in config file")

        for line in lines:
            if line.startswith("connection"):
                if ":" not in line or "-" not in line:
                    raise e.ZoneFormatError(
                        f"Invalid connection format: {line}"
                        )

                data = line.split(":", 1)[1].strip()
                n_p = data.split("[")[0].strip()

                try:
                    n1, n2 = [n.strip() for n in n_p.split("-")]
                except ValueError:
                    raise e.ZoneFormatError(
                        f"Invalid connection val, check your conf file: {line}"
                        )

                z1 = zones_by_name.get(n1)
                z2 = zones_by_name.get(n2)

                if not z1 or not z2:
                    missing = n1 if not z1 else n2
                    raise e.ZoneValueError(
                        f"Attempt to connect non-existing Zone: {missing}"
                        )

                try:
                    meta_data = read_metadata(line)
                    link_cap = int(meta_data.get("max_link_capacity", 8))
                except ValueError:
                    raise ConnectionError("Invalud max_link_capacity value")

                if link_cap <= 0 or link_cap >= 10:
                    raise ConnectionError(
                        f"max_link_capacity should be 0 to 10: {link_cap}"
                        )
                z1.connections[z2] = link_cap

    except IOError as exc:
        raise e.ConfigError(f"Error with reading file: {exc}")

    return result
