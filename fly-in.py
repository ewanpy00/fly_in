from utils.exceptions import ConfigError
from src.Drone import Drone
from src.Map import Map
from parser import config
from src.display import display

def fly_in():
        print()
        map = Map()
        mode = False #read from the terminal
        try:
            print("[LOG] Processing all the configurations")
            configuratoin = config.get_config("maps/custom_map.txt")
            zones_conf = configuratoin["zones"]
            drones_amount = configuratoin["nb_drones"]
            map.add_zones(zones_conf)
            for i in range(drones_amount):
                map.add_drone(Drone(zones_conf[0], mode, i+1))
            display.visualize(map, mode)
        except ConfigError as e: #Catch Programm error that will be parent class for ConfigError and Processing error (OR I DONT EVEN NEED PROCESSING ERROR)
             print("[LOG] Configuration process failed")
             print(e)
        print("[LOG] Configuration completed successfully")
        print("[LOG] Running the program")

if __name__ == "__main__":
    fly_in()
