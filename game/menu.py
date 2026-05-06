import pygame
import random

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Налаштування шрифту для заголовку
        self.title_font = pygame.font.Font(None, 74)
        self.prompt_font = pygame.font.Font(None, 36)
        
        # Створення заголовку
        self.title = "SPACE INVADERS"
        self.title_color = (255, 255, 255)
        self.title_image = self.title_font.render(self.title, True, self.title_color)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.centerx = self.screen_rect.centerx
        self.title_rect.centery = self.screen_rect.centery - 50
        
        # Створення підказки для старту
        self.prompt = "Press ENTER to start"
        self.prompt_color = (255, 255, 0)  # Жовтий колір
        self.prompt_image = self.prompt_font.render(self.prompt, True, self.prompt_color)
        self.prompt_rect = self.prompt_image.get_rect()
        self.prompt_rect.centerx = self.screen_rect.centerx
        self.prompt_rect.bottom = self.screen_rect.bottom - 80
        
        # Створення кнопки аналітики
        self.analytics = "A-Analytics | U-Upgrades | S-Skins | M-Map | C-Crafting | ESC-Exit"
        self.analytics_color = (255, 255, 0)  # Жовтий колір
        self.analytics_image = self.prompt_font.render(self.analytics, True, self.analytics_color)
        self.analytics_rect = self.analytics_image.get_rect()
        self.analytics_rect.centerx = self.screen_rect.centerx
        self.analytics_rect.bottom = self.screen_rect.bottom - 30
        
        # Анімація зірок
        self.stars = []
        self.create_stars()
        
    def create_stars(self):
        # Створюємо зірки як маленькі білі крапки
        for _ in range(50):  # 50 зірок
            x = random.randint(0, self.screen_rect.width)
            y = random.randint(0, self.screen_rect.height)
            size = random.randint(1, 3)
            brightness = random.randint(100, 255)
            self.stars.append({
                'pos': [x, y],
                'size': size,
                'brightness': brightness,
                'speed': random.randint(1, 3)
            })
    
    def update_stars(self):
        # Оновлюємо позиції зірок
        for star in self.stars:
            # Рух зірок вниз
            star['pos'][1] += star['speed']
            # Якщо зірка виходить за межі екрану, переміщуємо її вгору
            if star['pos'][1] > self.screen_rect.height:
                star['pos'][1] = 0
                star['pos'][0] = random.randint(0, self.screen_rect.width)
    
    def draw(self):
        # Заливаємо екран чорним
        self.screen.fill((0, 0, 0))
        
        # Малюємо зірки
        for star in self.stars:
            pygame.draw.circle(
                self.screen,
                (star['brightness'], star['brightness'], star['brightness']),
                star['pos'],
                star['size']
            )
        
        # Малюємо заголовок та підказки
        self.screen.blit(self.title_image, self.title_rect)
        self.screen.blit(self.prompt_image, self.prompt_rect)
        self.screen.blit(self.analytics_image, self.analytics_rect)
        
        # Оновлюємо екран
        pygame.display.flip() 