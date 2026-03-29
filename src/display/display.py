import pygame

# Настройки экрана
WIDTH, HEIGHT = 800, 600
OFFSET = 50

def get_screen_coords(x, y, min_max):
    min_x, max_x, min_y, max_y = min_max
    
    # Чтобы не делить на ноль, если все точки в одной линии
    range_x = (max_x - min_x) if max_x != min_x else 1
    range_y = (max_y - min_y) if max_y != min_y else 1
    
    scale_x = (WIDTH - 2 * OFFSET) / range_x
    scale_y = (HEIGHT - 2 * OFFSET) / range_y
    
    screen_x = OFFSET + (x - min_x) * scale_x
    screen_y = OFFSET + (y - min_y) * scale_y
    return int(screen_x), int(screen_y)

def visualize(zones_list):
    pygame.init()
    # Исправил опечатку в инициализации экрана
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fly-in Map Visualization")
    clock = pygame.time.Clock()
    
    # 1. Находим границы карты (работаем со списком)
    xs = [z.x for z in zones_list]
    ys = [z.y for z in zones_list]
    min_max = (min(xs), max(xs), min(ys), max(ys))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30)) # Темный фон

        # 2. РИСУЕМ СВЯЗИ (Линии)
        for zone in zones_list:
            start_pos = get_screen_coords(zone.x, zone.y, min_max)
            for neighbor_name in zone.connections:
                # Ищем объект соседа в списке по его имени
                neighbor_obj = next((z for z in zones_list if z.name == neighbor_name), None)
                if neighbor_obj:
                    end_pos = get_screen_coords(neighbor_obj.x, neighbor_obj.y, min_max)
                    pygame.draw.line(screen, (100, 100, 100), start_pos, end_pos, 2)

# Получаем текущую позицию мыши
        mouse_pos = pygame.mouse.get_pos()
        hovered_zone = None  # Переменная для хранения зоны под курсором

        # 3. РИСУЕМ ХАБЫ
        for zone in zones_list:
            pos = get_screen_coords(zone.x, zone.y, min_max)
            
            # Проверяем, наведен ли курсор (радиус хаба 15 пикселей)
            dist = ((pos[0] - mouse_pos[0])**2 + (pos[1] - mouse_pos[1])**2)**0.5
            
            color = getattr(zone, 'color', "white")
            # Если навели — делаем круг чуть ярче или больше
            if dist < 15:
                draw_color = pygame.Color("white") 
                pygame.draw.circle(screen, draw_color, pos, 18) # Увеличиваем при наведении
                hovered_zone = zone # Запоминаем, кого подсветить текстом
            else:
                try:
                    draw_color = pygame.Color(color)
                except ValueError:
                    draw_color = pygame.Color("white")
                pygame.draw.circle(screen, draw_color, pos, 15)

        # 4. РИСУЕМ ТЕКСТ (только для той зоны, на которую навели)
        if hovered_zone:
            pos = get_screen_coords(hovered_zone.x, hovered_zone.y, min_max)
            font = pygame.font.SysFont("Arial", 20, bold=True)
            
            # Создаем подложку для текста (чтобы он был читаем на любом фоне)
            text_surface = font.render(hovered_zone.name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(pos[0], pos[1] - 30))
            
            # Рисуем небольшую тень или рамку
            bg_rect = text_rect.inflate(10, 5)
            pygame.draw.rect(screen, (50, 50, 50), bg_rect, border_radius=5)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()