from src.display.movement import process_drones_step
from src.display.rendering import draw_connections, draw_zones, draw_tooltip, draw_ui_counter
from src.Map import Map
from src.Drone import Drone
import pygame

WIDTH, HEIGHT = 800, 600
OFFSET = 70

def get_screen_coords(x, y, min_max):
    min_x, max_x, min_y, max_y = min_max
    
    range_x = (max_x - min_x) if max_x != min_x else 1
    range_y = (max_y - min_y) if max_y != min_y else 1
    
    scale_x = (WIDTH - 2 * OFFSET) / range_x
    scale_y = (HEIGHT - 2 * OFFSET) / range_y
    
    screen_x = OFFSET + (x - min_x) * scale_x
    screen_y = OFFSET + (y - min_y) * scale_y
    return int(screen_x), int(screen_y)


def visualize(map_obj, mode):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fly-in Map Visualization")
    clock = pygame.time.Clock()

    xs, ys = [z.x for z in map_obj.zones], [z.y for z in map_obj.zones]
    min_max = (min(xs), max(xs), min(ys), max(ys))
    
    turn_counter = 0
    font_turns = pygame.font.SysFont("Arial", 24, bold=True)
    running = True 

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # 1. ОБРАБОТКА СОБЫТИЙ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if mode and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                turn_counter = process_drones_step(map_obj, turn_counter)

        # 2. АВТОМАТИЧЕСКИЙ ШАГ
        if not mode:
            turn_counter = process_drones_step(map_obj, turn_counter)

        # 3. ОБНОВЛЕНИЕ СОСТОЯНИЙ
        for drone in map_obj.drones:
            drone.update()

        # 4. ОТРИСОВКА
        screen.fill((30, 30, 30))
        draw_connections(screen, map_obj, min_max)
        hovered_zone = draw_zones(screen, map_obj, min_max, mouse_pos)
        
        for drone in map_obj.drones:
            drone.draw(screen, min_max, get_screen_coords)

        # UI: Тултипы и счетчик
        if hovered_zone:
            draw_tooltip(screen, hovered_zone, min_max)
            
        draw_ui_counter(screen, turn_counter, font_turns)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
