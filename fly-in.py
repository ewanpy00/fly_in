from exceptions import ConfigError
from Drone import Drone
from Map import Map
import argparse
from SpeedLevel import SpeedLevel
from config import ConfigLoader
from display import SimulationView
from typing import Optional


class CLI:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="Fly-in drone simulation"
        )
        self.parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            help="Launch the program in a debug mdoe",
        )
        self.parser.add_argument(
            "-s",
            "--speed",
            type=int,
            default=3,
            choices=[1, 2, 3, 4, 5],
            help="Drones speed (from 1 to 5). By default: 3",
        )
        self.parser.add_argument(
            "map_path",
            type=str,
            help="Path to the map file",
        )

    def parse(self) -> argparse.Namespace:
        return self.parser.parse_args()


class Simulation:
    def __init__(self, config_loader: Optional[ConfigLoader] = None) -> None:
        self.config_loader = config_loader or ConfigLoader()

    def build_map(self, map_path: str, mode: bool, speed: float) -> Map:
        configuration = self.config_loader.load(map_path)
        zones_conf = configuration["zones"]
        drones_amount = configuration["nb_drones"]

        map_obj = Map()
        map_obj.add_zones(zones_conf)
        for i in range(drones_amount):
            map_obj.add_drone(Drone(zones_conf[0], mode, i + 1, speed))
        return map_obj

    def run(self, map_path: str, mode: bool, speed_level: int) -> None:
        drone_speed = SpeedLevel(speed_level).factor
        print("[LOG] Processing all the configurations")
        map_obj = self.build_map(map_path, mode, drone_speed)
        print("[LOG] Map Successfully created")
        SimulationView(map_obj, mode).run()


def fly_in() -> None:
    try:
        print()
        args = CLI().parse()
        app = Simulation()
        try:
            app.run(args.map_path, args.debug, args.speed)
            print("\nProgram finished without any errors")
        except ConfigError as e:
            print("[LOG] Configuration process failed")
            print(e)
    except Exception as e:
        print("An unknown error occurred. ", end="")
        print("Please check your configuration against the README.\n", e)


if __name__ == "__main__":
    fly_in()
