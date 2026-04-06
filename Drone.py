from typing import List, Optional, Tuple, Dict, Any, Callable
from ZoneType import ZoneType
import heapq
import pygame


class Drone:
    def __init__(self,
                 start_zone: Any,
                 mode: bool,
                 name: int,
                 speed: float) -> None:
        self.drone_name: int = name
        self.current_zone: Any = start_zone
        self.target_zone: Optional[Any] = None
        self.progress: float = 0.0
        self.speed: float = speed
        self.is_moving: bool = False
        self.exit_path: List[Any] = []
        self.debug_mode: bool = mode
        self.delay: int = 0

    def start_move(self, destination: Optional[Any]) -> None:
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

    def update(self) -> int:
        if self.is_moving and self.target_zone:
            if self.target_zone.type == ZoneType.RESTRICTED:
                self.progress += self.speed / 2
            else:
                self.progress += self.speed

            if self.progress >= 1.0:
                self.current_zone.connections[self.target_zone] += 1
                if self.target_zone.title == "common_buffer":
                    target_conn_zone = next(iter(self.target_zone.connections))
                    print(f"{self.drone_name}-connection_{target_conn_zone.name} ", end="")
                else:
                    print(f"{self.drone_name}-{self.target_zone.name} ", end="")

                self.current_zone = self.target_zone
                self.target_zone = None
                self.progress = 0.0
                self.is_moving = False
                return 1
        return 0

    def get_current_world_pos(self) -> Tuple[float, float]:
        if not self.is_moving or self.target_zone is None:
            return float(self.current_zone.x), float(self.current_zone.y)

        d_x: float = self.target_zone.x - self.current_zone.x
        d_y: float = self.target_zone.y - self.current_zone.y

        c_x: float = self.current_zone.x + d_x * self.progress
        c_y: float = self.current_zone.y + d_y * self.progress
        return c_x, c_y

    def draw(self,
             screen: pygame.Surface,
             min_max: Any,
             screen_cords: Callable[[float, float, Any], Tuple[int, int]]
             ) -> None:

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

    def get_exit_path(self) -> Optional[List[Any]]:
        start_node: Any = self.current_zone
        queue: List[Tuple[int, int, List[Any]]] = []
        count: int = 0

        heapq.heappush(queue, (0, count, [start_node]))
        visited_costs: Dict[str, int] = {start_node.name: 0}

        while queue:
            current_complexity, _, path = heapq.heappop(queue)
            current_zone: Any = path[-1]

            if current_zone.title == "end_hub":
                return path

            for neighbor in current_zone.connections:
                if neighbor.type == ZoneType.BLOCKED:
                    continue

                base_cost = neighbor.type.cost
                step_complexity = base_cost
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
