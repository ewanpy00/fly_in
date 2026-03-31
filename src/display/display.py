from src.Map import Map
from src.Drone import Drone
import pygame

WIDTH, HEIGHT = 800, 600
OFFSET = 50

def get_screen_coords(x, y, min_max):
    min_x, max_x, min_y, max_y = min_max
    
    range_x = (max_x - min_x) if max_x != min_x else 1
    range_y = (max_y - min_y) if max_y != min_y else 1
    
    scale_x = (WIDTH - 2 * OFFSET) / range_x
    scale_y = (HEIGHT - 2 * OFFSET) / range_y
    
    screen_x = OFFSET + (x - min_x) * scale_x
    screen_y = OFFSET + (y - min_y) * scale_y
    return int(screen_x), int(screen_y)

def visualize(map, mode):
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fly-in Map Visualization")
    clock = pygame.time.Clock()

    xs = [z.x for z in map.zones]
    ys = [z.y for z in map.zones]
    min_max = (min(xs), max(xs), min(ys), max(ys))

    drones = []
    if len(map.zones) >= 2:
        drones.append(Drone(map.zones[0], get_screen_coords))

    # zones_cords = []
    i = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for drone in drones:
                        if not drone.is_moving and drone.current_zone.connections:
                            next_hop = drone.get_exit_path(map.zones)
                            drone.get_exit_path(map.zones)
                            drone.start_move(next_hop[i])
                            i += 1
                                

        screen.fill((30, 30, 30))

        for zone in map.zones:
            start_pos = get_screen_coords(zone.x, zone.y, min_max)
            
            for neighbor in zone.connections:
                end_pos = get_screen_coords(neighbor.x, neighbor.y, min_max)
                pygame.draw.line(screen, (100, 100, 100), start_pos, end_pos, 2)

        mouse_pos = pygame.mouse.get_pos()
        hovered_zone = None

        for zone in map.zones:
            zone_pos = get_screen_coords(zone.x, zone.y, min_max)            
            dist = ((zone_pos[0] - mouse_pos[0])**2 + (zone_pos[1] - mouse_pos[1])**2)**0.5
            color = getattr(zone, 'color', "white")

            if dist < 15:
                draw_color = pygame.Color("white") 
                pygame.draw.circle(screen, draw_color, zone_pos, 18)
                hovered_zone = zone
            else:
                try:
                    draw_color = pygame.Color(color)
                except ValueError:
                    draw_color = pygame.Color("white")
                pygame.draw.circle(screen, draw_color, zone_pos, 15)

        for drone in drones:
            drone.update()      # Дрон сам решит, нужно ли ему двигаться
            drone.draw(screen, min_max)

        if hovered_zone:
            pos = get_screen_coords(hovered_zone.x, hovered_zone.y, min_max)
            font = pygame.font.SysFont("Arial", 20, bold=True)

            text_surface = font.render(hovered_zone.name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(pos[0], pos[1] - 30))

            bg_rect = text_rect.inflate(10, 5)
            pygame.draw.rect(screen, (50, 50, 50), bg_rect, border_radius=5)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
