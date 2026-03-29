from parser import config
from src.display import display
# import src


def fly_in():
    configuratoin = config.get_config("maps/easy/01_linear_path.txt")
    zones_conf = configuratoin["zones"]
    display.visualize(zones_conf)

fly_in()
