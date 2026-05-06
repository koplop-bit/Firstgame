import pygame
from pygame.sprite import Sprite
from bossbullet import BossBullet

class Boss(Sprite):
    def __init__(self, screen):
        super(Boss, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/emp5.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Початкове положення
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = -self.rect.height  #  поза екраном з

        # Швидкість переміщення
        self.speed_y = 2  # Вертикальна швидкість
        self.speed_x = 4  # Збільшена швидкість по арені
        self.direction = 1  # 1 вправо, -1 вліво

        # Здоров'я боса
        self.health = 1500

        # Кулі боса
        self.bullets = pygame.sprite.Group()

        import random
        self.random = random
        # Час останнього пострілу
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_delay = 500  # затримка 
        self.target_player = None
        
    def set_player(self, player):
        self.target_player = player

    def update(self):
        """Оновлення положення боса"""
        # Рух вниз, поки не досягне певної висоти
        if self.rect.top < 50:
            self.rect.y += self.speed_y
        else:
            # Рух вліво-вправо
            self.rect.x += self.speed_x * self.direction
            
            # Зміна напрямку 
            if self.rect.right >= self.screen_rect.right - 10:
                self.direction = -1
            elif self.rect.left <= 10:
                self.direction = 1

        self.update_bullets()

    def draw(self):
        """Малює боса та його кулі"""
        self.screen.blit(self.image, self.rect)
        self.bullets.draw(self.screen)

    def take_damage(self, amount):
        self.health -= amount

    def update_bullets(self):
        """Оновлення стану куль"""
        self.bullets.update()
        # Видалення куль що вийшли за межі екрану
        for bullet in self.bullets.copy():
            if bullet.rect.top > self.screen_rect.bottom:
                self.bullets.remove(bullet)

    def shoot(self):
        """Постріл боса (Спец атаки)"""
        attack_type = self.random.randint(1, 3)
        
        if attack_type == 1:
            # Атака 1: Віяло з 5 куль
            offsets = [-60, -30, 0, 30, 60]
            for offset in offsets:
                bullet = BossBullet(self.screen, self, x=self.rect.centerx + offset, y=self.rect.bottom)
                bullet.speed_x = offset * 0.05  # Розліт по горизонталі
                bullet.homing_factor = 0.01  # Легке наведення
                self.bullets.add(bullet)
                
        elif attack_type == 2:
            # Атака 2: Кулеметна черга (дуже швидкі кулі прямо)
            offsets = [-15, 15]
            for offset in offsets:
                bullet = BossBullet(self.screen, self, x=self.rect.centerx + offset, y=self.rect.bottom)
                bullet.speed_y = 8  # Швидка куля
                self.bullets.add(bullet)
                
        elif attack_type == 3:
            # Атака 3: Снаряд по боках і по центру
            offsets = [-100, 0, 100]
            for offset in offsets:
                bullet = BossBullet(self.screen, self, x=self.rect.centerx + offset, y=self.rect.bottom)
                bullet.speed_y = 4
                bullet.damage = 30  # Більше урону
                self.bullets.add(bullet)