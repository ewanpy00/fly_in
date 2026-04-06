from typing import Dict, Any


class Zone:
    def __init__(self,
                 name: str,
                 x: float,
                 y: float,
                 type: Any,
                 color: str,
                 drone_capacity: int,
                 title: str) -> None:
        self.name: str = name
        self.x: float = x
        self.y: float = y
        self.type: Any = type
        self.color: str = color
        self.title: str = title
        self.drone_capacity: int = int(drone_capacity)
        self.current_drones: int = 0
        self.connections: Dict['Zone', int] = {}
        self.is_visible: bool = True

    def debug(self) -> None:
        print(self.name, self.type, self.drone_capacity)
        for c in self.connections:
            print(f"Connections: {c}")
