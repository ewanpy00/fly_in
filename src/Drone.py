from utils.ZoneType import ZoneType
import heapq
import pygame


class Drone:
    def __init__(self, start_zone, mode, name, speed):
        self.drone_name = name
        self.current_zone = start_zone
        self.target_zone = None
        self.progress = 0.0
        self.speed = speed
        self.is_moving = False
        self.exit_path = []
        self.debug_mode = mode

    def start_move(self, destination):
        if not self.is_moving:
            if destination:
                if self.current_zone.connections[destination] > 0:
                    self.current_zone.connections[destination] -= 1
                    self.target_zone = destination
                    self.is_moving = True
                else:
                    return
        else:
            if not self.debug_mode and destination:
                self.target_zone = destination

    def update(self):
        if self.is_moving and self.target_zone:
            if self.target_zone.type == ZoneType.RESTRICTED:
                self.progress += self.speed / 2
            else:
                self.progress += self.speed
            if self.progress >= 1.0:
                self.current_zone.connections[self.target_zone] += 1
                print(
                    f"[LOG] Drone {self.drone_name} ", end=""
                    )
                print(
                    f"moved from the {self.current_zone.name}", end=""
                    )
                print(
                    f" to the {self.target_zone.name}"
                    )
                self.current_zone = self.target_zone
                self.target_zone = None
                self.progress = 0.0
                self.is_moving = False
                return 1
        return 0

    def get_current_world_pos(self):
        if not self.is_moving or self.target_zone is None:
            return self.current_zone.x, self.current_zone.y

        d_x = self.target_zone.x - self.current_zone.x
        d_y = self.target_zone.y - self.current_zone.y

        c_x = self.current_zone.x + d_x * self.progress
        c_y = self.current_zone.y + d_y * self.progress
        return c_x, c_y

    def draw(self, screen, min_max, screen_cords):
        wx, wy = self.get_current_world_pos()

        if 0.06 <= self.progress <= 0.94:
            screen_pos = screen_cords(wx, wy, min_max)

            pygame.draw.circle(screen, (255, 255, 0), screen_pos, 7)
            pygame.draw.circle(screen, (0, 0, 0), screen_pos, 7, 1)

            font = pygame.font.SysFont("Arial", 16, bold=True)
            text_surface = font.render(str(self.drone_name),
                                       True,
                                       (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_pos[0],
                                                      screen_pos[1] - 15))
            bg_rect = text_rect.inflate(4, 2)
            pygame.draw.rect(screen, (30, 30, 30), bg_rect, border_radius=3)

            screen.blit(text_surface, text_rect)

    def get_exit_path(self):
        start_node = self.current_zone
        queue = []
        count = 0

        heapq.heappush(queue, (0, count, [start_node]))
        visited_costs = {start_node.name: 0}

        while queue:
            current_complexity, _, path = heapq.heappop(queue)
            current_zone = path[-1]

            if current_zone.title == "end_hub":
                return path

            for neighbor in current_zone.connections:
                if neighbor.type == ZoneType.BLOCKED:
                    continue

                base_cost = neighbor.type.cost
                traffic_penalty = neighbor.current_drones * 1
                
                step_complexity = base_cost + traffic_penalty
                new_total_complexity = current_complexity + step_complexity

                if neighbor.name not in visited_costs or \
                        new_total_complexity < visited_costs[neighbor.name]:

                    visited_costs[neighbor.name] = new_total_complexity
                    new_path = list(path)
                    new_path.append(neighbor)

                    count += 1
                    heapq.heappush(queue, (new_total_complexity,
                                           count,
                                           new_path))
        return None
