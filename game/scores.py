import pygame.font
from pygame.sprite import Group
from weapon import Gun

class Scores:
    def __init__(self, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 36)

        self.image_score()
        self.image_high_score()
        self.image_guns()
        self.image_wave()

    def image_wave(self):
        """Вивід поточної хвилі"""
        self.wave_img = self.font.render(f"Wave: {getattr(self.stats, 'wave', 1)}", True, self.text_color)
        self.wave_rect = self.wave_img.get_rect()
        self.wave_rect.right = self.screen_rect.right - 20
        self.wave_rect.top = 60

    def image_score(self):
        """Вивід поточних очок"""
        self.score_img = self.font.render(f"Score: {self.stats.score}", True, self.text_color)
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def image_high_score(self):
        """Вивід рекорду"""
        self.high_score_img = self.font.render(f"High Score: {self.stats.high_score}", True, self.text_color)
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def image_guns(self):
        """Вивід кількості життів"""
        self.guns = Group()
        for gun_number in range(self.stats.guns_left):
            gun = Gun(self.screen)
            gun.rect.x = 15 + gun_number * gun.rect.width
            gun.rect.y = 20
            self.guns.add(gun)

    def show_score(self):
        """Показує рахунок, рекорд і кількість життів"""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.wave_img, self.wave_rect)
        self.guns.draw(self.screen)
