from __future__ import annotations
import pygame
from typing import Tuple, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Map import Map
    from Zone import Zone


def draw_connections(screen: pygame.Surface,
                     map_obj: Map,
                     min_max: Tuple[float, float, float, float]) -> None:
    from display import get_screen_coords
    for zone in map_obj.zones:
        start_pos = get_screen_coords(zone.x, zone.y, min_max)
        for neighbor in zone.connections:
            end_pos = get_screen_coords(neighbor.x, neighbor.y, min_max)
            pygame.draw.line(screen, (100, 100, 100), start_pos, end_pos, 2)


def draw_zones(screen: pygame.Surface,
               map_obj: Map,
               min_max: Tuple[float, float, float, float],
               mouse_p: Tuple[int, int]) -> Optional[Zone]:
    from display import get_screen_coords
    hovered_zone: Optional[Zone] = None
    for zone in map_obj.zones:
        if zone.is_visible is True:
            zone_p = get_screen_coords(zone.x, zone.y, min_max)
            zp_mp0 = float(zone_p[0] - mouse_p[0])
            zp_mp1 = float(zone_p[1] - mouse_p[1])
            dist = (zp_mp0**2 + zp_mp1**2)**0.5

            color: str = getattr(zone, 'color', "white")
            radius: int = 15

            if dist < radius:
                draw_color = pygame.Color("white")
                pygame.draw.circle(screen, draw_color, zone_p, radius + 3)
                hovered_zone = zone
            else:
                try:
                    draw_color = pygame.Color(color)
                except ValueError:
                    draw_color = pygame.Color("white")
                pygame.draw.circle(screen, draw_color, zone_p, radius)

    return hovered_zone


def draw_tooltip(screen: pygame.Surface,
                 zone: Zone,
                 min_max: Tuple[float, float, float, float]) -> None:
    from display import get_screen_coords
    pos = get_screen_coords(zone.x, zone.y, min_max)
    font = pygame.font.SysFont("Arial", 18, bold=True)

    text_surf = font.render(zone.name, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(pos[0], pos[1] - 35))

    bg_rect = text_rect.inflate(14, 8)
    pygame.draw.rect(screen,
                     (40, 40, 40),
                     bg_rect,
                     border_radius=5)
    pygame.draw.rect(screen,
                     (200, 200, 200),
                     bg_rect,
                     width=1,
                     border_radius=5)

    screen.blit(text_surf, text_rect)


def draw_ui_counter(screen: pygame.Surface,
                    turn_counter: int,
                    font: pygame.font.Font) -> None:
    text_str = f"Total Turns: {turn_counter}"
    turn_surf = font.render(text_str, True, (0, 255, 0))
    text_pos = (25, 20)

    shadow_surf = font.render(text_str, True, (0, 50, 0))
    screen.blit(shadow_surf, (text_pos[0] + 2, text_pos[1] + 2))
    screen.blit(turn_surf, text_pos)
