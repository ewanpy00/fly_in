from __future__ import annotations
import pygame
import rendering as r
from typing import Tuple, List, TYPE_CHECKING
from movement import process_drones_step

if TYPE_CHECKING:
    from Map import Map

WIDTH: int = 800
HEIGHT: int = 600
OFFSET: int = 70


def get_screen_coords(x: float,
                      y: float,
                      min_max: Tuple[float, float, float, float]
                      ) -> Tuple[int, int]:
    min_x, max_x, min_y, max_y = min_max

    range_x = (max_x - min_x) if max_x != min_x else 1.0
    range_y = (max_y - min_y) if max_y != min_y else 1.0

    scale_x = (WIDTH - 2 * OFFSET) / range_x
    scale_y = (HEIGHT - 2 * OFFSET) / range_y

    screen_x = OFFSET + (x - min_x) * scale_x
    screen_y = OFFSET + (y - min_y) * scale_y
    return int(screen_x), int(screen_y)


def visualize(map_obj: Map, mode: bool) -> None:
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fly-in Map Visualization")
    clock: pygame.time.Clock = pygame.time.Clock()

    xs: List[float] = [float(z.x) for z in map_obj.zones]
    ys: List[float] = [float(z.y) for z in map_obj.zones]
    min_max = (min(xs), max(xs), min(ys), max(ys))

    turn_counter: int = 0
    font_turns: pygame.font.Font = pygame.font.SysFont("Arial", 24, bold=True)
    running: bool = True

    while running:
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if mode and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    turn_counter = process_drones_step(map_obj, turn_counter)

        if not mode:
            turn_counter = process_drones_step(map_obj, turn_counter)

        for drone in map_obj.drones:
            drone.update()

        screen.fill((30, 30, 30))
        r.draw_connections(screen, map_obj, min_max)
        hovered_zone = r.draw_zones(screen, map_obj, min_max, mouse_pos)

        for drone in map_obj.drones:
            drone.draw(screen, min_max, get_screen_coords)

        if hovered_zone:
            r.draw_tooltip(screen, hovered_zone, min_max)

        r.draw_ui_counter(screen, turn_counter, font_turns)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
