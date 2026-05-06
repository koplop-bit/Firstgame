import pygame
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

class Analytics:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Налаштування шрифту для заголовків
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        # Заголовок
        self.title = "Game Analytics"
        self.title_color = (255, 255, 255)
        self.title_image = self.font.render(self.title, True, self.title_color)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.centerx = self.screen_rect.centerx
        self.title_rect.top = 50
        
        # Кнопка повернення
        self.back_text = "Press ESC to return"
        self.back_color = (250, 250, 250)
        self.back_image = self.small_font.render(self.back_text, True, self.back_color)
        self.back_rect = self.back_image.get_rect()
        self.back_rect.centerx = self.screen_rect.centerx
        self.back_rect.bottom = self.screen_rect.bottom - 30
        
        # Створення графіка
        self.create_chart()
        
    def create_chart(self):
        try:
            # Читаємо очки за кожне життя з файлу
            with open('life_scores.txt', 'r') as f:
                life_scores = [int(line.strip()) for line in f.readlines()]
                if len(life_scores) != 3:
                    life_scores = [0, 0, 0]
        except (FileNotFoundError, ValueError):
            life_scores = [0, 0, 0]
            
        # Дані для кругової діаграми
        data = life_scores
        total_score = sum(data)
        
        # Якщо всі очки 0 рівномірний розподіл
        if total_score == 0:
            data = [1, 1, 1]  # Рівні частини для візуалізації
            total_score = "No scores yet"
        
        # Покращені підписи для життів
        labels = [
            f'First Life (★★★): {life_scores[0]} pts',
            f'Second Life (★★): {life_scores[1]} pts',
            f'Last Life (★): {life_scores[2]} pts'
        ]
        colors = ["#EC7F7F", '#66B2FF', '#99FF99']
        
        # Створюємо графік з покращеним форматуванням
        plt.figure(figsize=(6, 6))
        plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', 
                labeldistance=1.1, pctdistance=0.8)
        plt.title(f'Score Distribution by Life\nTotal Score: {total_score}', pad=20)
        
        # Додаємо легенду
        plt.legend(labels, title="Life Scores", 
                  loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Зберігаємо графік у пам'яті
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', transparent=True)
        buffer.seek(0)
        plt.close()
        
        # Конвертуємо в pygame
        chart_str = buffer.getvalue()
        buffer.close()
        
        # Створюємо поверхню з графіком
        import pygame.image
        from pygame.locals import RLEACCEL
        
        chart_surface = pygame.image.load(BytesIO(chart_str))
        self.chart_surface = pygame.transform.scale(chart_surface, (500, 400))  # Збільшено ширину для легенди
        self.chart_rect = self.chart_surface.get_rect()
        self.chart_rect.centerx = self.screen_rect.centerx
        self.chart_rect.centery = self.screen_rect.centery + 30
        
    def draw(self):
        # екран чорним
        self.screen.fill((0, 0, 0))
        
        # Малюємо заголовок
        self.screen.blit(self.title_image, self.title_rect)
        
        # Малюємо графік
        self.screen.blit(self.chart_surface, self.chart_rect)
        
        # Малюємо кнопку повернення
        self.screen.blit(self.back_image, self.back_rect)
        
        # Оновлюємо екран
        pygame.display.flip() 