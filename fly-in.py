from src.Map import Map
from parser import config
from src.display import display
# import src


def fly_in():
    configuratoin = config.get_config("maps/challenger/01_the_impossible_dream.txt")
    zones_conf = configuratoin["zones"]
    map = Map()
    map.add_zones(zones_conf)
    display.visualize(map, mode=False)

    # execute the algorithm by steps or execute algorithm as a video demonstration

fly_in()
