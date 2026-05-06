import pygame
from pygame.sprite import Sprite
from bossbullet import BossBullet

class BossTck(Sprite):
    def __init__(self, screen):
        super(BossTck, self).__init__()
        self.screen = screen
        try:
            self.image = pygame.image.load('images/boss.png').convert_alpha()
        except:
            self.image = pygame.Surface((150, 150), pygame.SRCALPHA)
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = -self.rect.height

        self.speed_y = 2
        self.speed_x = 4
        self.direction = 1

        self.health = 2000

        self.bullets = pygame.sprite.Group()

        import random
        self.random = random
        self.last_shot_time = pygame.time.get_ticks()
        self.target_player = None
        
    def set_player(self, player):
        self.target_player = player

    def update(self):
        if self.rect.top < 50:
            self.rect.y += self.speed_y
        else:
            self.rect.x += self.speed_x * self.direction
            if self.rect.right >= self.screen_rect.right - 10:
                self.direction = -1
            elif self.rect.left <= 10:
                self.direction = 1

        self.update_bullets()

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.bullets.draw(self.screen)

    def take_damage(self, amount):
        self.health -= amount

    def update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.top > self.screen_rect.bottom:
                self.bullets.remove(bullet)

    def shoot(self):
        bullet = BossBullet(self.screen, self, x=self.rect.centerx, y=self.rect.bottom)
        bullet.speed_y = 6
        bullet.damage = 50
        bullet.shape_type = 'dick'
        bullet.color = (0, 255, 0) # Зелений, як у Зеленського
        bullet.resize(40, 100)
        bullet.homing_factor = 0.03
        self.bullets.add(bullet)
