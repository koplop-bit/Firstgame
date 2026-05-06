import pygame
import random
import math
from pygame.sprite import Sprite, Group

class Boss3(Sprite):
    def __init__(self, screen):
        super(Boss3, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Завантаження зображення боса
        try:
            self.image = pygame.image.load('images/emp7.png').convert_alpha()
            self.rect = self.image.get_rect()
        except:
            # Якщо зображення не знайдено, створюємо червоний прямокутник
            self.image = pygame.Surface((80, 80))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()
        
        # Початкова позиція боса (зверху екрану)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = 50
        
        # Параметри боса
        self.health = 1750
        self.speed = 3.5  # Збільшена швидкість
        self.direction = 1
        self.bullets = Group()
        self.last_shot_time = pygame.time.get_ticks()
        self.x = float(self.rect.x)
        
        # Параметри атак
        self.current_attack = 1
        self.attack_phase = 0
        self.bullets_in_attack = 0
        self.warning_line_start_time = 0
        self.warning_line_active = False
        self.warning_line_x = self.rect.centerx  # Позиція червоної лінії
        self.target_player = None  # Посилання на гравця для відслідковування
        
    def set_player(self, player):
        """Встановлює посилання на гравця для відслідковування"""
        self.target_player = player
        
    def update(self):
        """Оновлення позиції боса"""
        # Горизонтальний рух
        self.x += self.speed * self.direction
        if self.x <= 0:
            self.direction = 1
        elif self.x >= self.screen_rect.width - self.rect.width:
            self.direction = -1
        self.rect.x = self.x
        
        # Оновлення попереджувальної лінії
        if self.warning_line_active:
            current_time = pygame.time.get_ticks()
            if self.target_player:  # Якщо є посилання на гравця
                self.warning_line_x = self.target_player.rect.centerx  # Слідкуємо за гравцем
            if current_time - self.warning_line_start_time >= 1000:  # Збільшено час попередження до 1 секунди
                self.warning_line_active = False
                # Створюємо смертельний промінь
                from bossbullet import BossBullet
                beam = BossBullet(self.screen, self)
                beam.resize(50, self.screen_rect.height)
                beam.shape_type = 'rectangle'
                beam.rect.centerx = self.warning_line_x
                beam.rect.top = self.rect.bottom
                beam.speed = 0
                beam.damage = 1  # Смертельний промінь забирає життя
                self.bullets.add(beam)
                self.current_attack = random.randint(1, 4)
                self.bullets_in_attack = 0
        
    def take_damage(self, amount):
        self.health -= amount
        
    def draw(self):
        """Відображення боса на екрані"""
        self.screen.blit(self.image, self.rect)
        # Малюємо кулі
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        # Малюємо попереджувальну лінію
        if self.warning_line_active and self.target_player:
            line_rect = pygame.Rect(self.warning_line_x - 25, self.rect.bottom, 50, self.screen_rect.height - self.rect.bottom)
            pygame.draw.rect(self.screen, (255, 0, 0), line_rect, 2)  # Тонша червона лінія
            
    def shoot(self):
        """Постріл боса"""
        from bossbullet import BossBullet
        current_time = pygame.time.get_ticks()
        
        if self.current_attack == 1:
            # Перша атака: діагональні кулі (повільніше)
            if self.bullets_in_attack < 2:
                # Ліва куля
                left_bullet = BossBullet(self.screen, self)
                left_bullet.resize(30)
                left_bullet.shape_type = 'circle'
                left_bullet.rect.left = 0
                left_bullet.rect.top = 0
                left_bullet.speed = 3  # Зменшено швидкість з 3 до 2
                left_bullet.speed_x = 2  # Зменшено з 2 до 1.5
                left_bullet.speed_y = 2
                left_bullet.homing_factor = 0.02
                
                # Права куля
                right_bullet = BossBullet(self.screen, self)
                right_bullet.resize(30)
                right_bullet.shape_type = 'circle'
                right_bullet.rect.right = self.screen_rect.width
                right_bullet.rect.top = 0
                right_bullet.speed = 3
                right_bullet.speed_x = -2
                right_bullet.speed_y = 2
                right_bullet.homing_factor = 0.02
                
                self.bullets.add(left_bullet)
                self.bullets.add(right_bullet)
                self.bullets_in_attack += 1
            else:
                self.current_attack = random.randint(1, 4)
                self.bullets_in_attack = 0
                
        elif self.current_attack == 2:
            # Друга атака: великий прямокутник (повільніше)
            if self.bullets_in_attack == 0:
                rect_bullet = BossBullet(self.screen, self)
                rect_bullet.resize(350, 100)
                rect_bullet.shape_type = 'rectangle'
                rect_bullet.rect.centerx = self.screen_rect.centerx
                rect_bullet.rect.top = self.rect.bottom + 20
                rect_bullet.speed = 2  # Зменшено швидкість з 2 до 1
                rect_bullet.speed_y = rect_bullet.speed
                
                self.bullets.add(rect_bullet)
                self.bullets_in_attack += 1
            else:
                self.current_attack = random.randint(1, 4)
                self.bullets_in_attack = 0
                
        elif self.current_attack == 3:
            # Третя атака: центральний прямокутник (повільніше)
            if self.bullets_in_attack == 0:
                center_rect = BossBullet(self.screen, self)
                center_rect.resize(350, 100)
                center_rect.shape_type = 'rectangle'
                center_rect.rect.centerx = self.screen_rect.centerx
                center_rect.rect.top = self.rect.bottom
                center_rect.speed = 2  # Зменшено швидкість з 3 до 1.5
                center_rect.speed_y = center_rect.speed
                
                self.bullets.add(center_rect)
                self.bullets_in_attack += 1
            else:
                self.current_attack = random.randint(1, 4)
                self.bullets_in_attack = 0
                
        elif self.current_attack == 4:
            # Четверта атака: попереджувальна лінія, що слідкує за гравцем
            if not self.warning_line_active:
                self.warning_line_active = True
                self.warning_line_start_time = pygame.time.get_ticks()
            
    def update_bullets(self):
        """Оновлення позиції куль боса"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if (bullet.rect.top >= self.screen_rect.bottom or
                bullet.rect.right < 0 or
                bullet.rect.left > self.screen_rect.width):
                self.bullets.remove(bullet) 