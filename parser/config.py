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

    if "goal" in name:
        drone_capacity = 100
    return Zone(name, x, y, type, color, drone_capacity, link_capacity)


def get_config(map_path):
    result = {"nb_drones": 0, "zones": []}
    # Создаем словарь для быстрого поиска: "имя": объект_зоны
    zones_by_name = {}

    with open(map_path, "r") as f:
        lines = f.readlines()

    # ПЕРВЫЙ ПРОХОД: Создаем все объекты зон
    for line in lines:
        line = line.strip()
        if "hub" in line:
            zone_obj = process_zones(line)
            result["zones"].append(zone_obj)
            zones_by_name[zone_obj.name] = zone_obj # Запоминаем объект
        elif line.startswith("nb_drone"):
            result["nb_drones"] = int(line.split(":")[1].strip())

    # ВТОРОЙ ПРОХОД: Устанавливаем связи объектами
    # ВТОРОЙ ПРОХОД: Устанавливаем связи объектами (только в одну сторону)
    for line in lines:
        line = line.strip()
        if line.startswith("connection"):
            data = line.split(":", 1)[1].strip()
            names_part = data.split("[")[0].strip()
            n1, n2 = [n.strip() for n in names_part.split("-")]

            zone1 = zones_by_name.get(n1)
            zone2 = zones_by_name.get(n2)

            if zone1 and zone2:
                # Добавляем ТОЛЬКО связь от первой ко второй
                # Теперь из n1 можно попасть в n2, но не наоборот
                zone1.connections.append(zone2)
    return result