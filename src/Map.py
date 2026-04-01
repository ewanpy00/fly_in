from src.Drone import Drone

class Map:
    def __init__(self):
        self.zones = []
        self.drones = []

    def add_zones(self, zones):
        for zone in zones:
            self.zones.append(zone)

    def add_drone(self, drone):
        self.drones.append(drone)