from enum import Enum


class ZoneType(Enum):
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class Zone():
    def __init__(self, name, x, y, type, color, drone_capacity, link_capacity):
        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.drone_capacity = drone_capacity
        self.link_capacity = link_capacity
        self.current_drones = []
        self.connections = []
        print(self.name, self.x, self.y, self.type, self.color, self.drone_capacity)
