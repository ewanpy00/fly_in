from typing import List, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from Zone import Zone
    from Drone import Drone


class Map:
    def __init__(self) -> None:
        self.zones: List[Zone] = []
        self.drones: List[Drone] = []

    def add_zones(self, zones: List[Any]) -> None:
        for zone in zones:
            self.zones.append(zone)

    def add_drone(self, drone: Any) -> None:
        self.drones.append(drone)
