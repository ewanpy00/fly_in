from collections import deque
import pygame

class Drone:
    def __init__(self, start_zone, screen_coords_func):
        self.current_zone = start_zone
        self.target_zone = None 
        self.progress = 0.0
        # Скорость: чем меньше число, тем медленнее полет (0.02 = 50 кадров на путь)
        self.speed = 0.02 
        self.is_moving = False
        self.screen_coords = screen_coords_func
        self.exit_path = []

    def start_move(self, destination):
        if not self.is_moving and destination:
            self.target_zone = destination
            self.is_moving = True

    def update(self):
        if self.is_moving and self.target_zone:
            self.progress += self.speed
            
            if self.progress >= 1.0:
                self.current_zone = self.target_zone
                self.target_zone = None
                self.progress = 0.0
                self.is_moving = False
                return True # Сигнал, что полет завершен
        return False

    def get_current_world_pos(self):
        if not self.is_moving or self.target_zone is None:
            return self.current_zone.x, self.current_zone.y
            
        # Линейная интерполяция (LERP) между координатами зон
        curr_x = self.current_zone.x + (self.target_zone.x - self.current_zone.x) * self.progress
        curr_y = self.current_zone.y + (self.target_zone.y - self.current_zone.y) * self.progress
        return curr_x, curr_y
    
    def draw(self, screen, min_max):
        # Получаем игровые координаты
        wx, wy = self.get_current_world_pos()
        if self.progress >= 0.05 and self.progress <= 0.95:
            # Переводим в пиксели экрана
            screen_pos = self.screen_coords(wx, wy, min_max)
            # Рисуем дрона (желтый кружок)
            pygame.draw.circle(screen, (255, 255, 0), screen_pos, 7)
            # Опционально: обводка, чтобы дрон был заметнее
            pygame.draw.circle(screen, (0, 0, 0), screen_pos, 7, 1)

    def get_exit_path(self, zone_list):
    # 1. Находим старт (обычно это первая зона, но лучше проверить)
        start_node = zone_list[0] 

        # ПУТЬ должен быть списком: [start_node]
        queue = [(start_node, [start_node])] 
        visited = {start_node.name}

        while queue:
            current_zone, path = queue.pop(0)

            # Если это финиш
            if "goal" in current_zone.name or current_zone.type == "end_hub":
                return path 

            for neighbor in current_zone.connections:
                if neighbor.name not in visited and neighbor.type != "blocked":
                    visited.add(neighbor.name)
                    
                    # Теперь path — это список, и list(path) создаст его копию
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append((neighbor, new_path))
        return None