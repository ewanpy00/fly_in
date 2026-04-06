class Zone():
    def __init__(self, name, x, y, type, color, drone_capacity, title):
        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.title = title
        self.drone_capacity = int(drone_capacity)
        self.current_drones = 0
        self.connections = {}
        self.is_visible = True

    def debug(self):
        print(self.name, self.type, self.drone_capacity)
        for c in self.connections:
            print(f"Connections: {c}")
