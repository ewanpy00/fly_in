from __future__ import annotations
import pygame
import rendering as r
from typing import Tuple, TYPE_CHECKING
from movement import MovementSystem

if TYPE_CHECKING:
    from Map import Map

WIDTH: int = 800
HEIGHT: int = 600
OFFSET: int = 70


class Viewport:
    def __init__(
        self,
        width: int = WIDTH,
        height: int = HEIGHT,
        offset: int = OFFSET,
    ) -> None:
        self.width = width
        self.height = height
        self.offset = offset

    def screen_coords(
        self,
        x: float,
        y: float,
        min_max: Tuple[float, float, float, float],
    ) -> Tuple[int, int]:
        min_x, max_x, min_y, max_y = min_max

        range_x = (max_x - min_x) if max_x != min_x else 1.0
        range_y = (max_y - min_y) if max_y != min_y else 1.0

        scale_x = (self.width - 2 * self.offset) / range_x
        scale_y = (self.height - 2 * self.offset) / range_y

        screen_x = self.offset + (x - min_x) * scale_x
        screen_y = self.offset + (y - min_y) * scale_y
        return int(screen_x), int(screen_y)


class SimulationView:
    def __init__(
        self,
        map_obj: Map,
        mode: bool,
        viewport: Viewport | None = None,
        movement: MovementSystem | None = None,
    ) -> None:
        self.map_obj = map_obj
        self.mode = mode
        self.viewport = viewport or Viewport()
        self.movement = movement or MovementSystem()
        self.renderer = r.Renderer(self.viewport.screen_coords)

        xs = [float(z.x) for z in self.map_obj.zones]
        ys = [float(z.y) for z in self.map_obj.zones]
        self.min_max = (min(xs), max(xs), min(ys), max(ys))

        self.turn_counter = 0
        self.font_turns: pygame.font.Font | None = None

    def _handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.mode and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.turn_counter = self.movement.step(
                        self.map_obj,
                        self.turn_counter,
                    )
        return True

    def _auto_step(self) -> None:
        if not self.mode:
            self.turn_counter = self.movement.step(
                self.map_obj,
                self.turn_counter,
            )

    def _update_drones(self) -> None:
        for drone in self.map_obj.drones:
            drone.update()

    def _draw_frame(self, screen: pygame.Surface) -> None:
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()

        screen.fill((30, 30, 30))
        self.renderer.draw_connections(screen, self.map_obj, self.min_max)
        hovered_zone = self.renderer.draw_zones(
            screen,
            self.map_obj,
            self.min_max,
            mouse_pos,
        )

        for drone in self.map_obj.drones:
            drone.draw(screen, self.min_max, self.viewport.screen_coords)

        if hovered_zone:
            self.renderer.draw_tooltip(screen, hovered_zone, self.min_max)

        if self.font_turns is None:
            self.font_turns = pygame.font.SysFont(
                "Arial",
                24,
                bold=True,
            )
        self.renderer.draw_ui_counter(
            screen,
            self.turn_counter,
            self.font_turns,
        )

    def run(self) -> None:
        pygame.init()
        screen: pygame.Surface = pygame.display.set_mode(
            (self.viewport.width, self.viewport.height)
        )
        pygame.display.set_caption("Fly-in Map Visualization")
        clock: pygame.time.Clock = pygame.time.Clock()

        running = True
        while running:
            running = self._handle_events()
            self._auto_step()
            self._update_drones()
            self._draw_frame(screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    @classmethod
    def open(cls, map_obj: Map, mode: bool) -> None:
        cls(map_obj, mode).run()
