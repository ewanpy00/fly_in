from enum import Enum


class ZoneType(Enum):
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class Zone():
    def __init__(self, name, x, y, type, color, capacity):
        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.capacity = capacity
        self.current_drones = []
        self.connections = []
        print(self.name, self.x, self.y, self.type, self.color, self.capacity)
