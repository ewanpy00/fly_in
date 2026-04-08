from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Map import Map


class MovementSystem:
    def step(self, map_obj: Map, turn_counter: int) -> int:
        all_idle = all(not drone.is_moving for drone in map_obj.drones)

        if all_idle:
            if any(len(d.get_exit_path() or []) > 1 for d in map_obj.drones):
                turn_counter += 1
                print(f"\nTurn: {turn_counter}:     ", end="")

                for drone in map_obj.drones:
                    exit_path = drone.get_exit_path()
                    if exit_path and len(exit_path) > 1:
                        next_step = exit_path[1]

                        if next_step.current_drones < next_step.drone_capacity:
                            next_step.current_drones += 1
                            drone.current_zone.current_drones -= 1
                            drone.start_move(next_step)
        return turn_counter


def process_drones_step(map_obj: Map, turn_counter: int) -> int:
    return MovementSystem().step(map_obj, turn_counter)
