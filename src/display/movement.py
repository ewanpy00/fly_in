def process_drones_step(map, turn_counter):
    all_idle = all(not drone.is_moving for drone in map.drones)

    if all_idle:
        if any(len(drone.get_exit_path() or []) > 1 for drone in map.drones):
            turn_counter += 1
            print(f"[LOG] Turn: {turn_counter}")

            for drone in map.drones:
                exit_path = drone.get_exit_path()
                if exit_path and len(exit_path) > 1:
                    next_step = exit_path[1]

                    if next_step.current_drones < next_step.drone_capacity:
                        next_step.current_drones += 1
                        drone.current_zone.current_drones -= 1
                        drone.start_move(next_step)
    return turn_counter
