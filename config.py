import math
import os
from typing import Dict, Any, List, Set
from ZoneType import ZoneType
import exceptions as e
from Zone import Zone


class ConfigLoader:
    def _assert_valid_zone_name(self, name: str, line: str) -> None:
        if not name:
            raise e.ZoneFormatError(f"Zone name cannot be empty: {line}")
        if "-" in name or " " in name or "\t" in name:
            raise e.ZoneFormatError(
                f"Zone name '{name}' must not contain dashes or spaces "
                f"(breaks connection syntax): {line}"
            )

    def read_metadata(self, line: str) -> Dict[str, Any]:
        if '[' not in line or ']' not in line:
            return {}

        try:
            meta_part = line.split('[')[1].split(']')[0]
            meta: Dict[str, Any] = {}
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

    def process_zone_line(self, line: str) -> Zone:
        if ":" not in line:
            raise e.ZoneFormatError(
                f"':' symbol is missing in zone definition: {line}"
                )

        title, rest = line.split(":", 1)

        if title not in ["start_hub", "end_hub", "hub"]:
            raise e.ZoneFormatError(
                f"Invalid zone prefix '{title}'. start_hub, end_hub or hub."
                )

        if ":" in rest:
            raise e.ZoneFormatError(
                f"Zone data cannot contain additional ':' symbols: {line}"
                )

        main_data = rest.split('[')[0].strip()
        p = main_data.split()

        if len(p) < 3:
            raise e.ZoneFormatError(
                f"Not enough data for the Zone (Name, X, Y required): {line}"
                )

        name = p[0]
        self._assert_valid_zone_name(name, line)

        try:
            x = float(p[1])
            y = float(p[2])
        except ValueError:
            raise e.ZoneValueError(
                f"Zone cords should be numeric value: '{name}': {p[1]}, {p[2]}"
                )

        if not x.is_integer() or not y.is_integer():
            raise e.ZoneValueError(
                f"Zone coords must be integers: '{name}' got ({p[1]}, {p[2]})"
            )

        metadata = self.read_metadata(line)
        color = metadata.get("color", "white")
        z_type = metadata.get("zone", "normal")

        try:
            raw_cap = metadata.get("max_drones", 1)
            drone_capacity = int(raw_cap)
            if drone_capacity <= 0:
                raise e.ZoneValueError(
                    f"Drone capacity of the Zone '{name}' "
                    f"must > 0. Got: {drone_capacity}"
                    )
        except ValueError:
            raise e.ZoneValueError(
                f"max_drones should be int val: {metadata.get('max_drones')}"
                )

        if title == "end_hub":
            drone_capacity = 100

        try:
            zone_type = ZoneType(z_type)
        except ValueError:
            raise e.ZoneFormatError(
                f"Invalid zone type '{z_type}' for zone '{name}'."
                )

        return Zone(name, x, y, zone_type, color, drone_capacity, title)

    def _check_graph_connectivity(self, zones: List[Zone]) -> None:
        start_hubs = [z for z in zones if z.title == "start_hub"]
        end_hubs = [z for z in zones if z.title == "end_hub"]

        if len(start_hubs) != 1:
            raise e.ConfigError(
                "Map must contain exactly one 'start_hub' "
                f"(found {len(start_hubs)})."
            )
        if len(end_hubs) != 1:
            raise e.ConfigError(
                "Map must contain exactly one 'end_hub' "
                f"(found {len(end_hubs)})"
            )

        visited: Set[Zone] = set()
        queue: List[Zone] = start_hubs.copy()

        for s in start_hubs:
            visited.add(s)

        while queue:
            curr = queue.pop(0)
            for neighbor in curr.connections.keys():
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        if not any(eh in visited for eh in end_hubs):
            raise e.ConfigError(
                "Disconnected graph: No path from any start_hub to any end_hub"
                )

    def validate_coordinates(
            self,
            zones: List[Zone],
            threshold: int = 30) -> None:
        if len(zones) < 2:
            return

        xs = [z.x for z in zones]
        ys = [z.y for z in zones]

        range_x = max(xs) - min(xs)
        range_y = max(ys) - min(ys)

        if range_x > 0 and range_y > 0:
            ratio = max(range_x, range_y) / min(range_x, range_y)
            if ratio >= threshold:
                raise e.ZoneValueError(
                    f"Map is too distorted ({ratio:.1f}:1). "
                    "Check junction/hub coordinates."
                )
        for i, z1 in enumerate(zones):
            for z2 in zones[i+1:]:
                if z1.title == "common_buffer" or z2.title == "common_buffer":
                    continue
                dist = math.sqrt((z1.x - z2.x)**2 + (z1.y - z2.y)**2)
                if dist < 0.1:
                    raise e.ZoneValueError(
                        f"Zones '{z1.name}' and '{z2.name}' are too close "
                        f"(distance {dist:.4f}). This will break visualization"
                    )

    def load(self, map_path: str) -> Dict[str, Any]:
        if not os.path.exists(map_path):
            raise e.ConfigError(f"Invalid file path: {map_path}")

        result: Dict[str, Any] = {"nb_drones": None, "zones": []}
        zones_by_name: Dict[str, Zone] = {}
        seen_connections: Set[tuple] = set()
        seen_coordinates: Set[tuple] = set()

        try:
            with open(map_path, "r") as f:
                lines = []
                for line in f:
                    clean_line = line.split('#')[0].strip()
                    if clean_line:
                        lines.append(clean_line)

            for line in lines:
                if line.startswith("nb_drones:"):
                    try:
                        val = int(line.split(":")[1].strip())
                        if val <= 0 or val > 100:
                            raise e.DroneValueError(
                                f"nb_drones must be from 1 to 100: {val}"
                                )
                        result["nb_drones"] = val
                    except (ValueError, IndexError):
                        raise e.DroneValueError(
                            "Amount of drones should be an integer value."
                            )

                elif line.startswith(("start_hub:", "end_hub:", "hub:")):
                    zone_obj = self.process_zone_line(line)

                    if zone_obj.name in zones_by_name:
                        raise e.ZoneValueError(
                            f"Duplicated Zone name: {zone_obj.name}"
                            )

                    coords = (zone_obj.x, zone_obj.y)
                    if coords in seen_coordinates:
                        raise e.ZoneValueError(
                            f"Zone '{zone_obj.name}' uses coords {coords} "
                            f"which are already occupied by another zone."
                        )

                    result["zones"].append(zone_obj)
                    zones_by_name[zone_obj.name] = zone_obj
                    seen_coordinates.add(coords)

            if result["nb_drones"] is None:
                raise e.ConfigError(
                    "Malformed file: missing 'nb_drones' definition"
                    )

            if not result["zones"]:
                raise e.ConfigError(
                    "No zones found in config file. Map is empty"
                    )

            for line in lines:
                if line.startswith("connection:"):
                    if "-" not in line:
                        raise e.ZoneFormatError(
                            f"Invalid connection format: {line}"
                            )

                    data = line.split(":", 1)[1].strip()
                    n_p = data.split("[")[0].strip()

                    try:
                        n1, n2 = [n.strip() for n in n_p.split("-")]
                    except ValueError:
                        raise e.ZoneFormatError(
                            f"Connection must be between two nodes: {line}"
                            )

                    conn_id = tuple(sorted([n1, n2]))
                    if conn_id in seen_connections:
                        raise e.ZoneFormatError(
                            f"Duplicate connection found between {n1} and {n2}"
                            )
                    seen_connections.add(conn_id)

                    z1 = zones_by_name.get(n1)
                    z2 = zones_by_name.get(n2)

                    if not z1 or not z2:
                        missing = n1 if not z1 else n2
                        raise e.ZoneValueError(
                            f"Attempt to connect non-existing Zone: {missing}"
                            )

                    try:
                        meta_data = self.read_metadata(line)
                        link_cap = int(meta_data.get("max_link_capacity", 1))
                    except ValueError:
                        raise e.ConfigError(
                            f"Invalid max_link_capacity value in line: {line}"
                            )

                    if link_cap <= 0:
                        raise e.ConfigError(
                            "max_link_capacity must "
                            f"be a positive integer: {link_cap}"
                            )

                    target_restricted = None
                    if z2.type == ZoneType.RESTRICTED:
                        target_restricted = z2
                    elif z1.type == ZoneType.RESTRICTED:
                        target_restricted = z1

                    if target_restricted:
                        target_restricted.type = ZoneType.NORMAL

                        mid_x, mid_y = (z1.x + z2.x) / 2, (z1.y + z2.y) / 2
                        mid_name = f"buffer_{z1.name}_{z2.name}"

                        buffer_zone = Zone(
                            name=mid_name, x=mid_x, y=mid_y,
                            type=ZoneType.NORMAL, color="yellow",
                            drone_capacity=link_cap, title="common_buffer"
                        )
                        buffer_zone.is_visible = False

                        result["zones"].append(buffer_zone)
                        zones_by_name[mid_name] = buffer_zone

                        z1.connections[buffer_zone] = link_cap
                        buffer_zone.connections[z2] = link_cap
                    else:
                        z1.connections[z2] = link_cap

            self._check_graph_connectivity(result["zones"])
            self.validate_coordinates(result["zones"])

        except IOError as exc:
            raise e.ConfigError(f"Error while reading file: {exc}")

        return result

    @classmethod
    def load_map(cls, map_path: str) -> Dict[str, Any]:
        return cls().load(map_path)
