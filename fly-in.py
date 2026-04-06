from exceptions import ConfigError
from Drone import Drone
from Map import Map
import config
import display
import argparse
from SpeedLevel import SpeedLevel


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fly-in drone simulation")
    parser.add_argument("-d",
                        "--debug",
                        action="store_true",
                        help="Launch the program in a debug mdoe")
    parser.add_argument("-s",
                        "--speed",
                        type=int,
                        default=3,
                        choices=[1, 2, 3, 4, 5],
                        help="Drones speed (from 1 to 5). By default: 3")
    parser.add_argument("map_path",
                        type=str,
                        help="Path to the map file")

    return parser.parse_args()


def fly_in() -> None:
    try:
        print()
        args = parse_args()
        path = args.map_path
        mode = args.debug
        drone_speed_arg = SpeedLevel(args.speed)
        drone_speed = drone_speed_arg.factor
        map = Map()

        try:
            print("[LOG] Processing all the configurations")
            configuratoin = config.get_config(path)
            zones_conf = configuratoin["zones"]
            drones_amount = configuratoin["nb_drones"]
            map.add_zones(zones_conf)
            for i in range(drones_amount):
                map.add_drone(Drone(zones_conf[0], mode, i+1, drone_speed))
            print("[LOG] Map Successfully created")
            display.visualize(map, mode)
            print("\nProgram finished without any errors")
        except ConfigError as e:
            print("[LOG] Configuration process failed")
            print(e)
    except Exception as e:
        print("An unknown error occurred. ", end="")
        print("Please check your configuration against the README.\n", e)


if __name__ == "__main__":
    fly_in()
