from src.Drone import Drone
from src.Map import Map
from parser import config
from src.display import display
# import src


def fly_in():
    configuratoin = config.get_config("maps/challenger/01_the_impossible_dream.txt")
    zones_conf = configuratoin["zones"]
    drones_amount = configuratoin["nb_drones"]
    mode = True
    map = Map()
    map.add_zones(zones_conf)
    for i in range(drones_amount):
        map.add_drone(Drone(zones_conf[0], mode, i+1))
    print(map.drones)
    display.visualize(map, mode)

    # execute the algorithm by steps or execute algorithm as a video demonstration

fly_in()
